from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from main_pipeline import main_pipeline
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 루트
@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

# 단어, 뜻 저장 및 단어, 뜻, 어원 반환
@app.post("/words")
async def extract_word(
    image: UploadFile = File(...)
):
    image = await image.read()
    return main_pipeline(image)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)