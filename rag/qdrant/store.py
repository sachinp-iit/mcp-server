from functools import lru_cache

from langchain_qdrant import QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient, models

from rag.embeddings.local import create_embeddings
from settings import settings


@lru_cache(maxsize=1)
def create_qdrant_client() -> QdrantClient:
    """Create a client for the standalone Qdrant server."""
    
    return QdrantClient (
        host = settings.qdrant_host,
        port = settings.qdrant_port,
    )
    
@lru_cache(maxsize=1)
def create_vector_store() -> QdrantVectorStore:
    """Create the collection if needed and return its vector store."""
    
    client = create_qdrant_client()
    embeddings = create_embeddings()
    
    # Derive vector size from the configured embedding model.
    vector_size = len(embeddings.embed_query("dimension check"))
    
    # Create the collection only when it does not already exist
    if not client.collection_exists(settings.qdrant_collection):
        client.create_collection(
            collection_name = settings.qdrant_collection,
            vectors_config = models.VectorParams(
                size = vector_size,
                distance = models.Distance.COSINE,
            )
        )
        
    
    return QdrantVectorStore(
        client = client,
        collection_name = settings.qdrant_collection,
        embedding = embeddings,
        retrieval_mode = RetrievalMode.DENSE,
    )