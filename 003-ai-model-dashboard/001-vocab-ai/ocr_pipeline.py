from ocr.naver_ocr import naver_ocr
from model_generators.base_gpt_model import base_gpt_model
import json, re

# 프롬프트 반환하는 함수
def get_prompt_template(ver=1):
    if ver == 1:
        file_name = "prompts/ocr_to_vocab.txt"
    elif ver == 2:
        file_name = "prompts/expand_vocab_combinations.txt"

    with open(file_name, "r", encoding="utf-8") as f:
        prompt_template = f.read()
    
    return prompt_template

# LLM으로 {word: ~, meaning: ~, synonyms: ~}를 [{word: ~, meaning: ~}...]으로 변환하는 함수
def expand_vocab_combinations_with_llm(word_info):
    word = word_info.get("word")
    synonyms = word_info.get("synonyms")
    meaning = word_info.get("meaning")

    word_info = []
    meanings = meaning.split(";")

    for meaning in meanings:
        meaning = meaning.strip()
        word_info.append({
            "word": word,
            "meaning": meaning
        })

    prompt_template = get_prompt_template(ver=2)

    if not synonyms:
        return word_info
    
    for word in synonyms:
        text = [{"word": word, "meaning": meanings}]
        text = json.dumps(text)

        meaning = base_gpt_model(prompt_template, params={"text": text})
        meaning = meaning.strip()

        word_info.append({
            "word": word,
            "meaning": meaning
        })

    return word_info

# 알고리즘으로 {word: ~, meaning: ~, synonyms: ~}를 [{word: ~, meaning: ~}...]으로 변환하는 함수
def expand_vocab_combinations(word_info):
    word = word_info.get("word")
    synonyms = word_info.get("synonyms")
    meaning = word_info.get("meaning")

    words = []
    words.append(word)

    if synonyms:
        words.extend(synonyms)

    meanings = meaning.split(",")

    # {'word': 'special', 'meaning': '특정한; 특정한'}
            
    word_info = []
    for word in words:
        word = word.strip()

        for meaning in meanings:
            meaning = meaning.strip()
                    
            word_info.append({
                "word": word,
                "meaning": meaning
            })

    return word_info
    
def ocr_pipeline(img: bytes) -> list:
    img_info = naver_ocr(img)
    prompt_template = get_prompt_template(ver=1)
    words_info = base_gpt_model(prompt_template, params={"text": img_info})
    words_info = re.sub(r"^.*?\[", '[', words_info, flags=re.DOTALL)
    words_info = re.sub(r'^(.*\]).*$', r'\1', words_info, flags=re.DOTALL)

    # JSON 리스트로 변환
    words_info = json.loads(words_info)

    words_dataset = []
    unique = set()

    for word_info in words_info:

        if ';' in word_info.get("meaning"):
            word_info = expand_vocab_combinations_with_llm(word_info)
        else:
            word_info = expand_vocab_combinations(word_info)

        for info in word_info:
            key = (info.get("word"), info.get("meaning"))

            if key not in unique:
                words_dataset.append(info)
                unique.add(key)

    return words_dataset