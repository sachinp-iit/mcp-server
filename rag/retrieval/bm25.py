from langchain_core.documents import Document
from rank_bm25 import BM25Okapi


class BM25Retriever:
    """Local BM25 retriever over transcript chunks."""
    
    def __init__(self, documents: list[Document]):
        self.documents = documents
        
        # Tokenize chunk text for BM25 indexing.
        corpus = [
            document.page_content.lower().split()
            for document in documents
        ]
        
        self.index = BM25Okapi(corpus)
        
    def retrieve(self, query: str, k: int) -> list[Document]:
        """Retrieve the top-k documents using BM25."""
        
        tokens = query.lower().split()
        scores = self.index.get_scores(tokens)
        
        ranked_indexes = sorted (
            range(len(scores)),
            key = lambda index: scores[index],
            reverse = True,
        )[:k]
        
        return [self.documents[index] for index in ranked_indexes]