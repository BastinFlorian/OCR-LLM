
import os
from typing import Iterator, Tuple
from data.pdfs.splitted import SPLITTED_PDF_PATH
from data.extracted_texts import EXTRACTED_TEXT_PATH
from src.lib.utils import split_pdf_pages, write_in_json_file
from src.lib.ocr import OCRDocumentAI

PROJECT_ID = "acn-gcp-octo-sas"
LOCATION = "eu"  # Format is "us" or "eu"
PROCESSOR_DISPLAY_NAME = "basf-accor-avv"


def document_ai_ocr_from_pdf(pdf_path: str) -> Iterator[Tuple[str, float]]:
    """ We apply the following steps:
    - Split the PDF into individual pages
    - Compute the OCR for each page
    - Concatenate the OCR outputs into a single text file
    Parameters
    ----------
    pdf_path : str
        The filepath of the PDF to process
    text_output_filepath : str
        The text output file to save
    """
    # Split PDF by page because Document AI max page size is 15 pages
    document_ai_handler = OCRDocumentAI()
    split_pdf_pages(pdf_path, SPLITTED_PDF_PATH)
    pdf_filename = os.path.basename(pdf_path)
    splitted_pdf_directory = os.path.join(
        SPLITTED_PDF_PATH, pdf_filename.split(".")[0])

    # Process each page of the PDF in the good order
    i = 0
    extracted_text: dict = {}
    pdf_page_path = f"{splitted_pdf_directory}/page_{i}.pdf"
    page_number = len(os.listdir(splitted_pdf_directory))
    while os.path.isfile(pdf_page_path):
        print(f"Processing {pdf_page_path}: page {i}")
        page_text = document_ai_handler.process_pdf(pdf_page_path)
        extracted_text["page_" + str(i)] = page_text
        i += 1
        pdf_page_path = f"{splitted_pdf_directory}/page_{i}.pdf"
        yield page_text, i / page_number

    # Save extracted text in a txt file
    write_in_json_file(extracted_text, os.path.join(
        EXTRACTED_TEXT_PATH, pdf_filename.split(".")[0]))


if __name__ == "__main__":
    pass
