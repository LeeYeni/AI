from embeddings.normalize import ko_normalize, en_normalize
from embeddings.embedder import embedder

def embed_pipeline(text_dataset: list) -> list:
    words = []
    meanings = []

    for data in text_dataset:
        word = data.get("word")
        meaning = data.get("meaning")

        word = en_normalize(word)
        meaning = ko_normalize(meaning)

        words.append(word)
        meanings.append(meaning)

    embedded_dataset = embedder(words, meanings)

    return embedded_dataset