from langchain_core.documents import Document

from rag.qdrant.store import create_vector_store
from rag.retrieval.bm25 import BM25Retriever
from settings import settings


class HybridRetriever:
    """Combine dense qdrant retrieval with local BM25 retrieval."""
    
    def __init__(self, documents: list[Document]):
        self.vector_store = create_vector_store()
        self.bm25 = BM25Retriever(documents)
        
    def retrieve(self, query: str) -> list[Document]:
        """Retrieve candidates from both dense and keyword search."""
        
        # Dense retrieval from Qdrant.
        dense_docs = self.vector_store.similarity_search(
            query,
            k = settings.retrieval_k,
        )
        
        # Keyword/pattern retrieval from the local BM25 index.
        bm25_docs = self.bm25.retrieve (
            query,
            k = settings.retrieval_k,
        )
        
        # Merge candidates while preserving document uniqueness.
        merged: dict[tuple[str, str], Document] = {}
        
        for document in dense_docs + bm25_docs:
            key = (
                document.metadata.get("source", ""),
                document.page_content,
            )
            merged[key] = document
            
        return list(merged.values())