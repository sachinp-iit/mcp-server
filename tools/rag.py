"""Expose transcript ingestion and RAG question answering as MCP tools."""

from mcp.server.fastmcp import FastMCP

from rag.answering import answer_question
from rag.ingestion.pipeline import ingest_transcripts


def register(mcp: FastMCP) -> None:
    """Register RAG tools with the existing FastMCP server."""

    @mcp.tool()
    def ingest_transcript_files() -> dict[str, int | str]:
        """Ingest local transcript txt files into Qdrant and the BM25 index."""
        chunk_count = ingest_transcripts()

        return {"status": "success", "chunks_indexed": chunk_count}

    @mcp.tool()
    def ask_transcripts(question: str) -> dict[str, object]:
        """Answer a question using hybrid retrieval over indexed transcripts."""

        return answer_question(question)
