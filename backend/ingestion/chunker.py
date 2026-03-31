from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from pathlib import Path

def load_documents(knowledge_base_path: str) -> list:
    """Load all markdown and PDF files from the knowledge base folder."""
    docs = []
    path = Path(knowledge_base_path)

    # Load markdown files
    for md_file in path.rglob("*.md"):
        try:
            loader = TextLoader(str(md_file), encoding="utf-8")
            loaded = loader.load()
            for doc in loaded:
                doc.metadata["category"] = md_file.parent.name
                doc.metadata["source"] = md_file.name
            docs.extend(loaded)
            print(f"  Loaded: {md_file.name}")
        except Exception as e:
            print(f"  Failed to load {md_file.name}: {e}")

    # Load PDF files
    for pdf_file in path.rglob("*.pdf"):
        try:
            loader = PyPDFLoader(str(pdf_file))
            loaded = loader.load()
            for doc in loaded:
                doc.metadata["category"] = pdf_file.parent.name
                doc.metadata["source"] = pdf_file.name
            docs.extend(loaded)
            print(f"  Loaded: {pdf_file.name}")
        except Exception as e:
            print(f"  Failed to load {pdf_file.name}: {e}")

    print(f"\nTotal documents loaded: {len(docs)}")
    return docs

def chunk_documents(docs: list) -> list:
    """
    Split documents into overlapping chunks.
    
    chunk_size=500    — each chunk is ~500 characters
    chunk_overlap=100 — 100 chars overlap between chunks so 
                        we don't lose meaning at boundaries
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_documents(docs)
    print(f"Total chunks created: {len(chunks)}")
    return chunks