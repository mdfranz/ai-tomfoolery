#!/usr/bin/env python

from agno.agent import Agent, RunResponse  # noqa
from agno.models.ollama import Ollama

ollama_models = ['cogito:14b', 'qwen2.5:14b', 'mistral-nemo:12b','granite4:micro','granite4:tiny-h','gpt-oss:20b']

for m in ollama_models:
    agent = Agent(model=Ollama(id=m), markdown=False,telemetry=True,debug_mode=True)
    resp = agent.run("Write a bash shell script that calls the AWS cli to retrieve all the running instances in all regions. Do not print the results for regions where there are no instances running. Do not comment the script. Prioritize clarity over cleverness")
    print(resp.content)
