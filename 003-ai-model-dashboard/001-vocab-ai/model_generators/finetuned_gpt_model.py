import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import json

load_dotenv()

FINETUNED_GPT_MODEL = os.getenv("FINETUNED_GPT_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(
    model=FINETUNED_GPT_MODEL,
    temperature=0.2,
    api_key=OPENAI_API_KEY,
    max_tokens=6000
)

SYSTEM_PROMPT = """
주어진 영어 단어와 뜻을 참고하여, 아래 **3가지 항목을 필수로 포함**하는 JSON 객체를 생성하세요. 이때, 각 항목은 아래의 **구체적인 스타일 및 제약 조건**을 엄격하게 준수해야 합니다.
1. **pun (언어 유희):** 청중을 고려하여 친근하고 매력적인 톤으로, 내용적 제약 없이 창의적인 상황을 자유롭게 활용하여 작성할 것.
2. **root_components (어원/뿌리):** 라틴어, 고대 영어 등 원어와 뜻을 괄호 안에 병기하는 형식을 반드시 따를 것. 여러 단계의 변화는 화살표(`→`)로 연결할 것.
3. **root_story (어원 풀이):** 친근하고 교육적인 톤으로, 어원 요소가 결합하여 현대적 의미를 도출하는 과정을 스토리텔링 형식으로 풀이할 것.
"""

USER_PROMPT1 = """
# pun 관련 추가 지시사항
- pun(언어 유희)는 반드시 **자연스러운 한국어 문장**이어야 합니다.
- USER PROMPT에서 주어진 영어 단어를 한국어식으로 자연스럽게 들리는 소리로 변환할 것.
- 이렇게 변환된 발음을 기반으로, 한국어 단어나 어절처럼 들리도록 창의적으로 재해석할 것.
  (예: ‘한국어 어절처럼 들리는 새로운 표현’으로 변환, ‘비슷한 소리의 다른 한국어 표현’으로 재해석)
- 그 문장이 영어 단어의 실제 의미와 직관적으로 연결되도록 구성할 것.
  → 말장난이 단어의 뜻을 떠올리는 ‘암기 트리거’가 되도록.
- 전체 톤은 가볍고 재치 있으며, 기억에 오래 남는 한국어 문장일 것.
  → 유머, 말장난, 상황 설정 모두 허용하되 억지스럽지는 않게.

# pun 예시 모음
- cancel: “그건… 걍 쓸(cancel) 필요 없겠다. 취소!”
- challenge: “겁내지 말고, 그냥 쳐! 냈지(challenge)? 그럼 그게 도전이지"
- compare: "상대 전략이랑 비교해도, 이건 판을 뒤집을 큰 패여(compare)"
- behave: "남들에 비해 입(behave)이 너무 거칠어. 좀 점잖게 행동해."
- consider: "이건 인생을 건 큰 시도(consider)야... 할지 말지 깊게 고려해봐."
- connect: "누가 전원 끄네? 트(connect)집 잡히기 싫으면, 당장 케이블 다시 연결해."
- depend: "힘들면 내 뒤 편(depend)에 기대! 나한테 의존해"
- contribute: "큰 트리 붙(contribute)들고 있어 봐. 너도 장식하는 데 기여해야지."
- discuss: "머릿속 생각이 막 뒤섞였어(discuss). 앉아서 차근차근 논의하자."
- except: "불량인 이 세트(except)는 빼고 보내. 이것만 제외해."

다음 단어에 대해 SYSTEM_PROMPT의 형식에 따라 JSON 객체를 생성하세요

단어:
\"\"\" 
{word} 
\"\"\"
"""

USER_PROMPT2 = """
\n\n다음은 해당 단어의 어원 원문입니다.
SYSTEM_PROMPT의 형식에 따라 root_components 및 root_story를 생성할 때 참고하세요:

어원 원문:
\"\"\" 
{etymology} 
\"\"\"
"""

USER_PROMPT3 = """
\n\n다음은 해당 단어의 뜻입니다.
SYSTEM_PROMPT의 형식에 따라 root_story를 생성할 때 참고하세요:

뜻:
\"\"\" 
{meanings} 
\"\"\"
"""

def get_gpt_response(word: str, meanings: str, etymology: str):
    USER_PROMPT = USER_PROMPT1.format(word=word) + USER_PROMPT2.format(etymology=etymology) + USER_PROMPT3.format(meanings=meanings)

    response = model.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT}
    ])

    return json.loads(response.content)