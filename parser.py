import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        # If error occurs, try OCR as fallback
        uploaded_file.seek(0)
        images = convert_pdf_to_images(uploaded_file)
        for image in images:
            text += pytesseract.image_to_string(image)
    return clean_text(text)

def convert_pdf_to_images(uploaded_file):
    images = []
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes()))
                images.append(img)
    except Exception:
        pass
    return images

def clean_text(text):
    # Basic cleaning and normalization
    return " ".join(text.split())
