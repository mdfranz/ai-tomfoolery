#!/usr/bin/env python3

import logging,os
from pydantic import BaseModel

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

#logging.basicConfig(level=logging.DEBUG)

for m in ['hermes3:latest', 'llama3.2','mistral:latest','gemma3:12b','phi4:14b']:
    print(f'\n\n\nUsing model: {m}')

    om = OpenAIModel(model_name=m,provider=OpenAIProvider(base_url=f"{ os.environ['OLLAMA_HOST'] }/v1"))
    agent = Agent(model=om, instructions='Be verbose, reply with at least 3 sentences with elaboration')

    result = agent.run_sync('Where does "hello world" come from?')
    print(result.output)
    print(result.all_messages())
    print(result.usage())
