import fitz  # PyMuPDF
import docx
from typing import Union

def parse_pdf(file_path: str) -> str:
    """Extracts text from a PDF file."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error parsing PDF {file_path}: {e}")
        return ""

def parse_docx(file_path: str) -> str:
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error parsing DOCX {file_path}: {e}")
        return ""

def parse_document(file_path: str) -> Union[str, None]:
    """
    Parses a document based on its file extension.
    Returns the extracted text or None if the format is unsupported.
    """
    if file_path.lower().endswith(".pdf"):
        return parse_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        return parse_docx(file_path)
    else:
        print(f"Unsupported file format for {file_path}")
        return None