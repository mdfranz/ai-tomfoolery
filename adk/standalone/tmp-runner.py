import asyncio
import logging

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# Configure logging
# logging.basicConfig( level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s" )
#
# See https://github.com/koverholt/adk-runtime-example
#

APP_NAME = "ollama"
USER_ID = "user"
SESSION_ID = "session"
MODEL_IDS = [
    "ollama/granite4:latest",
    "ollama/cogito:14b",
    "ollama/granite4:micro",
    "ollama/granite4:tiny-h",
]


def create_agent(model_id: str) -> Agent:
    return Agent(
        name=model_id.replace("/", "").replace(":", "").replace("-", ""),
        model=LiteLlm(model=model_id),
        description=f"Agent for {model_id}",
        instruction="""
           You are a silly 3rd grader that says inappropriate things all the time
        """,
    )


def create_runner(model_id: str) -> InMemoryRunner:
    agent = create_agent(model_id)
    return InMemoryRunner(
        agent=agent,
        app_name=APP_NAME,
    )


def create_session(runner: InMemoryRunner):
    session = asyncio.run(
        runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    )
    return session


def query_agent(runner: InMemoryRunner, prompt: str, session_id: str):
    """Query the agent with the given prompt."""
    print("** User:", prompt)

    response = runner.run(
        new_message=types.Content(role="user", parts=[types.Part(text=prompt)]),
        user_id=USER_ID,
        session_id=session_id,
    )

    for message in response:
        if message.content.parts and message.content.parts[0].text:
            print(f"** {message.author}: {message.content.parts[0].text}\n")


if __name__ == "__main__":
    # Iterate through each model
    for model_id in MODEL_IDS:
        print(f"\n{'=' * 60}")
        print(f"Testing model: {model_id}")
        print(f"{'=' * 60}\n")

        # Create runner for this model
        runner = create_runner(model_id)

        # Create session
        session = create_session(runner)

        # Query the agent
        query_agent(runner, "Tell me a joke", session_id=session.id)
        query_agent(runner, "Tell me a story", session_id=session.id)
