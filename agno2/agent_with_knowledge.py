import asyncio

from agno.agent import Agent, RunOutput
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.ollama import Ollama
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.lancedb import LanceDb, SearchType

# Load Agno documentation into Knowledge

ollama_inferencing_models = [
    "llama3.1:8b",
    "qwen3:14b",
    "cogito:14b",
    "granite4:micro",
    "granite4",
    "gpt-oss:20b",
]

if __name__ == "__main__":
    knowledge = Knowledge(
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="agno_docs",
            search_type=SearchType.hybrid,
            # Use OpenAI for embeddings
            embedder=OpenAIEmbedder(id="text-embedding-3-small", dimensions=1536),
        ),
    )

    asyncio.run(
        knowledge.add_content_async(
            name="Agno Docs",
            url="https://raw.githubusercontent.com/agno-agi/agno-docs/refs/heads/main/concepts/agents/overview.mdx",
        )
    )

    for m in ollama_inferencing_models:
        print(f"\n\n\nTESTING {m} ")
        agent = Agent(
            name="Agno Assist",
            model=Ollama(id=m),
            instructions=[
                "Use tables to display data.",
                "Include sources in your response.",
                "Search your knowledge before answering the question.",
                "Only include the output in your response. No other text.",
            ],
            knowledge=knowledge,
            tools=[ReasoningTools(add_instructions=True)],
            add_datetime_to_context=True,
            markdown=True,
            debug_mode=True,
        )

        try:
            agent.print_response(
                "What are Agents?",
                stream=True,
                show_full_reasoning=True,
                stream_events=True,
            )
        except Exception as e:
            print(f"An error occurred for model {m}: {e}")
