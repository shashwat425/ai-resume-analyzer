import fitz

def extract_text_from_pdf(pdf_bytes: bytes)->str:
    """
        Extract text from a PDF supplied as bytes.
        The PDF is processed in memory; it is not saved to disk
    """
    try:
      with fitz.open(
        stream = pdf_bytes,
        filetype = "pdf", 
        ) as document:
        text = "\n".join(
            page.get_text() for page in document
        )
              
    except Exception as exp:
        raise ValueError(
        "Could not read this PDF. Please upload a valid PDF"
        ) from exp
       
    text = text.strip()
        
    if not text:
        raise ValueError(
        "No readble text found."
        "The PDF may be scanned or image-based."
        )
    return text 