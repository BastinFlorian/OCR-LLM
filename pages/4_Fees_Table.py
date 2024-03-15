import os
import streamlit as st
from data.summarized_pages import SUMMARIZED_TEXT_PATH
from src.lib.utils import list_json_file_in_directory
from src.scripts.detect_fees import generate_fees_table_from_summarized_pages


available_filepaths = list_json_file_in_directory(SUMMARIZED_TEXT_PATH)
available_filenames = [os.path.basename(file) for file in available_filepaths]

if "filepath_to_extract_fees" not in st.session_state:
    st.session_state.filepath_to_extract_fees = None


st.session_state.filepath_to_extract_fees = st.selectbox(
    "Which filename would you like to use to extract the fees ?",
    (filename for filename in available_filenames),
    index=None,
    placeholder="Select one of the available filenames ...",
)

if st.session_state.filepath_to_extract_fees:
    with st.spinner("Generating fees table with GPT 4..."):
        fees_table = generate_fees_table_from_summarized_pages(
            filepath=os.path.join(
                SUMMARIZED_TEXT_PATH,
                st.session_state.filepath_to_extract_fees)
        )
    st.markdown(fees_table)
