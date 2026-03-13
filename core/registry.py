from typing import List
from agents.agent import Agent

class AgentRegistry:
    def __init__(self):
        self.agents = []

    def register(self, agent: Agent):
        self.agents.append(agent)
        return agent

    def list_agents(self) -> List[Agent]:
        return self.agents

registry = AgentRegistry()
