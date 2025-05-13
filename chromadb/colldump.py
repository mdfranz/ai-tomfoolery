#!/usr/bin/env python3

import chromadb
from chromadb.config import Settings 

def get_db():
    CHROMA_DATA_PATH = "/tmp/chromadb"
    client = chromadb.PersistentClient(
        path=CHROMA_DATA_PATH,
        settings=Settings() # Default settings are usually sufficient for inspection
        # tenant and database parameters can be specified if not using defaults
    )
    return client

def dump(client):
    if client:
        print("\nAvailable collections:")
        collections_list = client.list_collections()
        if not collections_list:
            print("  No collections found.")
        for collection_obj in collections_list:
            # Assuming list_collections returns Collection objects
            print(f"=== Name: {collection_obj.name}, ID: {collection_obj.id}, Metadata: {collection_obj.metadata}")
            print (collection_obj.get_model())

if __name__ == "__main__":
    c = get_db()
    dump(c)
    
