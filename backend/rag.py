import os
from dotenv import load_dotenv
load_dotenv()

import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.PersistentClient(path="./chroma_db")
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

collection = chroma_client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_fn
)

def add_document(text: str, doc_id: str, metadata: dict = {}):
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    collection.add(
        documents=chunks,
        ids=[f"{doc_id}_chunk_{i}" for i in range(len(chunks))],
        metadatas=[{"doc_id": doc_id, **metadata} for _ in chunks]
    )
    return f"Added {len(chunks)} chunks from document '{doc_id}'"

def search_documents(query: str, n_results: int = 3) -> str:
    count = collection.count()
    if count == 0:
        return "No documents in knowledge base yet. Please upload a document first."
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, count)
    )
    if not results["documents"][0]:
        return "No relevant documents found."
    output = "Relevant documents found:\n\n"
    for i, doc in enumerate(results["documents"][0]):
        output += f"[Result {i+1}]:\n{doc}\n\n"
    return output