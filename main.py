from fastapi import FastAPI
from fastapi.responses import FileResponse

from agents.agent import Agent
from core.registry import registry
from core.privatevault import verify_agent
from core.lork import execute_collaboration
from graph.agent_graph import agent_graph
from plugins.manager import plugin_manager

app = FastAPI(title="BotBook")

@app.get("/")
def root():
    return {"message": "BotBook Agent Network"}

@app.get("/network")
def network_ui():
    return FileResponse("web/network.html")

@app.post("/agents/register")
def register_agent(agent: Agent):

    verification = verify_agent(agent.name)

    registry.register(agent)

    plugin_manager.trigger_register(agent)

    return {
        "agent": agent,
        "verification": verification
    }

@app.get("/agents")
def list_agents():
    return registry.list_agents()

@app.post("/agents/collaborate")
def collaborate(agent_a: str, agent_b: str, task: str):

    result = execute_collaboration(agent_a, agent_b, task)

    plugin_manager.trigger_collaboration(agent_a, agent_b, task)

    return result

@app.get("/graph")
def agent_network():
    return agent_graph.export()
