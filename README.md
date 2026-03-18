# BotBook

 

> **The Operating System for AI Agents**

BotBook is the runtime fabric for deploying, connecting, and managing autonomous AI agents. It provides the agent graph, memory, plugin system, network layer, and protocol primitives that production agent systems are built on — the foundation that PrivateVault and LORK sit on top of.

---

## Install

```bash
pip install botbook
```

---

## Quickstart

### Start the server

```bash
botbook start
```

Server runs at `http://localhost:8000`

### Create a project

```bash
botbook init
```

### Dev mode (hot reload)

```bash
botbook dev
```

---

## Architecture

BotBook separates agent definition from agent execution. The agent graph manages relationships and routing between agents. The runtime handles execution, memory, and tool dispatch.

```
Application
     │
     ▼
BotBook Runtime
     │
     ├── Agent Graph       (topology, routing, relationships)
     ├── Memory            (per-agent and shared memory stores)
     ├── Plugin System     (tools, connectors, capabilities)
     ├── Network Layer     (inter-agent messaging and coordination)
     ├── Protocol          (agent communication standards)
     └── Audit Log         (execution record for every agent action)
     │
     ▼
Agents
     │
     ▼
Tools / APIs / LLMs
```

---

## Core Concepts

### Agent Graph
Agents are nodes in a directed graph. BotBook manages the topology — which agents can call which other agents, how data flows between them, and how failures propagate. Define complex multi-agent systems declaratively.

### Memory
Each agent has access to a memory store scoped to its identity. Memory persists across turns within a run and can be shared across agents within the same graph. Supports short-term (run-scoped) and long-term (persistent) memory.

### Plugins
Extend any agent with tools and connectors via the plugin system. Plugins are declared per-agent and versioned independently of the agent graph. Built-in plugins cover HTTP, databases, file I/O, and common SaaS integrations.

### Network Layer
BotBook handles inter-agent communication — routing messages between agents, managing fan-out and aggregation, and enforcing communication boundaries defined in the agent graph.

### Protocol
BotBook defines a standard protocol for agent-to-agent messaging. This means agents built on different model providers can be composed into the same graph without custom integration code.

### Audit Log
Every agent action is written to an append-only audit log (`audit.log`). When paired with PrivateVault, this log is Merkle-hashed and governance-enforced at the runtime layer.

---

## Pipelines

BotBook supports declarative pipeline definitions for common agent workflows:

```yaml
# fintech_pipeline.yaml
name: loan_review
agents:
  - id: intake_agent
    plugins: [document_reader, kyc_connector]
  - id: risk_agent
    plugins: [credit_model, fraud_detector]
  - id: decision_agent
    plugins: [approval_store, notification]
graph:
  - intake_agent -> risk_agent
  - risk_agent -> decision_agent
```

```bash
botbook run fintech_pipeline.yaml
```

---

## Repository Layout

```
botbook/        Core runtime (agent graph, memory, protocol, network)
agents/         Agent execution logic and base classes
api/            REST API server
core/           Shared primitives and utilities
graph/          Agent graph implementation
memory/         Memory store implementations
network/        Inter-agent network layer
plugins/        Plugin registry and built-in plugins
protocol/       Agent communication protocol
deployments/    Container and cloud deployment configs
docs/           Architecture and integration guides
runs/           Run history (local dev)
web/            Web UI
```

---

## Integrations

BotBook is designed to compose with the rest of the stack:

| Integration | What it provides |
|---|---|
| **PrivateVault** | Runtime governance — every agent action policy-evaluated before execution |
| **LORK** | Observability — event-sourced run history, replay, and time-travel debugging |
| **Envoy** | Proxy interception for network-level governance |
| **HashiCorp Vault** | Secrets management for agent credentials and API keys |

---

## Development

```bash
# Clone
git clone https://github.com/LOLA0786/botbook.dev
cd botbook.dev

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Start in dev mode
botbook dev
```

---

## License

See [LICENSE](LICENSE).
