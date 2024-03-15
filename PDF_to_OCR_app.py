import os
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from data.pdfs.raw import RAW_PDF_PATH
from src.scripts.ocr import document_ai_ocr_from_pdf

if "pdf_ref" not in st.session_state:
    st.session_state.pdf_ref = None

if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""


# Access the uploaded ref via a key.
pdf = st.file_uploader("Upload PDF file", type=('pdf'), key='pdf')

if pdf is not None:
    with st.spinner(text='Loading PDF ...'):
        st.session_state.pdf_ref = pdf  # backup
        st.session_state.binary_data = pdf.getvalue()
        pdf_viewer(input=st.session_state.binary_data, width=700)

with st.sidebar:
    ocr = st.button("Extract text from PDF")
    if ocr and st.session_state["pdf_ref"] is not None:
        binary_data = st.session_state.pdf_ref.getvalue()
        with st.spinner(text=f'Saving {st.session_state["pdf_ref"].name} before extraction ...'):
            with open(os.path.join(RAW_PDF_PATH, st.session_state["pdf_ref"].name), "wb") as f:
                f.write(binary_data)

        pdf_name = st.session_state["pdf_ref"].name.split(".")[0]
        progress_text = 'OCR Text extraction ...'
        my_bar = st.progress(0, text=progress_text)
        full_text = ""
        saved_pdf_path = os.path.join(
            RAW_PDF_PATH, st.session_state["pdf_ref"].name.split(".")[
                0] + ".pdf"
        )
        for page_value, (text, percent) in enumerate(document_ai_ocr_from_pdf(saved_pdf_path)):
            my_bar.progress(percent, text=progress_text)
            partial_text = "\n" + "PAGE:" + str(page_value) + "\n" + text
            st.markdown(partial_text)
            full_text += partial_text

        my_bar.empty()

        st.session_state.extracted_text = full_text
