import fitz  # PyMuPDF to extract text directly from the PDF
import pytesseract
from PIL import Image
import pyttsx3
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def pdf_to_images(pdf_file, poppler_path):
    """Convert PDF to images using pdf2image."""
    images = convert_from_path(pdf_file, poppler_path=poppler_path)
    return images

def ocr_image_to_text(images):
    """Use pytesseract to extract text from images."""
    full_text = ""
    for image in images:
        text = pytesseract.image_to_string(image)
        full_text += text
    return full_text

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF using PyMuPDF (fitz)."""
    doc = fitz.open(pdf_file)
    extracted_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        if text.strip():
            extracted_text += f"\n\n--- Page {page_num + 1} ---\n{text}"
    return extracted_text

def text_to_speech(text):
    """Convert text to speech using pyttsx3."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Set speaking speed
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    pdf_file = r'C:\Users\yesha\Downloads\THRONE_OF_GLASS_01_Throne_of_Glass.pdf'
    poppler_path = r'C:\Users\yesha\Downloads\Release-24.07.0-0\poppler-24.07.0\Library\bin'

    # Extract text directly from the PDF
    extracted_text = extract_text_from_pdf(pdf_file)

    if extracted_text.strip():
        print("Extracted text from the PDF.")
        text_to_speech(extracted_text)  # Convert extracted text to speech
    else:
        print("No text found in the PDF, falling back to OCR.")

        # Convert PDF to images (if it's an image-based PDF like scanned pages)
        images = pdf_to_images(pdf_file, poppler_path=poppler_path)

        # Use OCR to extract text from images
        extracted_text = ocr_image_to_text(images)

        if extracted_text.strip():
            print("Extracted text from images.")
            text_to_speech(extracted_text)  # Convert extracted text to speech
        else:
            raise ValueError("No text or images found that can be processed.")