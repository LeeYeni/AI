from dotenv import load_dotenv
import os
import base64
import uuid, time
import requests, json
import re

load_dotenv()

NAVER_OCR_SECRET_KEY=os.getenv("NAVER_OCR_SECRET_KEY")
NAVER_OCR_URL=os.getenv("NAVER_OCR_URL")



def naver_ocr(image):
    # 이미지 읽어서 base64 인코딩
    img_base64 = base64.b64encode(image).decode("utf-8")

    payload = {
        "version": "V2",
        "requestId": str(uuid.uuid4()),
        "timestamp": int(time.time() * 1000),
        "images": [{
            "format": "png",
            "name": "eng_word_ocr",
            "data": img_base64
        }]
    }

    # 헤더
    headers = {
        "X-OCR-SECRET": NAVER_OCR_SECRET_KEY,
        "Content-Type": "application/json"
    }

    # 요청
    response = requests.post(NAVER_OCR_URL, json=payload, headers=headers)
    data = response.json()

    fields = data["images"][0]["fields"]

    lines = []
    current_line = []

    for f in fields:
        current_line.append(f["inferText"])

        if f.get("lineBreak"):
            lines.append(" ".join(current_line))
            current_line = []

    if current_line:
        lines.append(" ".join(current_line))

    text = "\n".join(lines)

    return text