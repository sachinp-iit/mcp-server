"""Orchestrate hybrid retrieval, reranking, and LLM answer generation."""

from langchain_core.documents import Document

from rag.llm.openrouter import create_llm
from rag.prompting.renderer import renderer_prompt
from rag.retrieval.hybrid import HybridRetriever
from rag.ingestion.pipeline import load_transcripts
from rag.ingestion.chunking.text_spliter import split_documents

from settings import settings
