from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()
os.getenv("OLLAMA_API_KEY")

llm = ChatOpenAI(
    model="gpt-oss:120b-cloud",
    base_url="https://ollama.com/v1",
    temperature=0.7,
)

chain = llm | JsonOutputParser()

system_message = """
### 역할
당신은 개발자 [이름]의 포트폴리오를 안내하고 방문객과 소통하는 "AI 호스트"입니다. 

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

async def get_chatbot_response(prompt: str) -> str:
    message = [
        SystemMessage(content=system_message),
        HumanMessage(content=prompt),
    ]

    response = await chain.ainvoke(message)
    return response.get("chatbot_response", "오류가 생겼습니다.")