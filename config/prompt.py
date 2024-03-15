IMPROVE_OCR_PROMPT = """
    You are responsible of improving the OCR detection of the text extracted from the PDF.
    If the text is not in a good order, because multiple colums or tables, improve the structure.
    You can create a table from the text, or split the text into multiple columns.
    If the text make sence and contains reliable sentences, rewrite the text.
    The following text is:
    -------
    {text}
    -------
"""

SUMMARIZE_PAGE_WITH_FEES_PROMPT = """
    You help the hotel company to detect fees values from a subpart of a PDF hotel contract.
    Extract all the fees informations from the following PDF page. Summarize in a few sentences the fees informations
    with numerical values if present.
    If no fees or details about fees are present, write "".
    The PDF hotel contract page is
    -------
    {text}
    -------
"""

FEES_TABLE_GENERATOR_PROMPT = """
    You are responsible of generating a fees table from the summarized pages.
    Create a markdown table with the following columns: "Fees type", "Fees value", "Pages Number used to answer",
    "Description of the fees and the percentage and amout include tax information".
    The pages number are given at the beginning of the each summarize pages by "Page [page_number]".
    -------
    {text}
    -------
"""


RAG_PROMPT = """Answer the question based only on the following context:
    {context}
    Question: {question}
"""
