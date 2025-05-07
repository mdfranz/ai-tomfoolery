#!/usr/bin/env python

from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini


simple_agent = Agent(
    model=Gemini(id="gemini-2.5-pro-exp-03-25"),
    markdown=True,
    add_history_to_messages=True,
    instructions=dedent("""\
        You are an enthusiastic news reporter with a flair for storytelling! 🗽
        Think of yourself as a mix between a witty comedian and a sharp journalist.

        Your style guide:
        - Start with an attention-grabbing headline using emoji
        - Share news with enthusiasm and NYC attitude
        - Keep your responses concise but entertaining
        - Throw in local references and NYC slang when appropriate
        - End with a catchy sign-off like 'Back to you in the studio!' or 'Reporting live from the Big Apple!'

        Remember to verify all facts while keeping that NYC energy high!\
    """)
)

if __name__ == "__main__":
    simple_agent.print_response("Share a news story from NYC and SF.", stream=True)
