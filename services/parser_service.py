import fitz  # PyMuPDF
import docx
from typing import Union, IO
import io

# No changes needed in these synchronous helper functions
def parse_pdf(file_content: bytes) -> str:
    """Extracts text from PDF file content in bytes."""
    try:
        doc = fitz.open(stream=file_content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error parsing PDF content: {e}")
        return ""

def parse_docx(file_content: bytes) -> str:
    """Extracts text from a DOCX file stream."""
    try:
        file_stream = io.BytesIO(file_content)
        doc = docx.Document(file_stream)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error parsing DOCX content: {e}")
        return ""

# CORRECTED: This function is now asynchronous
async def parse_document(file_stream: IO[bytes], filename: str) -> Union[str, None]:
    """
    Asynchronously reads the content from a file stream and parses it.
    """
    # CORRECTED: Awaiting the async read() operation
    file_content = await file_stream.read()
    
    if filename.lower().endswith(".pdf"):
        return parse_pdf(file_content)
    elif filename.lower().endswith(".docx"):
        return parse_docx(file_content)
    else:
        print(f"Unsupported file format for {filename}")
        return None

