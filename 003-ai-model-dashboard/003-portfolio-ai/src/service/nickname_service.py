from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()
API_KEY = os.getenv("OLLAMA_API_KEY")

llm = ChatOpenAI(
    model="gpt-oss:20b-cloud",
    base_url="https://ollama.com/v1/",
    api_key=API_KEY,
)

chain = llm | JsonOutputParser()

system_message = """
### 역할
당신은 개발자 포트폴리오 방명록 전용 "닉네임 작명가"입니다.

### 수행 방법
방문자가 기분 좋게 방명록을 남길 수 있도록 위트 있고, 따뜻하며, 개발자스러운 센스가 섞인 닉네임을 생성합니다.

### 가이드라인
* 구성: [기분 좋은 형용사] + [IT/개발자 관련 명사] 조합을 선호합니다.
* 분위기: 긍정적, 다정한, 유머러스한 느낌이어야 합니다.
* 금지: 부정적인 단어, 공격적인 표현, 너무 딱딱한 표현은 피해야 합니다.
* 한글로 작성하세요.


### 출력 형식
{
    "nickname": "닉네임",
    "reason": "이 닉네임을 작명한 이유"
}
"""

user_message = """
닉네임:
"""

async def get_nickname() -> str:
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message),
    ]
    
    response = await chain.ainvoke(messages)
    return response.get("nickname", "코딩하는 방문객")