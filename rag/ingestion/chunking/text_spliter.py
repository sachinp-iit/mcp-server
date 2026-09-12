from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from settings import settings


def create_text_splitter() -> RecursiveCharacterTextSplitter:
    """Create the configured LangChain text splitter."""
    
    return RecursiveCharacterTextSplitter(
        chunk_size = settings.chunk_size,
        chunk_overlap = settings.chunk_overlap,
        length_function = len,
        separators=["\n\n", "\n", " ", ""],
    )
    
def split_documents(documents: list[Document]) -> list[Document]:
    """Split transcripts into LangChain Documents while preserving metadata."""
    
    splitter = create_text_splitter()
    
    return splitter.split_documents(documents)