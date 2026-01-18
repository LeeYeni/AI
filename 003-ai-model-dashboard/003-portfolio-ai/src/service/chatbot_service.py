from dotenv import load_dotenv
import os
import uuid
import json

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser

from src.database.valkey import get_valkey_db

load_dotenv()
API_KEY = os.getenv("OLLAMA_API_KEY")

llm = ChatOpenAI(
    model="gpt-oss:120b-cloud",
    base_url="https://ollama.com/v1",
    api_key=API_KEY
)

chain = llm | JsonOutputParser()

system_message = """
### 역할
당신은 개발자 이예니의 포트폴리오를 안내하고 방문객과 소통하는 "AI 호스트"입니다. 

### 핵심 지침
1. **공감과 반응(Reaction):** 사용자가 자신의 기분, 응원, 혹은 일상적인 이야기를 하면 그에 대해 따뜻하고 위트 있게 반응하세요. (예: "와, 오늘 정말 멋진 하루를 보내셨네요!", "응원 감사합니다. 개발자님께 큰 힘이 될 거예요!")
2. **명확한 설명(Explanation):** 사용자가 기술적인 질문이나 개발자에 대해 궁금한 점을 물으면, 쉽고 명확하게 설명해 주세요. 전문 용어는 친절하게 풀어서 설명합니다.
3. **톤앤매너:** - 친절하고 긍정적인 에너지가 느껴지는 말투를 사용하세요.
   - 너무 로봇 같지 않게, 적절한 이모지(예: ✨, 🚀, 😊)를 섞어 사용하세요.
   - 답변은 핵심 위주로 간결하게 하되, 필요한 경우 상세히 덧붙입니다.

### 금지 사항
- 부정적인 발언이나 비판적인 태도는 지양합니다.
- 모르는 정보에 대해서는 아는 척하지 않고, "그 부분은 제가 확인하기 어렵지만, 개발자님께 꼭 전달해 드릴게요!"라고 답변하세요.

### 출력 언어
- 한국어로 답변하세요.

### 출력 형식
{
    "chatbot_response": "답변"
}
"""

def generate_session_id() -> str:
    """
    사용자 식별을 위한 고유한 세션 Id를 생성합니다.
    """
    return str(uuid.uuid4())

def start_chat() -> dict:
    """
    초기 환영 메시지와 함께 ID 반환
    """
    session_id = generate_session_id()
    return {
        "session_id": session_id,
        "message": "안녕하세요! 이예니님의 포트폴리오 AI 호스트입니다. 무엇을 도와드릴까요? ✨"
    }

async def get_chatbot_response(session_id: str, prompt: str) -> dict:
    """
    Valkey를 연동하여 이전 대화를 기억하고 응답을 생성합니다.
    """
    memory_key = f"chat:memo:{session_id}"

    with get_valkey_db() as redis_client:
        # --- 최근 대화 내역 가져오기 ---
        raw_history = redis_client.lrange(memory_key, 0, -1)
        history = [json.loads(message) for message in raw_history]

        # --- 메시지 리스트 구성하기 ---
        messages = [SystemMessage(content=system_message)]

        for message in history:
            if message["role"] == "user":
                messages.append(HumanMessage(content=message["content"]))
            elif message["role"] == "assistant":
                messages.append(AIMessage(content=message["content"]))
            
        messages.append(HumanMessage(content=prompt))

        # --- 응답 생성 ---
        response = await chain.ainvoke(messages)
        bot_text = response.get("chatbot_response", "오류가 생겼습니다.")

        # --- 대화 내용 저장 ---
        redis_client.rpush(memory_key, json.dumps({"role": "user", "content": prompt}))
        redis_client.rpush(memory_key, json.dumps({"role": "assistant", "content": bot_text}))

        # --- 메모리 최적화 ---
        redis_client.ltrim(memory_key, -10, -1)
        redis_client.expire(memory_key, 3600)

        return {
            "session_id": session_id,
            "message": bot_text
        }