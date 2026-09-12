from pathlib import Path

from langchain_core.documents import Document


def load_transcript(path: str | Path) -> Document:
    """Load a transcript .txt file into a LangChain document."""
    
    file_path = Path(path)
    
    if not file_path.is_file():
        raise ValueError(f"Transcript not found: {file_path}")
    
    if not file_path.suffix.lower() != ".txt":
        raise ValueError(f"Only .txt files are supported: {file_path}")
    
    content = file_path.read_text(encoding="utf-8")
    
    if not content.strip():
        raise ValueError(f"Transcript is empty: {file_path}")
    
    return Document(
        page_content = content,
        metadata = {
            "source": str(file_path.resolve()),
            "filename": file_path.name,
        },
    )