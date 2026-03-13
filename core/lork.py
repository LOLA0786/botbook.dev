from graph.agent_graph import agent_graph

def execute_collaboration(agent_a, agent_b, task):
    """
    Simulated LORK orchestration layer
    """

    agent_graph.add_collaboration(agent_a, agent_b, task)

    return {
        "status": "executed",
        "agent_a": agent_a,
        "agent_b": agent_b,
        "task": task
    }
