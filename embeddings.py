import os
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
def initialize_embeddings():
    """Initialize HuggingFace embeddings."""
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )
def update_vector_store(new_docs, persist_dir="./chroma_store"):
    """Create or update vector store incrementally."""
    embeddings = initialize_embeddings()
    if os.path.exists(persist_dir):  # Append to existing
        vector_store1 = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings,
        )
        vector_store2 = Chroma(
            persist_directory="./chromaRACI",
            embedding_function=embeddings,
        )
        retriever1 = vector_store1.as_retriever(search_type="similarity", search_kwargs={"k": 10})
        retriever2 = vector_store2.as_retriever(search_type="similarity", search_kwargs={"k": 10})
    else:  # Create new
        vector_store = Chroma.from_documents(
            documents=new_docs,
            embedding=embeddings,
            persist_directory=persist_dir,
            collection_metadata={"hnsw:space": "cosine"}
        )
    return [retriever1, retriever2]