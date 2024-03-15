import os
import streamlit as st
from data.extracted_texts import EXTRACTED_TEXT_PATH
from data.improved_texts import IMPROVED_TEXT_PATH
from src.scripts.rag import answer_question, create_chatbot, create_chain
from src.lib.utils import list_json_file_in_directory
from config.llm import LLM_35

LOGO_PATH = "../logo.png"

json_extracted_filepaths = list_json_file_in_directory(EXTRACTED_TEXT_PATH)
json_extracted_filename = [os.path.basename(file) for file in json_extracted_filepaths]

json_improved_filepaths = list_json_file_in_directory(IMPROVED_TEXT_PATH)
json_improved_filename = [os.path.basename(
    file) for file in json_extracted_filepaths]

if 'filename' not in st.session_state:
    st.session_state.filename = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "chain" not in st.session_state:
    st.session_state.chain = None


chosen_method = st.selectbox(
    "From which text would you like to talk to ?",
    ("Extracted OCR", "Improved OCR"),
    index=None,
    placeholder="Select the method you want to use ...",
)

if chosen_method:
    if chosen_method == "Extracted OCR":
        st.session_state.filename = st.selectbox(
            "Which file do you want to use ?",
            (filename for filename in json_extracted_filename),
            index=None,
            placeholder="Select the extracted OCR file you want to use ...",
        )

    elif chosen_method == "Improved OCR":
        st.session_state.filename = st.selectbox(
            "Which file do you want to use ?",
            (filename for filename in json_improved_filename),
            index=None,
            placeholder="Select the improved OCR file you want to use ...",
        )
if st.session_state.filename:
    with st.spinner("Creating Chatbot ..."):
        st.session_state.retriever = create_chatbot(
            filepath=os.path.join(IMPROVED_TEXT_PATH, st.session_state.filename)
        )
        st.session_state.chain = create_chain(
            st.session_state.retriever, model=LLM_35)

if st.session_state.chain:
    st.write("Chatbot created !")
    st.write("You can now chat with your PDF")
    input = st.chat_input("How can I help you ?")
    if input:
        answer = answer_question(input, chain=st.session_state.chain)
        st.markdown(answer)
