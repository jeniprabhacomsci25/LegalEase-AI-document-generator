import streamlit as st
import os
from dotenv import load_dotenv
from utils import generate_legal_document, create_docx
from fpdf import FPDF

# Initialize environment variables
load_dotenv()

# Page Configuration (Centered Layout)
st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="centered")

# Custom CSS for Dark Theme and Centered Headers
st.markdown("""
    <style>
    /* Force dark background */
    .stApp { background-color: #0e1117; color: #fafafa; }
    
    /* Centered Title Container */
    .title-container { text-align: center; padding-bottom: 2rem; padding-top: 1rem; }
    .title-container h1 { font-size: 2.8rem; font-weight: 600; margin-bottom: 0.2rem; }
    .title-container h3 { font-size: 1.3rem; font-weight: 500; color: #cbd5e1; margin-top: 0; }
    
    /* Input Labels */
    label, p { color: #e2e8f0 !important; font-size: 0.9rem !important; }
    
    /* Input Fields Styling */
    .stTextInput input, .stTextArea textarea {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
    }
    
    /* Button Styling */
    .stButton>button, .stDownloadButton>button {
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 10px;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        border-color: #60a5fa;
        color: #60a5fa;
    }
    
    /* Info Box Styling */
    .stAlert { background-color: #1e3a8a !important; color: white !important; border: none !important;}
    </style>
""", unsafe_allow_html=True)

# Helper function for PDF generation
def create_pdf_file(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    for line in text.split('\n'):
        # Handle special characters safely for basic FPDF
        safe_line = line.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 8, txt=safe_line)
    return pdf.output(dest='S').encode('latin-1')

# Main Title Section
st.markdown("""
    <div class="title-container">
        <h1>⚖️ LegalEase</h1>
        <h3>AI Legal Document Generator</h3>
    </div>
""", unsafe_allow_html=True)

# Hidden API Configuration in Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    env_api_key = os.getenv("GEMINI_API_KEY", "")
    api_key = st.text_input("Google Gemini API Key", type="password", value=env_api_key)
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        st.success("API Key loaded successfully!")
    else:
        st.warning("Please enter your Gemini API Key to continue.")

# Input Fields
doc_type = st.text_input("Document Type (Ex: Agreement, Contract, NDA)")
parties = st.text_area("Parties Involved")
terms = st.text_area("Terms & Conditions (Use semicolons for bullet points)")
eff_date = st.text_input("Effective Date")

st.markdown("<br>", unsafe_allow_html=True)

# Generate Button and Status Box
if st.button("Generate Document", use_container_width=True):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not doc_type or not parties:
        st.warning("Please fill in at least the Document Type and Parties Involved.")
    else:
        with st.spinner("Generating document..."):
            generated_text = generate_legal_document(
                doc_type=doc_type,
                parties_involved=parties,
                terms_conditions=terms,
                effective_date=eff_date
            )
            st.session_state['generated_doc'] = generated_text
            st.session_state['doc_title'] = doc_type
else:
    if 'generated_doc' not in st.session_state:
        st.info("ℹ Click 'Generate Document' to start")

# Output Section
if 'generated_doc' in st.session_state:
    st.markdown("---")
    
    # Image nalli iruva hage success message
    st.success("✅ Document Generated Successfully!")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Edit Document Expander Button
    with st.expander("🖊️ Click to Edit Document"):
        st.text_area("Document Editor", value=st.session_state['generated_doc'], height=400, key="edited_doc", label_visibility="hidden")
    
    current_text = st.session_state.get('edited_doc', st.session_state['generated_doc'])
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Download TXT Button
    st.download_button(
        label="📄 Download as .TXT",
        data=current_text,
        file_name=f"{st.session_state['doc_title'].replace(' ', '_')}.txt",
        mime="text/plain"
    )
    
    # 3. Download DOCX Button
    docx_file = create_docx(current_text, st.session_state['doc_title'])
    st.download_button(
        label="📄 Download as .DOCX",
        data=docx_file,
        file_name=f"{st.session_state['doc_title'].replace(' ', '_')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    
    # 4. Download PDF Button
    pdf_file = create_pdf_file(current_text)
    st.download_button(
        label="📕 Download as .PDF",
        data=pdf_file,
        file_name=f"{st.session_state['doc_title'].replace(' ', '_')}.pdf",
        mime="application/pdf"
    )