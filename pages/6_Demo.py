import os
import pandas as pd
import streamlit as st
from data.extracted_texts import EXTRACTED_TEXT_PATH
from data.fees_summaries import FEES_SUMMARIES_PATH
from data.pdfs.raw import RAW_PDF_PATH
from data.summarized_pages import SUMMARIZED_TEXT_PATH
from data.human_validated_fees import HUMAN_VALIDATED_FEES_PATH
from src.scripts.ocr import document_ai_ocr_from_pdf
from src.scripts.detect_fees import generate_fees_table_from_summarized_pages, summarize_fees_informations
from src.lib.utils import (
    df_to_xlsx,
    list_csv_file_in_directory,
    list_json_file_in_directory,
    list_pdf_path_in_directory,
)

available_pdf_filepaths = list_pdf_path_in_directory(RAW_PDF_PATH)
available_pdf_filenames = [os.path.basename(
    file) for file in available_pdf_filepaths]

json_extracted_filepaths = list_json_file_in_directory(EXTRACTED_TEXT_PATH)
json_extracted_filename = [os.path.basename(
    file) for file in json_extracted_filepaths]

available_page_summarized_filepaths = list_json_file_in_directory(SUMMARIZED_TEXT_PATH)
available_page_summarized_filenames = [os.path.basename(
    file) for file in available_page_summarized_filepaths]

available_summarized_filepaths = list_csv_file_in_directory(
    FEES_SUMMARIES_PATH)
available_summarized_filenames = [os.path.basename(
    file) for file in available_summarized_filepaths]

if available_pdf_filenames:
    pdf_filename = st.selectbox(
        "Which documents would you loke to extract fees ?",
        (filename for filename in available_pdf_filenames),
        index=None,
        placeholder="Select one of the available document names ...",
    )
    if pdf_filename:
        if not pdf_filename.replace(".pdf", ".json") in json_extracted_filename:
            progress_text = 'OCR Text extraction ...'
            my_bar = st.progress(0, text=progress_text)
            saved_pdf_path = os.path.join(RAW_PDF_PATH, pdf_filename)
            for _, (_, percent) in enumerate(document_ai_ocr_from_pdf(saved_pdf_path)):
                my_bar.progress(percent, text=progress_text)
            my_bar.empty()

        if not pdf_filename.replace(".pdf", ".json") in available_page_summarized_filenames:
            # Detect fees
            file = pdf_filename.replace(".pdf", ".json")
            progress_text = "Summarize fees for each page with GPT 3.5 ..."
            my_bar = st.progress(0, text=progress_text)
            for percent, _ in summarize_fees_informations(
                filepath=os.path.join(EXTRACTED_TEXT_PATH, file),
                batch_size=5
            ):
                my_bar.progress(percent, text=progress_text)
            my_bar.empty()

        if not pdf_filename.replace(".pdf", ".csv") in available_summarized_filenames:
            file = pdf_filename.replace(".pdf", ".json")
            with st.spinner("Generating fees table with GPT 4..."):
                df_fees = generate_fees_table_from_summarized_pages(
                    filepath=os.path.join(
                        SUMMARIZED_TEXT_PATH,
                        file)
                )
        else:
            df_fees = pd.read_csv(os.path.join(
                FEES_SUMMARIES_PATH, pdf_filename.replace(".pdf", ".csv")))

        edited_df = st.data_editor(df_fees, num_rows="dynamic")

        send_sheet = st.button("Save a SpreadSheet")
        if send_sheet:
            saved_excel_path = os.path.join(HUMAN_VALIDATED_FEES_PATH, pdf_filename.replace(".pdf", ".xlsx"))
            df_to_xlsx(edited_df, saved_excel_path)
            st.write("SpreadSheet saved")

        send_agile_oft = st.button("Send to Agileoft")
        if send_agile_oft:
            st.write("Fake Sending to Agileoft ...")
