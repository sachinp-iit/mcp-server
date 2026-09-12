from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from rag.embeddings.local import create_embeddings
from settings import settings


def create_qdrant_client() -> QdrantClient:
    """Create a client for the standalone Qdrant server."""
    
    return QdrantClient (
        host = settings.qdrant_host,
        port = settings.qdrant_port,
    )
    

def create_vector_store() -> QdrantVectorStore:
    """Create the LangChain Qdrant vector store."""
    
    return QdrantVectorStore (
        client = create_qdrant_client(),
        collection_name = settings.qdrant_collection,
        embedding = create_embeddings()
    )