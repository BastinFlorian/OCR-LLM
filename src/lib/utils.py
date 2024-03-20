from io import StringIO
import json
import os
import shutil
from typing import Any
from PyPDF2 import PdfWriter, PdfReader
import pandas as pd
import openpyxl


def create_directory_if_not_exists(directory):
    """Create a directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def remove_directory_if_exists(directory):
    """Remove a directory if it exists."""
    if os.path.exists(directory):
        shutil.rmtree(directory)


def split_pdf_pages(input_path, output_dir):
    """Split a PDF into individual pages and save them as separate files."""
    filename = os.path.basename(input_path)
    output_dir = os.path.join(output_dir, filename.split(".")[0])
    input_pdf = PdfReader(open(input_path, "rb"))

    remove_directory_if_exists(output_dir)
    create_directory_if_not_exists(output_dir)

    for i in range(len(input_pdf.pages)):
        output = PdfWriter()
        output.add_page(input_pdf.pages[i])
        with open(os.path.join(output_dir, f"page_{i}.pdf"), "wb") as output_stream:
            output.write(output_stream)


def list_pdf_path_in_directory(directory):
    pdf_paths = []
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            pdf_paths.append(os.path.join(directory, file))
    return pdf_paths


def read_txt_from_file(filepath):
    if not filepath.endswith(".txt"):
        filepath += ".txt"

    with open(filepath, "r") as f:
        return f.read()


def write_in_txt_file(text, filepath):
    if not filepath.endswith(".txt"):
        filepath += ".txt"

    with open(filepath, "w") as f:
        f.write(text)


def write_in_json_file(data: dict[Any, Any], filepath):
    if not filepath.endswith(".json"):
        filepath += ".json"

    json_object = json.dumps(data)
    with open(filepath, "w") as f:
        f.write(json_object)


def read_json_from_file(filepath):
    if not filepath.endswith(".json"):
        filepath += ".json"

    with open(filepath, "r") as f:
        return json.load(f)


def list_json_file_in_directory(directory):
    json_files = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            json_files.append(os.path.join(directory, file))
    return json_files


def list_txt_file_in_directory(directory):
    txt_files = []
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            txt_files.append(os.path.join(directory, file))
    return txt_files


def list_csv_file_in_directory(directory):
    csv_files = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            csv_files.append(os.path.join(directory, file))
    return csv_files


def csv_str_to_df(csv_str: str) -> pd.DataFrame:
    input = StringIO(csv_str)
    return pd.read_csv(input, sep=",")


def df_to_xlsx(df: pd.DataFrame, filepath: str):
    if not filepath.endswith(".xlsx"):
        filepath += ".xlsx"
    df.to_excel(filepath, index=False)


def df_to_csv(df: pd.DataFrame, filepath: str):
    if not filepath.endswith(".csv"):
        filepath += ".csv"
    df.to_csv(filepath, index=False)
