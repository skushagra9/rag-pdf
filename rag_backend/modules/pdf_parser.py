from PyPDF2 import PdfReader
import io


def extract_text_from_pdf(file):
    """Extract text from a PDF file or file-like object."""
    try:
        if isinstance(file, str):
            # If file is a path, open it as a file
            with open(file, "rb") as f:
                reader = PdfReader(f)
        elif isinstance(file, io.BytesIO):
            # If file is a BytesIO object
            reader = PdfReader(file)
        else:
            raise ValueError("Unsupported file type. Must be a file path or BytesIO object.")
        
        # Extract text from all pages
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")
