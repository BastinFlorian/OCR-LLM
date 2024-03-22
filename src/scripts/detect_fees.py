import logging
import os
from typing import Dict, Iterator, List, Tuple
from data.fees_summaries import FEES_SUMMARIES_PATH
from src.lib.utils import df_to_tsv, read_json_from_file, tsv_str_to_df, write_in_json_file
from config.llm import LLM_35, LLM_4
from config.prompt import FEES_TABLE_GENERATOR_PROMPT, SUMMARIZE_PAGE_WITH_FEES_PROMPT
from data.summarized_pages import SUMMARIZED_TEXT_PATH


def summarize_fees_informations(filepath) -> Iterator[Tuple[float, List[str]]]:
    # Extract OCR text page by page
    extracted_texts = []
    summarized_pages_dict = {}
    texts = read_json_from_file(filepath)
    i = 1
    while str(i) in texts.keys():
        extracted_texts.append(texts[str(i)])
        i += 1

    batch_number = len(extracted_texts)
    for it, extracted_text in enumerate(extracted_texts):
        prompt = SUMMARIZE_PAGE_WITH_FEES_PROMPT.format(text=extracted_text)
        result = LLM_35.invoke(prompt).content
        summarized_pages_dict[str(it + 1)] = result
        logging.warning(
            f"PAGE {it + 1}: \n {extracted_text}, \n PROMPT: {prompt} \n RES: {result} \n")

        yield it / batch_number, result

    write_in_json_file(
        data=summarized_pages_dict,
        filepath=os.path.join(SUMMARIZED_TEXT_PATH, os.path.basename(filepath))
    )


def batch_summarize_fees_informations(filepath, batch_size=1) -> Iterator[Tuple[float, List[str]]]:
    improved_texts = {}
    texts = read_json_from_file(filepath)
    i = 1
    extracted_texts = []
    while str(i) in texts.keys():
        extracted_texts.append(texts[str(i)])
        i += 1

    prompts = [SUMMARIZE_PAGE_WITH_FEES_PROMPT.format(
        text=extracted_text) for extracted_text in extracted_texts]
    batches_prompts = [prompts[i:i + batch_size]
                       for i in range(0, len(prompts), batch_size)]
    batch_number = len(batches_prompts)

    for i, batch_prompts in enumerate(batches_prompts):
        if batch_size == 1:
            results: List[str] = [LLM_35.invoke(batch_prompts).content]
            for j, res in enumerate(results):
                logging.warning(i * batch_size + j + 1)
                improved_texts[i * batch_size + j + 1] = res
            yield i / batch_number, results
        else:
            results: List[str] = [
                answer.content for answer in LLM_35.batch(batch_prompts)
            ]
            for j, res in enumerate(results):
                logging.warning(i * batch_size + j + 1)
                improved_texts[i * batch_size + j + 1] = res
                logging.warning(res)
            yield i / batch_number, "\n \n \n".join(
                [
                    f"PAGE {i * batch_size + j + 1}: {result}" for j, result in enumerate(results)
                ]
            )
            logging.warning

    logging.warning("IMPROVED_TEXT", improved_texts)
    write_in_json_file(
        data=improved_texts,
        filepath=os.path.join(SUMMARIZED_TEXT_PATH, os.path.basename(filepath))
    )


def generate_fees_table_from_summarized_pages(filepath: str) -> str:
    summarized_pages_dict: Dict[str, str] = read_json_from_file(filepath)
    summarized_pages_text = "\n".join(
        f"PAGE {page_number}: \n {page_text}" for page_number, page_text in summarized_pages_dict.items()
    )
    logging.warning(summarized_pages_text)
    prompt = FEES_TABLE_GENERATOR_PROMPT.format(
        text=summarized_pages_text
    )
    fees_summary: str = LLM_4.invoke(prompt).content
    df = tsv_str_to_df(fees_summary)
    filepath = os.path.join(
        FEES_SUMMARIES_PATH, os.path.basename(filepath).split(".")[0]
    )
    df_to_tsv(df, filepath)
    return df
