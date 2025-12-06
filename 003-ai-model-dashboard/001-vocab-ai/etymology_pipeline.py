from data_sources.wiktionary_client import wiktionary_pipeline
from model_generators.finetuned_gpt_model import get_gpt_response
from model_generators.base_gpt_model import base_gpt_model
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_prompt_template():
    with open ("prompts/extract_etymology.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()
    
    return prompt_template

def aggregate_meanings(words_dataset: list):
    unique_words_dict = {}

    for data in words_dataset:
        word = data.get("word")
        meaning = data.get("meaning")

        if word not in unique_words_dict:
            unique_words_dict[word] = []
        
        unique_words_dict[word].append(meaning)

    return [
        {"word": word, "meanings": ", ".join(meanings)}
        for word, meanings in unique_words_dict.items()
    ]


def process_single_item(data):
    word = data.get("word")
    meanings = data.get("meanings")

    if " " in word:
        return {
            "word": word,
            "meanings": meanings,
            "root_components": None,
            "root_story": None
        }

    wikitext = wiktionary_pipeline(word)
    prompt_template = get_prompt_template()

    if wikitext is None:
        return {
            "word": word,
            "meanings": meanings,
            "root_components": None,
            "root_story": None
        }

    etymology = base_gpt_model(prompt_template, params={"text": wikitext})
    response = get_gpt_response(word, meanings, etymology)

    return {
        "word": word,
        "meanings": meanings,
        "root_components": response.get("root_components"),
        "root_story": response.get("root_story")
    }

def etymology_pipeline(words_dataset: list):
    words_dataset = aggregate_meanings(words_dataset)

    etymology_dataset = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        part_of_dataset = [executor.submit(process_single_item, data) for data in words_dataset]

        for data in as_completed(part_of_dataset):
            etymology_dataset.append(data.result())
    
    return etymology_dataset