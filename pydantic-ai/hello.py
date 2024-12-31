from pydantic_ai import Agent
import logging

# import logfire
# logfire.configure()  
# logfire.info('Hello, {name}!', name='world')

logging.basicConfig(level=logging.DEBUG)

for m in ['ollama:phi3:3.8b','ollama:hermes3:latest', 'ollama:llama3.2','ollama:mistral:latest','ollama:gemma2:9b']:
    agent = Agent(m, system_prompt='Be verbose, reply with at least 3 sentences with elaboration')
    result = agent.run_sync('Where does "hello world" come from?')
    print(result.data)
    print(result.usage())
