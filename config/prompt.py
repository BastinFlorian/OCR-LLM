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
    Always write the title of the section from which you extracted the informations.
    Your summary should look like:
    -------
    Page number: [The page number]
    Title of the section: [The title of the section]
    The fees informations are: [The fees informations]
    -------
    The PDF hotel contract page is
    -------
    {text}
    -------
"""

FEES_TABLE_GENERATOR_PROMPT = """
    You are responsible of generating a fees table from the summarized pages.
    Create a CSV table with the following columns: "Type of fees", "Basis", "VAT on basis", "Currency", "Amount",
    "Agreement Clause", "Pages Number used to answer",
    The "Type of fees" column can be one of the following: "Entrance Fee", "Franchise fee", "Distribution fee",
    "Sales & Marketing fee", "Trademark Royalty fee", "Technology fee".
    The "Basis" column can be one of the following: "Gross Revenue", "Net Revenue", "Room Revenue", "Total Revenue"
    or any other revenue basis found.
    The "VAT on basis" column MUST be ONLY "Include" of "Exlude" or empty if the information is not found.
    The "Agreement Clause" provides explanation about the fees.
    The pages number are given at the beginning of the each summarize pages by "Page [page_number]".
    Informations about the fees can be found in Appendix or Schedule.
    If the documents states to refer to the Appendix, get the informations from the appendix and
    fill it in the appropriate table row fee.
    If an information is not specified, leave the cell empty.
    -------
    {text}
    -------
"""


RAG_PROMPT = """Answer the question based only on the following context:
    {context}
    Question: {question}
"""
