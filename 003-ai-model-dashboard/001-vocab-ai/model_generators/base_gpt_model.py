from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    api_key=API_KEY,
    temperature=0.2,
    max_tokens=6000
)

def base_gpt_model(prompt_template: str, params: dict):
    prompt = prompt_template.replace("{text}", params["text"])

    response = llm.invoke([
        {"role": "system", "content": prompt}
    ])
    return response.content