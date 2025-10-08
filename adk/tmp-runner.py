from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

#
# See https://github.com/koverholt/adk-runtime-example
#

APP_NAME = "ollama"
USER_ID = "user"
SESSION_ID = "session"
MODEL_ID = "ollama/granite4:latest"

dumb_ollama_agent = Agent(
    name="dumb",
    model=LiteLlm(model=MODEL_ID),
    description="Dumb Dumb",
    instruction="""
        Do something really stupid for me
    """,
)

runner = InMemoryRunner(
    agent=dumb_ollama_agent,
    app_name=APP_NAME,
)


def create_session():
    session = asyncio.run(
        runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    )
    return session


# Define a convenience function to query the agent
def query_agent(prompt: str, session_id: str):
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
    session = create_session()
    query_agent("Hello!", session_id=session.id)
    query_agent("Who are you", session_id=session.id)
    query_agent("What do you stand for", session_id=session.id)
