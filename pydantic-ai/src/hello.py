import logging,os
from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel

logging.basicConfig(level=logging.DEBUG)

for m in ['phi3:3.8b','hermes3:latest', 'llama3.2','mistral:latest','gemma2:9b']:
    om = OllamaModel(model_name=m,base_url='http://'+os.environ['OLLAMA_HOST'] + '/v1')
    agent = Agent(model=om, system_prompt='Be verbose, reply with at least 3 sentences with elaboration')
    result = agent.run_sync('Where does "hello world" come from?')
    print(result.data)
    print(result.usage())
