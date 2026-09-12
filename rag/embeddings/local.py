from langchain_huggingface import HuggingFaceEmbeddings

from settings import settings


def create_embeddings() -> HuggingFaceEmbeddings:
    """Create the local sentence-transformer embedding model."""
    
    return HuggingFaceEmbeddings (
        model_name = settings.embedding_model,
        model_kwargs = {"device": "cpu"}, # for GPU use argument as "cuda"
        encode_kwargs = {"normalize_embeddings": True}
    )