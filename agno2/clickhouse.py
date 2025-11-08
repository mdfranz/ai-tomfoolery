import asyncio
from agno.agent import Agent
from agno.tools.mcp import MCPTools
from agno.models.anthropic import Claude


env = {
    "CLICKHOUSE_HOST": "sql-clickhouse.clickhouse.com",
    "CLICKHOUSE_PORT": "8443",
    "CLICKHOUSE_USER": "demo",
    "CLICKHOUSE_PASSWORD": "",
    "CLICKHOUSE_SECURE": "true"
}

async def main():
    async with MCPTools(command="uv run --with mcp-clickhouse mcp-clickhouse", env=env, timeout_seconds=60) as mcp_tools:
        agent = Agent(
            model=Claude(id="claude-sonnet-4-20250514"),
            debug_mode=True,
            markdown=True,
            tools = [mcp_tools]
        )
        await agent.aprint_response("What's the most starred project in 2025?", stream=True)

if __name__ == "__main__":
    asyncio.run(main())
