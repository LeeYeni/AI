from ocr_pipeline import ocr_pipeline
from embeddings.embed_pipeline import embed_pipeline
from vocab_ingest_pipeline import vocab_ingest_pipeline
from etymology_pipeline import etymology_pipeline

def main_pipeline(img: bytes):
    # --- 1. 단어장 이미지 -> 단어 정보(텍스트) ---
    words_dataset = ocr_pipeline(img)

    # --- 2. 단어 정보(텍스트) -> 임베딩 ---
    # embedded_dataset = embed_pipeline(words_dataset)

    # --- 3. 임베딩 데이터 -> vector DB에 저장 ---
    # vocab_ingest_pipeline(embedded_dataset)

    # --- 4. 어원 추출 ---
    etymology_dataset = etymology_pipeline(words_dataset)

    return etymology_dataset