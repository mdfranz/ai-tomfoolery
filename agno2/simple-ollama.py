import json
import datetime
from agno.agent import Agent, RunOutput
from agno.models.ollama import Ollama

ollama_models = [
    "cogito:8b",
    "cogito:14b",
    "phi4-mini:3.8b",
    "phi4:14b",
    "granite4:micro",
    "granite4",
    "granite3.2:8b",
    "gemma3n:e2b",
    "gemma3n:e4b",
    "gemma3:latest",
    "gemma3n:latest",
    "gemma3:12b",
]

if __name__ == "__main__":
    results = {}
    for m in ollama_models:
        agent = Agent(
            model=Ollama(id=m), markdown=False, telemetry=True, debug_mode=True
        )
        resp: RunOutput = agent.run(
            "Write a bash shell script that calls the AWS cli to retrieve all the running instances in all regions. Do not print the results for regions where there are no instances running"
        )
        results[m] = resp.content

    now = datetime.datetime.now()
    timestamp_suffix = now.strftime("%y%m%d%H%M")
    filename = f"model_outputs_{timestamp_suffix}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
