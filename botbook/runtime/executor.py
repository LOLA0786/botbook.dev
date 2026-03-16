import importlib

from botbook.runtime.memory import write
from botbook.runtime.llm import generate

def run(agent_name, task):

    module = importlib.import_module(f"agents.{agent_name}")

    agent = module.Agent()

    print("\n⚡ Running agent:", agent.name)

    prompt = f"{agent.role}\nTask: {task}"

    result = generate(prompt)

    write(agent.name, task, result)

    print("\nResult:", result)

    return result
