from botbook.api.nodes import router as nodes_router
from botbook.api.events import router as events_router
from botbook.api.capabilities import router as capability_router
from botbook.api.agent_dns import router as agent_dns_router
from botbook.api.jobs import router as jobs_router
from botbook.api.contracts import router as contracts_router
from botbook.api.contracts import router as contracts_router
from botbook.network.graph_api import router as network_router
from botbook.api.trust_routes import router as trust_router
"""
BotBook — main entrypoint
Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

import logging
import uvicorn
from botbook.api.routes import app


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1,
        log_level="info",
    )

app.include_router(network_router)
app.include_router(trust_router)
app.include_router(jobs_router)
app.include_router(contracts_router)

from botbook.api.agent_run import router as agent_run_router
app.include_router(agent_run_router)

from botbook.api.tools import router as tools_router
from botbook.tools.load_tools import *

app.include_router(tools_router)

from botbook.api.agent_rpc import router as agent_rpc_router
app.include_router(agent_rpc_router)
app.include_router(agent_dns_router)
app.include_router(capability_router)
app.include_router(events_router)
app.include_router(nodes_router)
