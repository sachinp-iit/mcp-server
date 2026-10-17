from pathlib import Path

from langchain_core.documents import Document

from rag.ingestion.chunking.text_spliter import split_documents
from rag.ingestion.loaders.text_loader import load_transcript
from rag.qdrant.store import create_vector_store
from rag.retrieval.bm25 import BM25Retriever
from settings import settings


def load_transcripts() -> list[Document]:
    """Load all transcripts .txt files from the configured directory."""

    directory = Path(settings.transcript_director)

    if not directory.exists():
        raise FileNotFoundError(f"Transcription director not found: {directory}")

    documents: list[Document] = []

    # Loop through the configured path and look for *.txt files
    for file_path in sorted(directory.glob("*.txt")):
        # Load the file, read the file and convert into the langchain core Document
        # class format
        documents.append(load_transcript(file_path))

    return documents


def ingest_transcripts() -> int:
    """Load, chunk, and store transcripts in Qdrant."""

    documents = load_transcripts()

    if not documents:
        return 0

    chunks = split_documents(documents)

    if not chunks:
        return 0

    # Build the local lexical index from the same chunks stored in Qdrant.
    bm25 = BM25Retriever()
    bm25.build(chunks)

    # Store dense vectors and chunk metadata in Qdrant.
    vector_store = create_vector_store()
    vector_store.add_documents(chunks)

    return len(chunks)
