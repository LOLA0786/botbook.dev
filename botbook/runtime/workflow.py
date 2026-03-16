import yaml
from botbook.runtime.executor import run

def run_workflow(file_path, task):

    with open(file_path) as f:
        config = yaml.safe_load(f)

    steps = config.get("steps", [])

    context = task

    for agent in steps:

        print("\n====================")
        print("Running agent:", agent)
        print("====================")

        result = run(agent, context)

        context = result

    print("\nWorkflow complete")

    return context
