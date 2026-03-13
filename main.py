from fastapi import FastAPI
from agents.agent import Agent
from core.registry import registry
from core.privatevault import verify_agent
from network.broadcast import broadcaster

app = FastAPI(title="BotBook")

@app.post("/agents/publish")

def publish_agent(agent: Agent):

    verification = verify_agent(agent.name)

    if verification["verified"]:
        agent.verified = True

    registry.register(agent)

    return {
        "agent": agent,
        "verification": verification
    }

@app.post("/node/connect")

def connect_node(url: str):

    broadcaster.add_peer(url)

    return {"status": "connected", "peer": url}

@app.get("/agents")

def list_agents():
    return registry.list_agents()
