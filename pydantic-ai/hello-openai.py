#!/usr/bin/env python3

import logging,os
from pydantic import BaseModel
from openai import OpenAI

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

#logging.basicConfig(level=logging.DEBUG)

client = OpenAI()
models = client.models.list().data

non_text_keywords = [
        'image',
        'vision',
        'embed',
        'audio',
        'speech',
        'whisper',
        'dall-e',
        'moderation',
        'codex'
    ]

models_id = [m.id for m in models]    

for m in models_id:
    try:
        print(f'\n\n\nUsing model: {m}')
        if any(keyword in m for keyword in non_text_keywords):
            print(f'Skipping model {m} as it is not a text model.')
            continue

        om = OpenAIModel(model_name=m)
        agent = Agent(model=om, instructions='Be verbose, reply with at least 3 sentences with elaboration')

        result = agent.run_sync('Where does "hello world" come from?')
        print(result.output)
        print(result.all_messages())
        print(result.usage())
    except Exception as e:
        print(f'Error with model {m}: {e}')
        continue
