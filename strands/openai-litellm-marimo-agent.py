import marimo

__generated_with = "0.16.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import os
    from datetime import datetime
    from datetime import timezone as tz
    from typing import Any
    from zoneinfo import ZoneInfo

    from strands import Agent, tool
    from strands.models.litellm import LiteLLMModel
    return Agent, Any, LiteLLMModel, ZoneInfo, datetime, mo, tool, tz


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Setting up custom tools

    Let's now setup two dummy tools to test our agent
    """
    )
    return


@app.cell
def _(Any, ZoneInfo, datetime, tool, tz):
    @tool
    def current_time(timezone: str = "UTC") -> str:
        if timezone.upper() == "UTC":
            timezone_obj: Any = tz.utc
        else:
            timezone_obj = ZoneInfo(timezone)

        return datetime.now(timezone_obj).isoformat()


    @tool
    def current_weather(city: str) -> str:
        # Dummy implementation. Please replace with actual weather API call.
        return "sunny"
    return current_time, current_weather


@app.cell
def _(LiteLLMModel):
    model = "openai/gpt-4.1-mini"
    litellm_model = LiteLLMModel(
        model_id=model, params={"max_tokens": 32000, "temperature": 0.7}
    )
    return (litellm_model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Defining Agent

    Now that we have all the required information available, let's define our agent
    """
    )
    return


@app.cell
def _(Agent, current_time, current_weather, litellm_model):
    system_prompt = "You are a simple agent that can tell the time and the weather"
    agent = Agent(
        model=litellm_model,
        system_prompt=system_prompt,
        tools=[current_time, current_weather],
    )
    return (agent,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Testing agent

    Let's now invoke the agent to test it
    """
    )
    return


@app.cell
def _(agent):
    results = agent("What time is it in Kuala Lumpur Malaysia? And how is the weather?")
    return (results,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    #### Analysing the agent's results

    Nice! We've invoked our agent for the first time! Let's now explore the results object. First thing we can see is the messages being exchanged by the agent in the agent's object
    """
    )
    return


@app.cell
def _(agent):
    agent.messages
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Next we can take a look at the usage of our agent for the last query by analysing the result `metrics`""")
    return


@app.cell
def _(results):
    results.metrics
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Congratulations!

    In this notebook you learned how to use LiteLLM with OpeanAi serving answers for weather agent.
    """
    )
    return


if __name__ == "__main__":
    app.run()
