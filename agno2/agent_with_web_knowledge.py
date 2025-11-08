import sys, time, datetime
from agno.agent import Agent, RunOutput
from agno.models.ollama import Ollama
from agno.models.google import Gemini


from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.website_reader import WebsiteReader

from agno.tools.reasoning import ReasoningTools
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.vectordb.chroma import ChromaDb
from agno.db.sqlite.sqlite import SqliteDb
from agno.vectordb.qdrant import Qdrant

ollama_tool_models = [
    "llama3.1:8b",
    # "phi4-mini:3.8b",
    "granite4:micro",
    # "granite4",
    # "cogito:8b",
    "qwen3:14b",
    "cogito:14b",
    # "gpt-oss:20b",
]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("foo.py <chromadb|lancedb> [openai|fastembed|openhermes")
        sys.exit(-1)

    memory_db = SqliteDb(db_file="agno-memory.db")
    contents_db = SqliteDb(db_file="my_knowledge.db")

    timestamp_str = datetime.datetime.now().strftime("%y%m%d%M")

    if len(sys.argv) == 3:
        if sys.argv[2] == "gemini":
            my_embedder = GeminiEmbedder()
        elif sys.argv[2] == "openhermes":
            my_embedder = OllamaEmbedder(id="openhermes", dimensions=4096)
        elif sys.argv[2] == "qwen3":
            my_embedder = OllamaEmbedder(id="qwen3-embedding:8b")
    else:
        my_embedder = OpenAIEmbedder(id="text-embedding-3-small", dimensions=1536)

    print(f"Using embedder: {my_embedder}\n")

    # Choose Vector Database
    if sys.argv[1] == "lancedb":
        vdb = LanceDb(
            name="Lance Job Description",
            uri="tmp/lancedb",
            table_name="agno_docs",
            search_type=SearchType.hybrid,
            embedder=my_embedder,
        )
    elif sys.argv[1] == "chromadb":
        vdb = ChromaDb(
            name="Chroma Job Description",
            collection="vectors",
            path="tmp/chromadb",
            persistent_client=True,
            embedder=my_embedder,
        )
    elif sys.argv[1] == "qdrant":
        vdb = Qdrant(
            name="Qdrant Job Description",
            collection=f"vectors-{timestamp_str}",
            url="http://localhost:6333",
            embedder=my_embedder,
        )

    knowledge = Knowledge(vector_db=vdb, contents_db=contents_db)
    knowledge.add_content(name="Job Description", path="ai-cloud-security-engineer.md")
    knowledge.add_content(
        name="Bespin Services",
        url="https://bespinglobal.us/managed-security",
        reader=WebsiteReader(),
    )
    print(f"Using knowledge: {knowledge}")

    print("Starting with API Models")
    agent = Agent(
        name=f"Agno Assist Gemini",
        model=Gemini(id="gemini-2.5-pro"),
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
        debug_mode=False,
        db=memory_db,
        add_history_to_context=False,
        num_history_runs=3,
    )
    try:
        agent.print_response(
            "I am applying for the  Cloud AI Security Engineer role in Bespin Managed Security Services. Use the provided job description and information from the Bespin Services and I want know if I will be succesful in this role. Also use information about Bespin Managed Services to craft the list of success criteria",
            stream=True,
            show_full_reasoning=True,
            stream_events=True,
        )
    except Exception as e:
        print(f"An error occurred for model {e}")

    # Evaluate the different models
    for m in ollama_tool_models:
        print(f"\n\n\nTESTING {m} ")
        agent = Agent(
            name=f"Agno Assist {m}",
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
            debug_mode=False,
            db=memory_db,
            add_history_to_context=False,
            num_history_runs=3,
        )

        try:
            agent.print_response(
                "I am applying for the  Cloud AI Security Engineer role in Bespin Managed Security Services. Use the provided job description and information from the Bespin Services and I want know if I will be succesful in this role. Also use information about Bespin Managed Services to craft the list of success criteria",
                stream=True,
                show_full_reasoning=True,
                stream_events=True,
            )
        except Exception as e:
            print(f"An error occurred for model {m}: {e}")
        time.sleep(2)
