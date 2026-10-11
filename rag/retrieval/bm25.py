
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi


class BM25Retriever:
    """Local BM25 retriever with a persisted index over transcript chunks."""
    
    def __init__(self, documents: list[Document]) -> None:
        self.documents = documents
        self.index: BM25Okapi | None = None
        
        if documents:
            corpus = [
                self._tokenize(documents.page_content)
                for document in documents
            ]
            self.index = BM25Okapi(corpus)
            
    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Normalize text into simple lowercase tokens."""
        return text.lower().split()
        
        
    def retrieve(self, query: str, k: int) -> list[Document]:
        """Return the top k documents ranked by BM25."""
        
        if not self.index or not query.strip() or k <= 0:
            return []
        
        scores = self.index.get_scores(self._tokenize(query))
        ranked_indexes = sorted(
            range(len(scores)),
            key = lambda index: scores[index],
            reverse=True
        )
        
        return [
            self.documents[index]
            for index in ranked_indexes[:k]
            if scores[index] > 0
        ]