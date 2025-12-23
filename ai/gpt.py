import time
import traceback
import types

from ui import log
from data import text_data
from data import content_data
from collections import deque

from openai import OpenAI

model_4o = "gpt-4o-mini"
model_5o = "gpt-5o-mini"
api_key = ""

title_list = deque(maxlen=20)
client = None

def init_gpt():
    global client, api_key

    # 테스트 용도로 주석처리
    # api_key = "AIzaSyAIZqqE6WCo4rSzHuRtAvkUkLf8mft4FN8"
    api_key = text_data.TextData().get_api_number()

    client = OpenAI(api_key=api_key)

def create_title_4o(titles, address, company, place):
    global title_list, model_4o, client

    last_exception = None

    contents = content_data.ContentData()
    titles_str = "\n".join(titles)

    if not place:
        place = "신공간 설비업체"

    system_prompt = """
                    너는 마케팅 AI가 아니라 규칙을 엄격히 집행하는 자동 생성 엔진이다.
                    아래 규칙을 어기면 실패다.
                    추론하거나 해석하지 말고 문자 그대로 지켜라.
                    """

    user_prompt = f"""
                    주소 키워드: {address}
                    업종 키워드: {company}
                    회사명: {place}
                    
                    [상위 노출 제목 10개]
                    {titles_str}
                    
                    [금지 내용]
                    {contents.get_ai_detail(company)}
                    {contents.get_ai_common()}
                    
                    [이미 생성된 제목 리스트]
                    {title_list}
                    
                    [규칙]
                    1. 제목은 반드시 한 줄
                    2. 마크다운 문법 금지
                    3. 제목 길이 25~40자
                    4. 회사명은 반드시 "{place}"
                    5. 기존 제목과 문장 구조 및 앞부분 중복 금지
                    6. 문장형/정보형/후기형/긴급형 중 하나
                    7. 네이버 정책 준수
                    8. 제목 외 다른 텍스트 출력 금지
                    
                    위 규칙을 모두 지켜 제목 하나만 출력하라.
                    """

    for i in range(5):
        try:
            response = client.responses.create(
                model=model_4o,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.4,  # ⭐ 낮음
                max_output_tokens=100,
            )
            title = response.output_text.strip()
            title_list.append(title)
            return title

        except Exception:
            if i == 4:
                raise
            time.sleep(60)

    raise RuntimeError("GPT-4o-mini 제목 생성 실패") from last_exception

def create_title_5o(titles, address, company, place):
    global title_list, client, model_5o

    last_exception = None

    contents = content_data.ContentData()
    titles_str = "\n".join(titles)

    if not place:
        place = "신공간 설비업체"

    system_prompt = """
                    너는 창의적인 AI가 아니다.
                    규칙을 어기면 즉시 실패로 간주된다.
                    판단, 추론, 최적화, 의도 해석을 금지한다.
                    """

    user_prompt = f"""
                    절대 규칙을 해석하지 마라.
                    아래 조건 중 하나라도 어기면 실패다.
                    
                    주소: {address}
                    업종: {company}
                    회사명: {place}
                    
                    [상위 제목]
                    {titles_str}
                    
                    [금지 사항]
                    {contents.get_ai_detail(company)}
                    {contents.get_ai_common()}
                    
                    [기존 생성 제목]
                    {title_list}
                    
                    [출력 규칙]
                    - 한 줄
                    - 25~40자
                    - 마크다운 금지
                    - 회사명은 "{place}"
                    - 기존 제목과 앞부분 구조 중복 금지
                    - 네이버 정책 준수
                    - 제목 외 텍스트 출력 금지
                    
                    규칙을 모두 만족하는 제목 하나만 출력하라.
                    """

    for i in range(5):
        try:
            response = client.responses.create(
                model=model_5o,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.25,  # ⭐ 더 낮음
                max_output_tokens=100,
            )
            title = response.output_text.strip()
            title_list.append(title)
            return title

        except Exception:
            if i == 4:
                raise
            time.sleep(60)

    raise RuntimeError("GPT-5o-mini 제목 생성 실패") from last_exception

def create_content_4o(contents, address, company, place):
    global client, model_4o

    last_exception = None
    content_ai = content_data.ContentData()

    if not place:
        place = "신공간 설비업체"

    system_prompt = """
    너는 마케팅 AI가 아니라 규칙을 엄격히 집행하는 자동 생성 엔진이다.
    아래 규칙을 어기면 실패다.
    추론하거나 해석하지 말고 문자 그대로 지켜라.
    """

    user_prompt = f"""
    주소 키워드: {address}
    업종 키워드: {company}
    회사명: {place}

    [예시 글 1]
    {contents[0]}

    [예시 글 2]
    {contents[1]}

    [금지 내용]
    {content_ai.get_ai_detail(company)}
    {content_ai.get_ai_common()}

    [규칙]
    1. 마크다운 문법 사용 금지
    2. %사진% 을 정확히 10번 포함
    3. 사진 설명 텍스트 작성 금지
    4. 전체 분량 약 1000자
    5. 문장 끝(. ? !)마다 줄바꿈
    6. 문단 종료 시 줄바꿈 2번
    7. 연락처, 주소, 홈페이지 언급 금지
    8. 회사명은 반드시 "{place}"만 사용
    9. 네이버 정책 준수
    10. 본문 외 다른 텍스트 출력 금지

    위 규칙을 모두 지켜 본문만 출력하라.
    """

    for i in range(5):
        try:
            response = client.responses.create(
                model=model_4o,          # gpt-4o-mini
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.8,
                max_output_tokens=1500,
            )

            return response.output_text.strip()

        except Exception as e:
            last_exception = e
            if i == 4:
                raise
            time.sleep(60)

    raise RuntimeError("GPT-4o-mini 본문 생성 실패") from last_exception
