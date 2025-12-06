import re

def ko_normalize(text: str) -> str:
    text = text.strip()
    text = re.sub(r"[^가-힣\s]", "", text)
    return text

def en_normalize(text: str) -> str:
    text = re.sub(r"[^A-Za-z\s'.-]", "", text)
    text = text.lower().strip()
    return text