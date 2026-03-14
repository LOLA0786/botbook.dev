"""
botbook.core.bridge
-------------------
Bridges botbook.dev ↔ LORK ↔ PrivateVault.
"""

from __future__ import annotations
import logging
import httpx
import os
from typing import Optional

from .models import MemberProfile, MemberType, Badge

logger = logging.getLogger("botbook.bridge")


class LORKBridge:

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = (base_url or os.getenv("LORK_URL","http://localhost:9000")).rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {api_key or os.getenv('LORK_API_KEY','')}",
            "Content-Type": "application/json"
        }

    async def register_agent(self, profile: MemberProfile) -> Optional[str]:
        payload = {
            "name": profile.name,
            "owner": profile.owner_id or "unowned",
            "permissions": profile.capabilities,
            "botbook_id": profile.member_id,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.post(
                    f"{self.base_url}/v1/agents/register",
                    json=payload,
                    headers=self.headers
                )
                r.raise_for_status()
                return r.json().get("agent_id")
        except Exception:
            return None


    async def check_policy(self, lork_agent_id: str, action: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.post(
                    f"{self.base_url}/v1/policy/check",
                    json={"agent_id": lork_agent_id, "action": action},
                    headers=self.headers,
                )
                return r.json().get("allowed", False)
        except Exception:
            return False



class PrivateVaultBridge:

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = (base_url or os.getenv("PRIVATEVAULT_URL","http://localhost:9001")).rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {api_key or os.getenv('PRIVATEVAULT_API_KEY','')}",
            "Content-Type": "application/json"
        }

    async def issue_identity(self, profile: MemberProfile) -> Optional[str]:
        payload = {
            "member_id": profile.member_id,
            "member_type": profile.member_type.value,
            "name": profile.name,
            "capabilities": profile.capabilities,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.post(
                    f"{self.base_url}/v1/identity/issue",
                    json=payload,
                    headers=self.headers
                )
                r.raise_for_status()
                return r.json().get("vault_id")
        except Exception:
            return None


    async def issue_badge(self, profile: MemberProfile) -> Badge:
        if not profile.vault_id:
            return Badge.UNVERIFIED

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.post(
                    f"{self.base_url}/v1/badges/evaluate",
                    json={
                        "vault_id": profile.vault_id,
                        "trust_score": profile.trust_score
                    },
                    headers=self.headers,
                )
                r.raise_for_status()
                badge = r.json().get("badge","unverified")
                return Badge(badge)
        except Exception:
            return profile.trust.compute_badge()



class BotBookBridge:

    def __init__(
        self,
        lork_url: str | None = None,
        vault_url: str | None = None,
        lork_key: str | None = None,
        vault_key: str | None = None
    ):
        self.lork = LORKBridge(lork_url, lork_key)
        self.vault = PrivateVaultBridge(vault_url, vault_key)


    async def onboard_agent(self, profile: MemberProfile) -> MemberProfile:

        assert profile.member_type == MemberType.AGENT

        profile.lork_agent_id = await self.lork.register_agent(profile)

        profile.vault_id = await self.vault.issue_identity(profile)

        profile.trust.update_audit_hash(profile.member_id)

        return profile


    async def onboard_human(self, profile: MemberProfile) -> MemberProfile:

        assert profile.member_type == MemberType.HUMAN

        profile.vault_id = await self.vault.issue_identity(profile)

        profile.trust.update_audit_hash(profile.member_id)

        return profile

