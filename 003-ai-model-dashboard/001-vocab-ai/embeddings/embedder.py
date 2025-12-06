from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=API_KEY
)

# 배치 사이즈로 임베딩
def embedder(words: list, meanings: list):
    embedded_words = embeddings.embed_documents(words)
    embedded_meanings = embeddings.embed_documents(meanings)

    embedded_dataset = []
    for word, meaning, embedded_word, embedded_meaning in zip(words, meanings, embedded_words, embedded_meanings):
        embedded_dataset.append({
            "word": word,
            "meaning":meaning,
            "embedded_word": embedded_word,
            "embedded_meaning": embedded_meaning
        })

    return embedded_dataset