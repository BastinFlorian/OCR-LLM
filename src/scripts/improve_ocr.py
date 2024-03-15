import os
from typing import Iterator, List, Tuple
from src.lib.utils import read_json_from_file, write_in_json_file
from config.llm import LLM_35
from config.prompt import IMPROVE_OCR_PROMPT
from data.improved_texts import IMPROVED_TEXT_PATH


def enhance_ocr_using_gpt_3_5(filepath, batch_size=10) -> Iterator[Tuple[float, List[str]]]:
    improved_texts = []
    texts = read_json_from_file(filepath)
    prompts = [IMPROVE_OCR_PROMPT.format(text=text) for text in texts.values()]
    batches_prompts = [prompts[i:i + batch_size] for i in range(0, len(prompts), batch_size)]
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
            yield i / batch_number, results

    write_in_json_file(
        data={i: text for i, text in enumerate(improved_texts)},
        filepath=os.path.join(IMPROVED_TEXT_PATH, os.path.basename(filepath))
    )
