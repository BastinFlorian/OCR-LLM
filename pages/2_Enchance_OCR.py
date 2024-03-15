import os
import streamlit as st
from data.extracted_texts import EXTRACTED_TEXT_PATH
from src.scripts.improve_ocr import enhance_ocr_using_gpt_3_5
from src.lib.utils import list_json_file_in_directory, read_json_from_file

st.markdown("# Enhance OCR 📄")

txt_extracted_filepaths = list_json_file_in_directory(EXTRACTED_TEXT_PATH)
txt_extracted_filename = [os.path.basename(file) for file in txt_extracted_filepaths]

if txt_extracted_filename:
    filename_to_enhance = st.selectbox(
        "Which OCR extracted document would you like to enhance among the available ones ?",
        (filename for filename in txt_extracted_filename),
        index=None,
        placeholder="Select one of the avaimable document names ...",
    )

    if filename_to_enhance:
        extracted_text_dict = read_json_from_file(os.path.join(EXTRACTED_TEXT_PATH, filename_to_enhance))
        extracted_text_str = "\n".join(f"\n \n \n \n{key}: \n {value}" for key, value in extracted_text_dict.items())
        st.session_state.text_to_enhance = extracted_text_str
        st.sidebar.markdown(st.session_state.text_to_enhance)

        enhance_ocr = st.button("Enhance OCR")
        if enhance_ocr:
            st.sidebar.markdown("ok")
            progress_text = f"Enhancing extracted text of {filename_to_enhance} ..."
            my_bar = st.progress(0, text=progress_text)

            for percent, results in enhance_ocr_using_gpt_3_5(
                filepath=os.path.join(EXTRACTED_TEXT_PATH, filename_to_enhance),
                batch_size=5
            ):
                my_bar.progress(percent, text=progress_text)
                st.markdown("\n".join(results))

            my_bar.empty()

else:
    st.markdown("First Extract the text in the first page please")
