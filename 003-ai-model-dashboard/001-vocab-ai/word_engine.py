from ocr.naver_ocr import naver_ocr
from rag_pipeline.wiktionary_client import wiktionary_pipeline
from rag_pipeline.text_cleaner import process_wikitext
from model_generators.gpt_model import get_gpt_response


word = "prominent"
etymology = wiktionary_pipeline(word)
print("wiktionary에서 어원을 크롤링했습니다.")

etymology = process_wikitext(etymology)
print("어원 전처리가 끝났습니다.")

word = "prominent (눈에 띄는)"
word_info = get_gpt_response(word, etymology)
print("영어 단어장1을 완성했습니다.")

print(word_info.get("pun"))
print(word_info.get("root_components"))
print(word_info.get("root_story"))