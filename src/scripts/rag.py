import os
from typing import List
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from db import DB_PATH
from config.embeddings import EMBEDDINGS
from config.prompt import RAG_PROMPT
from src.lib.utils import create_directory_if_not_exists, read_json_from_file, remove_directory_if_exists


def use_chatbot():
    db = Chroma(
        embedding_function=EMBEDDINGS,
        persist_directory=os.path.join(DB_PATH, "chroma"),
        collection_metadata={"hnsw:space": "cosine"}
    )
    return db.as_retriever(
        search_kwargs={
            "k": 10,
        }
    )


def create_chatbot(filepath):
    json_text = read_json_from_file(filepath)
    docs = json_to_document(json_text)
    splitted_docs = split_documents(docs)
    db = create_chroma_and_load_documents(splitted_docs)
    retriever = db.as_retriever(
        search_kwargs={
            "k": 10,
        }
    )
    return retriever


def json_to_document(json_text) -> List[Document]:
    return [
        Document(
            page_content=text,
            metadata={"page_number": page_number}
        )
        for text, page_number in json_text.items()
    ]


def split_documents(docs: List[Document]) -> List[Document]:
    content_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", "\n", " ", ""]
    )
    return content_splitter.split_documents(docs)


def create_chroma_and_load_documents(documents: List[Document]) -> Chroma:
    remove_directory_if_exists(os.path.join(DB_PATH, "chroma"))
    create_directory_if_not_exists(os.path.join(DB_PATH, "chroma"))
    db = Chroma(
        embedding_function=EMBEDDINGS,
        persist_directory=os.path.join(DB_PATH, "chroma"),
        collection_metadata={"hnsw:space": "cosine"}
    )

    for doc in documents:
        db.add_documents([doc])

    db.persist()
    return db


def answer_question(question: str, retriever=None, model=None, chain=None) -> str:
    if chain is None:
        chain = create_chain(retriever=None, model=None, chain=None)

    return chain.invoke(question)


def create_chain(retriever=None, model=None):
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT)
    return (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
