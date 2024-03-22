import os
import pandas as pd
import streamlit as st
from config.fees_table import BASIS_CONFIG, CURRENCY_CODE_CONFIG, TYPE_OF_FEES_CONFIG, VAT_ON_BASIC_CONFIG
from data.extracted_texts import EXTRACTED_TEXT_PATH
from data.fees_summaries import FEES_SUMMARIES_PATH
from data.pdfs.raw import RAW_PDF_PATH
from data.summarized_pages import SUMMARIZED_TEXT_PATH
from data.human_validated_fees import HUMAN_VALIDATED_FEES_PATH
from src.scripts.ocr import document_ai_ocr_from_pdf
from src.scripts.detect_fees import generate_fees_table_from_summarized_pages, summarize_fees_informations
from src.lib.utils import (
    df_to_xlsx,
    list_tsv_file_in_directory,
    list_json_file_in_directory,
    list_pdf_path_in_directory,
)

if "pdf_ref" not in st.session_state:
    st.session_state.pdf_ref = None

available_pdf_filepaths = list_pdf_path_in_directory(RAW_PDF_PATH)
available_pdf_filenames = [os.path.basename(
    file) for file in available_pdf_filepaths]

json_extracted_filepaths = list_json_file_in_directory(EXTRACTED_TEXT_PATH)
json_extracted_filename = [os.path.basename(
    file) for file in json_extracted_filepaths]

available_page_summarized_filepaths = list_json_file_in_directory(SUMMARIZED_TEXT_PATH)
available_page_summarized_filenames = [os.path.basename(
    file) for file in available_page_summarized_filepaths]

available_summarized_filepaths = list_tsv_file_in_directory(
    FEES_SUMMARIES_PATH)
available_summarized_filenames = [os.path.basename(
    file) for file in available_summarized_filepaths]

# Upload and save PDF
pdf = st.file_uploader("Upload PDF file", type=('pdf'), key='pdf')
if pdf is not None:
    st.session_state.pdf_ref = pdf
    pdf_filename = st.session_state["pdf_ref"].name
    # Save PDF
    if pdf_filename not in available_pdf_filenames:
        # Upload PDF
        binary_data = st.session_state.pdf.getvalue()
        with st.spinner(text=f'Saving {pdf_filename} before extraction ...'):
            with open(os.path.join(RAW_PDF_PATH, pdf_filename), "wb") as f:
                f.write(binary_data)

    # OCR
    if not pdf_filename.replace(".pdf", ".json") in json_extracted_filename:
        progress_text = 'OCR Text extraction ...'
        my_bar = st.progress(0, text=progress_text)
        saved_pdf_path = os.path.join(RAW_PDF_PATH, pdf_filename)
        for _, (_, percent) in enumerate(document_ai_ocr_from_pdf(saved_pdf_path)):
            my_bar.progress(percent, text=progress_text)
        my_bar.empty()

    # Summarize bu by page
    if not pdf_filename.replace(".pdf", ".json") in available_page_summarized_filenames:
        # Detect fees
        file = pdf_filename.replace(".pdf", ".json")
        progress_text = "Summarize fees for each page with GPT 3.5 ..."
        my_bar = st.progress(0, text=progress_text)
        for percent, _ in summarize_fees_informations(
            filepath=os.path.join(EXTRACTED_TEXT_PATH, file)
        ):
            my_bar.progress(percent, text=progress_text)
        my_bar.empty()

    # Generate fees table
    if not pdf_filename.replace(".pdf", ".tsv") in available_summarized_filenames:
        file = pdf_filename.replace(".pdf", ".json")
        with st.spinner("Generating fees table with GPT 4..."):
            df_fees = generate_fees_table_from_summarized_pages(
                filepath=os.path.join(
                    SUMMARIZED_TEXT_PATH,
                    file)
            )
    else:
        df_fees = pd.read_csv(os.path.join(
            FEES_SUMMARIES_PATH, pdf_filename.replace(".pdf", ".tsv")), sep="\t")

    edited_df = st.data_editor(
        df_fees,
        column_config={
            BASIS_CONFIG.column_name:
                st.column_config.SelectboxColumn(
                    width="medium",
                    options=BASIS_CONFIG.column_values,
                    required=True,
                ),
            CURRENCY_CODE_CONFIG.column_name:
                st.column_config.SelectboxColumn(
                    width="medium",
                    options=CURRENCY_CODE_CONFIG.column_values,
                    required=True,
                ),
            VAT_ON_BASIC_CONFIG.column_name:
                st.column_config.SelectboxColumn(
                    width="medium",
                    options=VAT_ON_BASIC_CONFIG.column_values,
                    required=True,
                ),
            TYPE_OF_FEES_CONFIG.column_name:
                st.column_config.SelectboxColumn(
                    width="medium",
                    options=TYPE_OF_FEES_CONFIG.column_values,
                    required=True,
                ),
        },
        num_rows="dynamic"
    )

    # Send to Agileoft and Spreadsheet
    send_sheet = st.button("Save Table as Spreadsheet")
    if send_sheet:
        saved_excel_path = os.path.join(HUMAN_VALIDATED_FEES_PATH, pdf_filename.replace(".pdf", ".xlsx"))
        df_to_xlsx(edited_df, saved_excel_path)
        st.write("SpreadSheet saved")

    send_agile_oft = st.button("Send to Agileoft")
    if send_agile_oft:
        st.write("Fake Sending to Agileoft ...")
