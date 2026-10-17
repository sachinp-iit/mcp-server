"""Answer transcript questions using hybrid retrieval and OpenRounter."""

from functools import lru_cache

from rag.llm.openrouter import create_llm
from rag.prompting.renderer import renderer_prompt
from rag.retrieval.hybrid import HybridRetriever


@lru_cache(maxsize=1)
def get_retriever() -> HybridRetriever:
    """Create and reuse the retrieval components."""

    return HybridRetriever()


def answer_question(question: str) -> dict[str, object]:
    """Retrieve relevant transcript chunks and generate an answer."""

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    # Retrieve from the existing Qdrant and BM25 indexes.
    documents = get_retriever().retrieve(question)

    if not documents:
        return {
            "answer": "No relevant information was found in the indexed transcripts.",
            "sources": [],
        }

    # Prepare context for the existing Jinja2 answer template
    context_documents = [
        {
            "source": document.metadata.get("filename")
            or document.metadata.get("source", "Unknown"),
            "content": document.page_content,
        }
        for document in documents
    ]

    # Call rendering process to render Jinja2 template
    prompt = renderer_prompt(
        "rag/answer.j2",  # Add this in settings file
        documents=context_documents,
        question=question,
    )

    response = create_llm().invoke(prompt)

    sources = list(dict.fromkeys(document["source"] for document in context_documents))

    return {
        "answer": str(response.content),
        "sources": sources,
    }
