import PyPDF2
from docx import Document

def extract_text_from_pdf(file):
    pdf_file_obj = open(file, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    num_pages = pdf_reader.numPages
    text = ""
    for page in range(num_pages):
        text += pdf_reader.getPage(page).extractText()
    pdf_file_obj.close()
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = " ".join([p.text for p in doc.paragraphs])
    return text