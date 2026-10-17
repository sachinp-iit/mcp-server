import json
from pathlib import Path
from typing import Any

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi


class BM25Retriever:
    """Local BM25 retriever with a persisted index over transcript chunks."""

    def __init__(
        self,
        documents: list[Document] | None = None,
        index_path: str | Path | None = None,
    ) -> None:
        # Store the index outside the source directories
        project_root = Path(__file__).resolve().parents[2]
        self.index_path = (
            Path(index_path)
            if index_path is not None
            else project_root / "data" / "indexes" / "bm25.json"
        )

        self.documents: list[Document] = []
        self.index: BM25Okapi | None = None

        # When documents are supplied, build and persist a fresh index
        if documents:
            self.build(documents)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Normalize text into simple lowercase tokens."""
        return text.lower().split()

    def build(self, documents: list[Document]) -> None:
        """Build the BM25 index and persist its source documents"""

        if not documents:
            raise ValueError("Cannot build a BM25 index without documents")

        self.documents = documents

        corpus = [self._tokenize(Document.page_content) for document in self.documents]

        self.index = BM25Okapi(corpus)

        # Persist document content and metadata as JSON.
        # The BM25 index itself is reconstructed when we load.
        self.index_path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "documents": [
                {"page_content": document.page_content, "metadata": document.metadata}
                for document in self.documents
            ]
        }

        temporary_path = self.index_path.with_suffix(".tmp")

        try:
            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump(payload, file, ensure_ascii=False, default=str)

            # Replace the old index only after the new file is written
            temporary_path.replace(self.index_path)
        finally:
            if temporary_path.exists():
                temporary_path.unlink()

    def load(self) -> None:
        """Load persisted documents and reconstruct the BM25 index."""

        if not self.index_path.is_file():
            raise FileNotFoundError(
                f"BM25 index not found at {self.index_path}. "
                "Ingest transcripts before querying."
            )

        with self.index_path.open("r", encoding="utf-8") as file:
            payload: dict[str, Any] = json.load(file)

        stored_documents = payload.get("documents")

        if not isinstance(stored_documents, list) or not stored_documents:
            raise ValueError(f"BM25 index contains no documents: {self.index_path}")

        self.documents = [
            Document(
                page_content=item["page_content"], metadata=item.get("metadata", {})
            )
            for item in stored_documents
        ]

        corpus = [self._tokenize(document.page_content) for document in self.documents]

        self.index = BM25Okapi(corpus)

    def retrieve(self, query: str, k: int) -> list[Document]:
        """Return the top k documents ranked by BM25."""

        if not self.index or not query.strip() or k <= 0:
            return []

        # Load the persisted index on first query if not already built.
        if self.index is None:
            self.load()

        if self.index is None or not self.documents:
            return []

        scores = self.index.get_scores(self._tokenize(query))

        ranked_indexes = sorted(
            range(len(scores)), key=lambda index: scores[index], reverse=True
        )

        return [
            self.documents[index] for index in ranked_indexes[:k] if scores[index] > 0
        ]
