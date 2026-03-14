"""
botbook.__init__
----------------
The developer-facing SDK. This is what goes in every agent's codebase:

    from botbook import BotBook, MatchIntent
"""

from __future__ import annotations
import asyncio
import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict

from .core.models import MemberProfile, MemberType, Badge, TrustProfile
from .core.bridge import BotBookBridge

logger = logging.getLogger("botbook")


@dataclass
class MatchIntent:
    task: str
    required_capabilities: List[str] = field(default_factory=list)
    min_trust_score: float = 0.0
    min_badge: Badge = Badge.UNVERIFIED
    member_type_filter: Optional[MemberType] = None
    max_results: int = 10


_BADGE_RANK = {
    Badge.UNVERIFIED: 0,
    Badge.VERIFIED: 1,
    Badge.TRUSTED: 2,
    Badge.CERTIFIED: 3,
}


class BotBook:

    def __init__(
        self,
        lork_url: str = "http://localhost:9000",
        vault_url: str = "http://localhost:9001",
        lork_key: str = "",
        vault_key: str = "",
    ):
        self.bridge = BotBookBridge(lork_url, vault_url, lork_key, vault_key)
        self._registry: Dict[str, MemberProfile] = {}

    # ------------------------------------------------------------ #
    # Registration
    # ------------------------------------------------------------ #

    def register_agent(
        self,
        name: str,
        capabilities: List[str],
        owner_id: Optional[str] = None,
    ) -> MemberProfile:

        profile = MemberProfile(
            name=name,
            member_type=MemberType.AGENT,
            capabilities=capabilities,
            owner_id=owner_id,
        )

        profile = asyncio.run(self.bridge.onboard_agent(profile))
        self._registry[profile.member_id] = profile

        logger.info(f"Agent registered: {profile.member_id}")
        return profile


    def register_human(
        self,
        name: str,
        email: str,
        capabilities: Optional[List[str]] = None,
    ) -> MemberProfile:

        profile = MemberProfile(
            name=name,
            member_type=MemberType.HUMAN,
            email=email,
            capabilities=capabilities or [],
        )

        profile = asyncio.run(self.bridge.onboard_human(profile))
        self._registry[profile.member_id] = profile

        logger.info(f"Human registered: {profile.member_id}")
        return profile


    # ------------------------------------------------------------ #
    # Discovery
    # ------------------------------------------------------------ #

    def match(self, intent: MatchIntent) -> List[MemberProfile]:

        candidates = list(self._registry.values())
        results = []

        for member in candidates:

            if intent.member_type_filter and member.member_type != intent.member_type_filter:
                continue

            if member.trust_score < intent.min_trust_score:
                continue

            if _BADGE_RANK[member.badge] < _BADGE_RANK[intent.min_badge]:
                continue

            cap_overlap = len(
                set(member.capabilities) & set(intent.required_capabilities)
            )

            if intent.required_capabilities and cap_overlap == 0:
                continue

            cap_score = cap_overlap / max(len(intent.required_capabilities), 1)
            badge_score = _BADGE_RANK[member.badge] / 3.0

            score = (
                (cap_score * 0.5)
                + (member.trust_score * 0.3)
                + (badge_score * 0.2)
            )

            results.append((score, member))

        results.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in results[: intent.max_results]]


    def get_member(self, member_id: str) -> Optional[MemberProfile]:
        return self._registry.get(member_id)


    def list_members(
        self,
        member_type: Optional[MemberType] = None,
        min_badge: Badge = Badge.UNVERIFIED,
    ) -> List[MemberProfile]:

        members = list(self._registry.values())

        if member_type:
            members = [m for m in members if m.member_type == member_type]

        members = [
            m for m in members
            if _BADGE_RANK[m.badge] >= _BADGE_RANK[min_badge]
        ]

        return sorted(members, key=lambda m: m.trust_score, reverse=True)


    # ------------------------------------------------------------ #
    # Trust updates
    # ------------------------------------------------------------ #

    def record_task_completed(self, member_id: str, rating: float = 5.0) -> None:

        m = self._registry.get(member_id)
        if not m:
            return

        m.trust.tasks_completed += 1

        n = m.trust.rating_count + 1
        m.trust.avg_rating = (
            (m.trust.avg_rating * m.trust.rating_count) + rating
        ) / n

        m.trust.rating_count = n
        m.trust.update_audit_hash(member_id)


    def record_task_failed(self, member_id: str) -> None:

        m = self._registry.get(member_id)
        if not m:
            return

        m.trust.tasks_failed += 1
        m.trust.update_audit_hash(member_id)


    def record_policy_violation(self, member_id: str) -> None:

        m = self._registry.get(member_id)
        if not m:
            return

        m.trust.policy_violations += 1
        m.trust.update_audit_hash(member_id)

        logger.warning(f"Policy violation recorded for {member_id}")
