import os
from typing import Dict, Iterator, List, Tuple
from data.fees_summaries import FEES_SUMMARIES_PATH
from src.lib.utils import csv_str_to_df, df_to_csv, read_json_from_file, write_in_json_file
from config.llm import LLM_35, LLM_4
from config.prompt import FEES_TABLE_GENERATOR_PROMPT, SUMMARIZE_PAGE_WITH_FEES_PROMPT
from data.summarized_pages import SUMMARIZED_TEXT_PATH


def summarize_fees_informations(filepath, batch_size=10) -> Iterator[Tuple[float, List[str]]]:
    improved_texts = []
    texts = read_json_from_file(filepath)
    prompts = [SUMMARIZE_PAGE_WITH_FEES_PROMPT.format(
        text=text) for text in texts.values()]
    batches_prompts = [prompts[i:i + batch_size]
                       for i in range(0, len(prompts), batch_size)]
    batch_number = len(batches_prompts)

    for i, prompts in enumerate(batches_prompts):
        if batch_size == 1:
            results: List[str] = [LLM_35.invoke(prompts).content]
            improved_texts.append(results)
            yield i / batch_number, results
        else:
            results: List[str] = [
                answer.content for answer in LLM_35.batch(prompts)
            ]
            improved_texts.extend(results)
            yield i / batch_number, "\n \n \n".join(
                [
                    f"PAGE {i * batch_size + j}: {result}" for j, result in enumerate(results)
                ]
            )

    write_in_json_file(
        data={i: text for i, text in enumerate(improved_texts)},
        filepath=os.path.join(SUMMARIZED_TEXT_PATH, os.path.basename(filepath))
    )


def generate_fees_table_from_summarized_pages(filepath: str) -> str:
    summarized_pages_dict: Dict[str, str] = read_json_from_file(filepath)
    summarized_pages_text = "\n".join(
        f"Page {page_number}: \n {page_text}" for page_number, page_text in summarized_pages_dict.items()
    )
    prompt = FEES_TABLE_GENERATOR_PROMPT.format(
        text=summarized_pages_text
    )
    fees_summary: str = LLM_4.invoke(prompt).content
    df = csv_str_to_df(fees_summary)
    filepath = os.path.join(
        FEES_SUMMARIES_PATH, os.path.basename(filepath).split(".")[0]
    )
    df_to_csv(df, filepath)
    return df
