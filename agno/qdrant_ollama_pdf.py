#!/usr/bin/env python

#
# Assumes
# OLLAMA_HOST, QDRANT_HOST
#

import os, platform, sys

from agno.agent import Agent, RunResponse
from agno.models.ollama import Ollama
from agno.vectordb.qdrant import Qdrant
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase,PDFUrlReader
from agno.embedder.ollama import OllamaEmbedder
from agno.embedder.fastembed import FastEmbedEmbedder

# What I've tested OllamaEmbedder, FastEmbedEmbedder

if __name__ == "__main__":

    if len(sys.argv) > 1:
        COLLECTION_NAME = f"pdf-reader-{platform.node()}-{sys.argv[1]}"
        if sys.argv[1] == "ollama":
            vector_db = Qdrant(collection=COLLECTION_NAME, url=os.environ.get('QDRANT_HOST'),embedder=OllamaEmbedder())
        elif sys.argv[1] == "fastembed":
            vector_db = Qdrant(collection=COLLECTION_NAME, url=os.environ.get('QDRANT_HOST'),embedder=FastEmbedEmbedder())
    else:
        COLLECTION_NAME = f"pdf-reader-{platform.node()}-openai"
        vector_db = Qdrant(collection=COLLECTION_NAME, url=os.environ.get('QDRANT_HOST'))

    kb = PDFUrlKnowledgeBase(
        urls = ['https://www.fedramp.gov/assets/resources/documents/FedRAMP_Collaborative_ConMon_Quick_Guide.pdf',
                'https://www.fedramp.gov/assets/resources/documents/CSP_Incident_Communications_Procedures.pdf',
                'https://www.fedramp.gov/assets/resources/documents/CSP_Vulnerability_Scanning_Requirements.pdf',
                'https://www.fedramp.gov/assets/resources/documents/CSP_Continuous_Monitoring_Performance_Management_Guide.pdf'
        ],
        vector_db=vector_db,
    )

    kb.load(recreate=True)

    useful_models = ['cogito:14b', 'qwen2.5:14b', 'mistral-nemo:12b','hermes3:8b','qwen2.5:7b','cogito:8b','llama3.2:3b','cogito:3b']

    for m in useful_models:
        print (f"\n\nRunning {m}")

        agent = Agent(knowledge=kb,model=Ollama(id=m), exponential_backoff=True, markdown=True,telemetry=False,debug_mode=False,
            description="You are a season FedRAMP compliance analyst with in depth experience with the NIST 800-53 framework and operational security monitoring tools in AWS GovCloud", instructions=['You have an important briefing with the CISO and Product Manager and you must impress them with your knowledge and experience so they provide the necessary funding for tools and headcount']
        )
        agent.print_response("1) Define continous monitoring  2) Explain the three most important steps (in order) to implement a continous monitoring program.  For each step identify the NIST 800-53 control (or controls) that are relevant to ensure you can pass your annual assessment and achieve monthly reporting goals")
