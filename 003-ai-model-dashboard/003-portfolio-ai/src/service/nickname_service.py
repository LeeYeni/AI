from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser

from src.database.valkey import get_valkey_db

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
방문자가 기분 좋게 방명록을 남길 수 있도록 위트 있고, 따뜻하며, 개발자스러운 센스가 섞인 닉네임을 5개 생성합니다.

### 가이드라인
* 구성: [기분 좋은 형용사] + [IT/개발자 관련 명사] 조합을 선호합니다.
* 분위기: 긍정적, 다정한, 유머러스한 느낌이어야 합니다.
* 금지: 부정적인 단어, 공격적인 표현, 너무 딱딱한 표현은 피해야 합니다.
* 한글로 작성하세요.


### 출력 형식
{
    "nickname": [
        "닉네임1",
        "닉네임2",
        ...,
        "닉네임5"
    ]
}
"""

user_message = """
닉네임:
"""

async def generate_and_save_nicknames():
    """
    닉네임을 5개 생성하여, Valkey의 nickname_pool에 저장합니다.
    """
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message),
    ]
    
    response = await chain.ainvoke(messages)
    nicknames = response.get("nickname", [])

    with get_valkey_db() as redis_client:
        # sadd를 사용하여 중복 없이 저장(set 자료구조)
        redis_client.sadd("nickname_pool", *nicknames)

async def get_nickname_from_pool():
    """
    Valkey에서 닉네임 하나를 무작위로 꺼냅니다.
    남은 닉네임 개수가 5개 미만이라면, 닉네임을 더 생성하여 채워넣습니다.
    """
    with get_valkey_db() as redis_client:
        nickname = redis_client.spop("nickname_pool")

        current_count = redis_client.scard("nickname_pool")
        if current_count < 5:
            await generate_and_save_nicknames()
        
        if not nickname:
            nickname = redis_client.spop("nickname_pool") or "익명의 개발자"

        return nickname