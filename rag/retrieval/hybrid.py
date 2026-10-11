from collections import defaultdict

from langchain_core.documents import Document

from rag.qdrant.store import create_vector_store
from rag.retrieval.bm25 import BM25Retriever
from rag.retrieval.reranker import LocalReranker
from settings import settings


class HybridRetriever:
    """Combine dense and BM25 retrieval using Reciprocal Rank Fusion."""
    
    def __init__(self, documents: list[Document]) -> None:
        self.vector_store = create_vector_store()
        self.bm25 = BM25Retriever(documents)
        self.reranker = LocalReranker()
        
    def retrieve(self, query: str) -> list[Document]:
        """Fuse dense and lexical rankings into one candidate list."""
        
        if not query.strip():
            return []
        
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
        
        # RRF combines ranks rather than incomparable raw scores
        scores: dict[tuple[str, str], float] = defaultdict(float)
        documents_by_key: dict[tuple[str, str], Document] = {}
        rrf_constant = 60
        
        for ranked_docs, weight in (
            (dense_docs, settings.dense_weight),
            (bm25_docs, settings.bm25_weight),
        ):
            for rank, document in enumerate(ranked_docs, start = 1):
                key = (
                    document.metadata.get("source", ""),
                    document.page_content,
                )
                scores[key] += weight / (rrf_constant + rank)
                documents_by_key[key] = document
        
        
        ranked_keys = sorted(
            scores.keys(),
            key = lambda key: scores[key],
            reverse = True,
            )
        
        candidates = [
            documents_by_key[key]
            for key in ranked_keys
        ]
        
        return self.reranker.rerank(query, candidates)