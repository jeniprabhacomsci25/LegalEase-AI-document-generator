import os
import google.generativeai as genai
from docx import Document
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_legal_document(doc_type, parties_involved, terms_conditions, effective_date):
    """
    Generates a legal document using Google Gemini based on the updated UI parameters.
    """
    prompt = f"""
    Act as an expert corporate lawyer. Generate a comprehensive, legally binding {doc_type}. 
    
    Parties Involved:
    {parties_involved}
    
    Effective Date: {effective_date}
    
    Terms, Conditions, and Specifics: 
    {terms_conditions}
    
    Requirements:
    1. Structure the contract with clear, numbered sections.
    2. Use precise, professional legal terminology.
    3. Include necessary boilerplate clauses appropriate for this document type.
    4. Output the pure document text starting directly with the document title. Do not include introductory conversational text.
    """
    
    try:
        # Utilizing Gemini 3.5 Flash for fast and accurate generation
        model = genai.GenerativeModel('gemini-3.5-flash') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating document: {e}"

def create_docx(text, doc_title):
    """
    Converts the generated text into a formatted Word Document (.docx).
    """
    doc = Document()
    doc.add_heading(doc_title, 0)
    
    for paragraph in text.split('\n'):
        if paragraph.strip():
            doc.add_paragraph(paragraph.strip())
            
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream