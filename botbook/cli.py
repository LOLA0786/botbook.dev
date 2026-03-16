import subprocess
import sys

from botbook.agent_scaffold import create_agent
from botbook.runtime.executor import run as run_agent
from botbook.runtime.memory import history

VERSION="0.1.0"

def banner():
    print("")
    print("🚀 BotBook — AI Agent Runtime")
    print("Version:", VERSION)
    print("")

def start():
    banner()
    subprocess.run(
        ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
    )

def make():
    if len(sys.argv)<3:
        print("Usage: botbook make <agent>")
        return

    create_agent(sys.argv[2])

def run():

    if len(sys.argv)<4:
        print("Usage: botbook run <agent> <task>")
        return

    agent=sys.argv[2]
    task=" ".join(sys.argv[3:])

    run_agent(agent,task)

def runs():

    for r in history():
        print(r)

def help():

    print("""

BotBook CLI

botbook start

botbook make <agent>

botbook run <agent> "<task>"

botbook runs

""")

def main():

    if len(sys.argv)<2:
        help()
        return

    cmd=sys.argv[1]

    if cmd=="start":
        start()

    elif cmd=="make":
        make()

    elif cmd=="run":
        run()

    elif cmd=="runs":
        runs()

    else:
        help()

if __name__=="__main__":
    main()
