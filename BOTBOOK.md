# BotBook

> **The Operating System for AI Agents**

BotBook is the runtime fabric for deploying, connecting, and managing autonomous AI agents. It provides the agent graph, memory, plugin system, network layer, and protocol primitives that production agent systems are built on — the foundation that PrivateVault and LORK sit on top of.

---

## Install

```bash
pip install botbook
Quickstart
Start the server
botbook start

Server runs at http://localhost:8000

Create a project
botbook init
Dev mode (hot reload)
botbook dev
Architecture

BotBook separates agent definition from agent execution.

Application
     │
     ▼
BotBook Runtime
     │
     ├── Agent Graph
     ├── Memory
     ├── Plugin System
     ├── Network Layer
     ├── Protocol
     └── Audit Log
     │
     ▼
Agents
     │
     ▼
Tools / APIs / LLMs
Core Concepts
Agent Graph

Agents are nodes in a directed graph. Defines routing, dependencies, and execution paths.

Memory

Scoped memory per agent with support for shared context across workflows.

Plugins

Extensible tools layer (APIs, DBs, SaaS integrations).

Network Layer

Handles communication, routing, and coordination across agents.

Protocol

Standardized agent-to-agent communication.

Audit Log

Append-only execution log of all agent actions.

Pipelines
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
botbook run fintech_pipeline.yaml
Repository Layout
botbook/
agents/
api/
core/
graph/
memory/
network/
plugins/
protocol/
deployments/
docs/
runs/
web/
Integrations

PrivateVault → governance layer

LORK → observability + replay

Envoy → network interception

Vault → secrets

Positioning

BotBook is not a framework.

It is:
👉 The runtime operating system for AI agents

Development
git clone https://github.com/LOLA0786/botbook.dev
cd botbook.dev
pip install -e ".[dev]"
pytest
botbook dev
License

See LICENSE.
