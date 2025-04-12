from agno.agent import Agent, RunResponse 
from agno.models.ollama import Ollama
from agno.vectordb.qdrant import Qdrant
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader


COLLECTION_NAME = "pdf-reader"

vector_db = Qdrant(collection=COLLECTION_NAME, url="http://http://100.120.208.61:6333/")

kb = PDFKnowledgeBase(
    path="/home/mfranz/tmp/pdf/FedRAMP_Collaborative_ConMon_Quick_Guide.pdf",
    vector_db=vector_db,
    reader=PDFReader(chunk=True)
)

kb.load(recreate=True)

#
# The following have tools, but return ollama template only
# phi4-mini:3.8b, granite3.2:8b
# 
# works: mistral-nemo:12b, cogito:14b, llama3.2, qwen2.5:14b, hermes3:8b (very different response) 
#
# Didn't use KB: command-r7b:7b
#
# Used KB, but Didn't return results; nemotron-mini:4b
#

agent = Agent(knowledge=kb,model=Ollama(id='mistral-nemo:12b'), markdown=False,telemetry=False,debug_mode=True)

agent.print_response("What is ConMon?")
