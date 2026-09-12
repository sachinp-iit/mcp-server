from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

from settings import settings


class LocalReranker:
    """Rerank retrieved documents using a local cross-encoder"""
    
    def __init__(self) -> None:
        # Load the reranker once and reuse it.
        self.model = CrossEncoder(settings.reranker_model)
        
    def rerank(self, query: str, documents: list[Document]) -> list[Document]:
        """Return documents ordered by cross-encoder relevance."""
        
        if not documents:
            return []
        
        pairs = [
            (query, document.page_content)
            for document in documents
        ]
        
        scores = self.model.predict(pairs)
        
        ranked = sorted (
            zip(scores, documents),
            key = lambda item: item[0],
            reverse = True
        )
        
        return [
            document
            for _, document in ranked[: settings.rerank_k]
        ]