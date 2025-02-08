from PyPDF2 import PdfReader
import io


def extract_text_from_pdf(file):
    """Extract text from a PDF file or file-like object."""
    try:
        if isinstance(file, str):
            with open(file, "rb") as f:
                reader = PdfReader(f)
        elif isinstance(file, io.BytesIO):
            reader = PdfReader(file)
        else:
            raise ValueError("Unsupported file type. Must be a file path or BytesIO object.")
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        print(text)
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")
