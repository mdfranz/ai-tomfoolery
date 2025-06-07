#!/usr/bin/env python

from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini

simple_agent = Agent(
    model=Gemini(id="gemini-2.5-pro-exp-03-25"),
    markdown=True, debug_mode=True,
    add_history_to_messages=True,
    instructions=dedent("""\
        You are a playful and creative security practioner with a knack for making the most boring topics interesting and exciting
    """)
)

if __name__ == "__main__":
    simple_agent.print_response("Create a threat model for an iPhone.", stream=True)
