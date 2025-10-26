import sys
from agno.agent import Agent, RunOutput
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.ollama import Ollama
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.vectordb.chroma import ChromaDb

ollama_inferencing_models = [
    "llama3.1:8b",
    "qwen3:14b",
    "granite4:micro",
    "granite4",
    "cogito:8b",
    "cogito:14b",
    "gpt-oss:20b",
]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("foo.py <chromadb|lancedb>")
        sys.exit(-1)

    if sys.argv[1] == "lancedb":
        knowledge = Knowledge(
            vector_db=LanceDb(
                uri="tmp/lancedb",
                table_name="agno_docs",
                search_type=SearchType.hybrid,
                embedder=OpenAIEmbedder(id="text-embedding-3-small", dimensions=1536),
            ),
        )
    elif sys.argv[1] == "chromadb":
        knowledge = Knowledge(
            vector_db=ChromaDb(
                collection="vectors",
                path="tmp/chromadb",
                persistent_client=True,
                embedder=OpenAIEmbedder(id="text-embedding-3-small", dimensions=1536),
            ),
        )

    knowledge.add_content(name="Job Description", path="ai-cloud-security-engineer.md")

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
            add_datetime_to_context=False,
            markdown=True,
            debug_mode=True,
        )

        try:
            agent.print_response(
                "What do I need to succeed in the Cloud AI Security Engineer role",
                stream=True,
                show_full_reasoning=True,
                stream_events=True,
            )
        except Exception as e:
            print(f"An error occurred for model {m}: {e}")
