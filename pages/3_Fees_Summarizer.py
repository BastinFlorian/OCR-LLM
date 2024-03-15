import os
import streamlit as st
from data.extracted_texts import EXTRACTED_TEXT_PATH
from data.improved_texts import IMPROVED_TEXT_PATH
from src.scripts.detect_fees import summarize_fees_informations
from src.lib.utils import list_json_file_in_directory, read_json_from_file


json_extracted_filepaths = list_json_file_in_directory(EXTRACTED_TEXT_PATH)
json_extracted_filename = [os.path.basename(file) for file in json_extracted_filepaths]

json_improved_filepaths = list_json_file_in_directory(IMPROVED_TEXT_PATH)
json_improved_filename = [os.path.basename(file) for file in json_extracted_filepaths]

chosen_method = st.selectbox(
        "Would you like to detect fees from the extracted OCR and improved OCR techniques?",
        ("Extracted OCR", "Improved OCR"),
        index=None,
        placeholder="Select the method you want to use ...",
    )


if chosen_method:
    if chosen_method == "Extracted OCR":
        extracted_ocr_method = st.selectbox(
            "Which file do you want to use ?",
            (filename for filename in json_extracted_filename),
            index=None,
            placeholder="Select the extracted OCR file you want to use ...",
        )

        if extracted_ocr_method:
            # Display the extracted text
            extracted_text_dict = read_json_from_file(os.path.join(EXTRACTED_TEXT_PATH, extracted_ocr_method))
            extracted_text_str = "\n".join(
                f"\n \n \n \n{key}: \n {value}" for key, value in extracted_text_dict.items()
            )
            st.session_state.text_to_enhance = extracted_text_str
            st.sidebar.markdown(st.session_state.text_to_enhance)

            # Detect fees
            progress_text = "Summarize fees for each page with GPT 3.5 ..."
            my_bar = st.progress(0, text=progress_text)

            for percent, results in summarize_fees_informations(
                filepath=os.path.join(EXTRACTED_TEXT_PATH, extracted_ocr_method),
                batch_size=5
            ):
                my_bar.progress(percent, text=progress_text)
                st.markdown(results)

            my_bar.empty()

    elif chosen_method == "Improved OCR":
        improved_ocr_method = st.selectbox(
            "Which file do you want to use ?",
            (filename for filename in json_improved_filename),
            index=None,
            placeholder="Select the improved OCR file you want to use ...",
        )

        if improved_ocr_method:
            # Display the extracted text
            improved_text_dict = read_json_from_file(
                os.path.join(IMPROVED_TEXT_PATH, improved_ocr_method))
            improved_text_str = "\n".join(
                f"\n \n \n \n{key}: \n {value}" for key, value in improved_text_dict.items()
            )
            st.session_state.text_to_enhance = improved_text_str
            st.sidebar.markdown(st.session_state.text_to_enhance)

            # Detect fees
            progress_text = "Summarize fees for each page ..."
            my_bar = st.progress(0, text=progress_text)

            for percent, results in summarize_fees_informations(
                filepath=os.path.join(
                    IMPROVED_TEXT_PATH, improved_ocr_method),
                batch_size=5
            ):
                my_bar.progress(percent, text=progress_text)
                st.markdown(results)

            my_bar.empty()
