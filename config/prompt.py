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
    You will be given a piece of text that is extracted from a PDF. Detect if there are fees informations in this text.
    If there are fees informations, summarize in a few sentences the fees informations with numerical values if present
    and add the title of the section at the beginning of the summary.
    If there is no fee information, just say 'No fee information provided'. You MUST not try to make up an answer.
    The important informations to extract ONLY IF they are mentioned in the text are the type of fees, the basis,
    the VAT on basis, the currency, the fixed amount or the percentage of fees per year, and the agreement clause.
    The text where you can find fees is:
    -------
    {text}
    -------
"""

FEES_TABLE_GENERATOR_PROMPT = """
    You are responsible of generating a fees table from the summarized pages.
    Create a TSV table with the following columns: "Type of fees", "Basis", "VAT on basis", "Currency", "Fixed",
    "Year 1", "Year 2", "Year 3", "Year 4", "Year 5+", "Agreement Clause", "Pages Number used to answer".
    The "Fixed" value is the fixed amount of the fee. If the fee is a percentage, leave the cell empty and
    fill the "Years" columns with the percentage value per year.
    The "Type of fees" column can be one of the following: "Entrance fee", "Franchise fee", "Distribution fee",
    "Sales & Marketing fee", "Trademark Royalty fee", "Technology fee".
    The "Basis" column can be one of the following: "Net Revenue", "Gross Room Revenue", "Total Revenue", "Room Revenue"
    or any other revenue basis found.
    The "Currency" column can be one of the following: "USD", "EUR", "GBP".
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
