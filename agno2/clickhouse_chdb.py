import asyncio

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools

#
# uv run --with mcp-clickhouse mcp-clickhouse
# export CLICKHOUSE_ENABLED=false
# export CHDB_DATA_PATH=data
# export CHDB_ENABLED=true
# export CLICKHOUSE_MCP_SERVER_TRANSPORT=http
#


async def main(data_question):
    async with MCPTools(
        transport="streamable-http",
        url="http://127.0.0.1:8000/mcp",
        timeout_seconds=60,
    ) as mcp_tools:
        agent = Agent(
            model=Claude(id="claude-sonnet-4-20250514"),
            debug_mode=True,
            markdown=True,
            tools=[mcp_tools],
        )
        await agent.aprint_response(data_question, stream=True)


if __name__ == "__main__":
    prompt = input("What do you want to know? ")
    asyncio.run(main(prompt))
