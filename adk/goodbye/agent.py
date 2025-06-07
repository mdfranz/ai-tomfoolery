from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(name="chef",instruction="be useful",description="do stuff",model=LiteLlm(model='ollama_chat/nemotron-mini:4b'))
