from uuid import uuid4

def store(
    embedded_dataset: list,
    collection
):
    
    for data in embedded_dataset:
        word = data.get("word")
        meaning = data.get("meaning")
        embedded_word = data.get("embedded_word")
        embedded_meaning = data.get("embedded_meaning")

        collection.add(
            ids=[str(uuid4())],            # 영어 단어 id
            embeddings=[embedded_word],    # 단어 embedding
            documents=[word],              # 문서: 원문 단어
            metadatas=[{
                "type": "word",
                "word": word,
                "meaning": meaning,
                "source": "english"
            }]
        )

        collection.add(
            ids=[str(uuid4())],
            embeddings=[embedded_meaning],
            documents=[meaning],
            metadatas=[{
                "type": "meaning",
                "word": word,
                "meaning": meaning,
                "source": "korean"
            }]
        )