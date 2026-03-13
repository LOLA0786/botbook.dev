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

@app.post("/agents/publish")
def publish_agent(agent: Agent):

    verification = verify_agent(agent.name)

    if verification["verified"]:
        agent.verified = True

    registry.register(agent)

    plugin_manager.trigger_register(agent)

    return {
        "agent": agent,
        "verification": verification
    }

@app.get("/agents")
def list_agents():
    return registry.list_agents()

@app.get("/agents/search")
def search_agents(capability: str):
    return registry.search(capability)

@app.post("/agents/collaborate")
def collaborate(agent_a: str, agent_b: str, task: str):

    result = execute_collaboration(agent_a, agent_b, task)

    plugin_manager.trigger_collaboration(agent_a, agent_b, task)

    return result

@app.get("/graph")
def agent_network():
    return agent_graph.export()

from protocol.router import initiate_handshake, send_message
from protocol.handshake import manager

@app.post("/protocol/handshake")
def start_handshake(agent_a: str, agent_b: str, task: str):
    return initiate_handshake(agent_a, agent_b, task)

@app.post("/protocol/message")
def route_message(session_id: str, sender: str, content: str):
    return send_message(session_id, sender, content)

@app.get("/protocol/sessions")
def list_sessions():
    return manager.list_sessions()

from core.capability_index import capability_index

@app.get("/search")
def search_capability(capability: str):
    return {
        "capability": capability,
        "agents": capability_index.search(capability)
    }


from core.reputation import reputation

@app.get("/reputation")
def reputation_score(agent: str):
    return {
        "agent": agent,
        "score": reputation.get(agent)
    }


from fastapi import WebSocket

connections = []

@app.websocket("/ws")

async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            for c in connections:
                await c.send_text(data)

    except:
        connections.remove(websocket)


from core.workflow import workflow_engine

@app.post("/workflow")

def run_workflow(agents: list[str], task: str):
    return workflow_engine.run(agents, task)


from core.marketplace import marketplace

@app.post("/marketplace/publish")

def publish_service(agent: str, capability: str, price: float):
    return marketplace.publish(agent, capability, price)

@app.get("/marketplace")

def list_marketplace():
    return marketplace.list()

