#!/usr/bin/env python

# From https://qdrant.tech/documentation/fastembed/fastembed-semantic-search/

import logging,os
from qdrant_client import QdrantClient

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)

    if 'QDRANT_HOST' not in os.environ:
        client = QdrantClient(":memory:")
    else:
        client = QdrantClient(host=os.environ['QDRANT_HOST'])

    docs = ["Qdrant has a LangChain integration for chatbots.", "Qdrant has a LlamaIndex integration for agents."]
    metadata = [
        {"source": "langchain-docs"},
        {"source": "llamaindex-docs"},
    ]
    ids = [42, 2]

    client.add(
        collection_name="test_collection",
        documents=docs,
        metadata=metadata,
        ids=ids
    )

    search_result = client.query(
        collection_name="test_collection",
        query_text="Which integration is best for agents?"
    )
    print(search_result)
