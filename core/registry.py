from typing import List
from agents.agent import Agent
from core.capability_index import capability_index

class AgentRegistry:

    def __init__(self):
        self.agents = []

    def register(self, agent: Agent):

        self.agents.append(agent)
        capability_index.register(agent)

        return agent

    def list_agents(self) -> List[Agent]:
        return self.agents

registry = AgentRegistry()
