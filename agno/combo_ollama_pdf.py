#!/usr/bin/env python

#
# Assumes
# OLLAMA_HOST, QDRANT_HOST
#

import os, platform, sys, argparse

from agno.agent import Agent, RunResponse
from agno.models.ollama import Ollama

# VectorDBs
from agno.vectordb.qdrant import Qdrant
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.chroma import ChromaDb

# Documents formats
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase,PDFUrlReader

# Supported Embedders
from agno.embedder.ollama import OllamaEmbedder
from agno.embedder.fastembed import FastEmbedEmbedder
from agno.embedder.openai import OpenAIEmbedder

def create_vdb(name="pdf",engine='qdrant',embedder='ollama'):
    # Select embedder
    kb_name = f"{name}-{embedder}-{platform.node()}"

    if embedder == 'ollama':
        agno_embedder =  OllamaEmbedder() 
    elif embedder == 'fastembed':
        agno_embedder =  FastEmbedEmbedder()
    elif embedder == 'openai':
        agno_embedder = OpenAIEmbedder()

    print (f"Embedder: {embedder}")
    print (f"VectorDB: {engine}")

    if engine == 'qdrant':
        return Qdrant(collection=kb_name, url=os.environ.get('QDRANT_HOST'), embedder=agno_embedder)
    elif engine == 'chromadb':
        return ChromaDb(collection=kb_name, path="/tmp/chromadb", persistent_client=True, embedder=agno_embedder)
    elif engine == 'lancedbb':
        return LanceDb(table_name=kb_name, uri="/tmp/lancedb", search_type=SearchType.keyword,embedder=agno_embedder)

def create_kb(vdb,doclist,recreate=True):
    kb =  PDFUrlKnowledgeBase(urls=doclist,vector_db=vdb)
    kb.load(recreate=recreate)
    return kb

if __name__ == "__main__":
    urls = [ 'https://www.fedramp.gov/resources/documents/FedRAMP_Collaborative_ConMon_Quick_Guide.pdf']

    parser = argparse.ArgumentParser(description="Run an agent with different models and vector databases.")
    parser.add_argument("--engine", type=str, default="chromadb", choices=["qdrant", "chromadb", "lancedb"], help="Vector database engine to use.")
    parser.add_argument("--embedder", type=str, default="ollama", choices=["ollama", "fastembed","openai"], help="Embedder to use.")
    parser.add_argument("--model", type=str, default=None, help="Ollama model to use. If not provided, iterates through a predefined list.")
   
    args = parser.parse_args()

    useful_models = ['cogito:14b', 'qwen2.5:14b', 'mistral-nemo:12b','llama3.2:3b']
    # useful_models = ['cogito:14b', 'qwen2.5:14b', 'mistral-nemo:12b','hermes3:8b','qwen2.5:7b','cogito:8b','llama3.2:3b','cogito:3b']

    vdb = create_vdb(engine=args.engine, embedder=args.embedder)
    kb = create_kb(vdb, urls)

    if args.model:
        models_to_use = [args.model]
    else:
        models_to_use = useful_models

    for m in models_to_use:
        print (f"\n\nRunning {m}")

        agent = Agent(knowledge=kb,model=Ollama(id=m), exponential_backoff=True, markdown=True,telemetry=False,debug_mode=True,stream=True,
            description="You are a season FedRAMP compliance analyst with in depth experience with the NIST 800-53 framework and operational security monitoring tools in AWS GovCloud", instructions=['You have an important briefing with the CISO and Product Manager and you must impress them with your knowledge and experience so they provide the necessary funding for tools and headcount']
        )
        r = agent.run("1) Define continous monitoring  2) Explain the three most important steps (in order) to implement a continous monitoring program.  For each step identify the NIST 800-53 control (or controls) that are relevant to ensure you can pass your annual assessment and achieve monthly reporting goals")

        print(r)
        print (type(r))

        # tools = [item['tool_args'] for item in r.tools]
        #content = r.content
        #metrics = r.metrics
        # print(tools)
