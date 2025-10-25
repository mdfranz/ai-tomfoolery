from agno.agent import Agent, RunOutput
from agno.models.ollama import Ollama

ollama_models = [
    "cogito:8b",
    "cogito:14b",
    "cogito:3b",
    "phi4-mini:3.8b",
    "phi4:14b",
]

for m in ollama_models:
    agent = Agent(model=Ollama(id=m), markdown=False, telemetry=True, debug_mode=True)
    resp: RunOutput = agent.run(
        "Write a bash shell script that calls the AWS cli to retrieve all the running instances in all regions. Do not print the results for regions where there are no instances running"
    )
    print(resp.content)
