from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(name="fish",instruction="be useful",description="do stuff",model=LiteLlm(model='ollama_chat/qwen2.5:7b'))
