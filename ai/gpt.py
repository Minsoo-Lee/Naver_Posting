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

prev_title = ""
title_list = deque(maxlen=20)
client = None

def init_gpt():
    global client, api_key

    # 테스트 용도로 주석처리
    # api_key = text_data.TextData().get_api_number()

    client = OpenAI(api_key=api_key)


def create_title_4o(titles, address, company, place):
    global title_list, model_4o, client, prev_title
    last_exception = None
    contents = content_data.ContentData()
    titles_str = "\n".join(titles)
    # title_list_value = "\n".join(title_list)
    # title_type = random.choice(title_types)
    # print("title_type = " + title_type)

    if not place:
        place = "신공간 설비업체"

    system_prompt = """
                    너는 판단하거나 추론하지 않는다.
                    규칙을 그대로 따르는 생성기다.
                    조건을 하나라도 어기면 실패다.
                    """

    user_prompt = f"""
                    내가 제목을 작성을 할 거야. 주소 키워드는 {address}, 업종 키워드는 {company}야.
                     한 마디로, 나는 {address} 지역에서 {place}라는 회사를 운영하는데, "홍보 글의 제목"을 작성하고 싶어.
                     내가 수집한 제목 리스트를 보여줄게. 이 리스트들은 상위 노출된 10개 글의 제목들이야.

                     {titles_str}
                     내가 쓰는 글도 상위 노출이 될 수 있게끔 저 리스트들을 참고해서 제목을 하나 작성해 줘.

                     그리고 다음 사항들은 반드시 지켜줘. 하나라도 빼먹으면 안 돼.

                     1. 우리 업체에 관한 내용과 제목에 넣지 말아야 하는 내용은 다음과 같아.

                     {contents.get_ai_detail(company)}
                     {contents.get_ai_common()}

                     너가 넣지 말아야 하는 내용을 넣어버리면 법적 분쟁에 휘말려 큰 손해를 볼 수도 있어. 하지 말라는 내용은 반드시 빼 줘
                     그리고 서비스만 나열하는 방식으로 제목을 생성하지 마.       

                     3. ** 또는 ##와 같은 마크다운 언어는 쓰지 마.
                     제발. 마크다운 언어는 절대 포함하지 마. 어차피 적용 안돼

                     4. 그리고 너가 준 제목으로 바로 포스팅을 할거야. 다른 제목 옵션 주지 말고 그냥 제목 딱 한줄만 넘겨줘.
                     이게 중요해. 다른 제목 옵션 주지 말고 제목 딱 한줄만 넘겨줘 제발.
                     그래야 글이 꼬이지 않아.

                     5. 내가 운영하는 회사 이름은 {place}야. 다른 이상한 이름 쓰지 말고 반드시 내 회사명은 {place}로 소개해 줘.
                        회사 이름 언급은 문장 내 위치를 다양하게 작성해 줘.

                     6. 제목 글자 수는 25-40자 정도로 작성해 줘. 함축적으로 작성해주면 더 좋아.

                     7. 아래 리스트는 지금까지 너가 생성해 준 제목 리스트야. 
                     너가 지금 새로 생성한 제목과 비교해서, 전혀 다른 제목으로 생성해 줘.
                     특히, {address}, {place}, {company}의 위치가 중복되지 않아야 해.

                     {prev_title}

                    """
    for i in range(5):
        try:
            response = client.responses.create(
                model=model_4o,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,  # ⭐ 낮음
                max_output_tokens=100,
                store=False
            )
            title = response.output_text.strip()
            title_list.append(title)
            prev_title = title
            return title

        except Exception as e:
            print(e)
            if i == 4:
                raise
            time.sleep(60)

    raise RuntimeError("GPT-4o-mini 제목 생성 실패") from last_exception

# def create_title_4o(titles, address, company, place):
#     global title_list, model_4o, client
#
#     last_exception = None
#
#     contents = content_data.ContentData()
#     titles_str = "\n".join(titles)
#
#     if not place:
#         place = "신공간 설비업체"
#
#     system_prompt = """
#                     너는 마케팅 AI가 아니라 규칙을 엄격히 집행하는 자동 생성 엔진이다.
#                     아래 규칙을 어기면 실패다.
#                     추론하거나 해석하지 말고 문자 그대로 지켜라.
#                     """
#
#     user_prompt = f"""
#                     주소 키워드: {address}
#                     업종 키워드: {company}
#                     회사명: {place}
#
#                     [상위 노출 제목 10개]
#                     {titles_str}
#
#                     [금지 내용]
#                     {contents.get_ai_detail(company)}
#                     {contents.get_ai_common()}
#
#                     [이미 생성된 제목 리스트]
#                     {title_list}
#
#                     [규칙]
#                     1. 제목은 반드시 한 줄
#                     2. 마크다운 문법 금지
#                     3. 제목 길이 25~40자
#                     4. 회사명은 반드시 "{place}"
#                     5. 기존 제목과 문장 구조 및 앞부분 중복 금지
#                     6. 문장형/정보형/후기형/긴급형 중 하나
#                     7. 네이버 정책 준수
#                     8. 제목 외 다른 텍스트 출력 금지
#
#                     위 규칙을 모두 지켜 제목 하나만 출력하라.
#                     """
#
#     for i in range(5):
#         try:
#             response = client.responses.create(
#                 model=model_4o,
#                 input=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt},
#                 ],
#                 temperature=0.4,  # ⭐ 낮음
#                 max_output_tokens=100,
#             )
#             title = response.output_text.strip()
#             title_list.append(title)
#             return title
#
#         except Exception:
#             if i == 4:
#                 raise
#             time.sleep(60)
#
#     raise RuntimeError("GPT-4o-mini 제목 생성 실패") from last_exception

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
    내가 글을 쓸건데, 주소 키워드는 {address}, 업종 키워드는 {company}야.
                그리고 '{place}'라는 회사를 운영하고 있어.
                예시 글들을 보여줄게.

                예시 1:
                {contents[0]}

                예시 2:
                {contents[1]}

                그리고 다음 사항들은 반드시 지켜줘. 하나라도 빼먹으면 안 돼.

                1. 우리 업체에 관한 내용과 본문에 넣지 말아야 하는 내용은 다음과 같아.

                {content_ai.get_ai_detail(company)}
                {content_ai.get_ai_common()}

                너가 넣지 말아야 하는 내용을 넣어버리면 법적 분쟁에 휘말려 큰 손해를 볼 수도 있어. 하지 말라는 내용은 반드시 빼 줘.

                2. ** 또는 ##와 같은 마크다운 언어는 쓰지 마.
                제발. 마크다운 언어는 절대 포함하지 마. 어차피 적용 안돼

                3. 중간에 사진을 10장 넣을 건데, 너가 생성한 글에서 사진을 넣을 만한 장소에 %사진% 이라고 써 주고, 1000자 내외의 글로 작성해 줘.
                반드시 사진을 10장 넣게 해 줘야 해. 꼭.
                사진이 들어가는 공간은 문맥을 해치지 말아야 해.
                그리고 사진에 대한 설명을 적으면 글을 파싱하기 어려우니까, 사진에 대한 설명은 반드시 빼 줘.

                4. 문장이 . ? ! 이런 끝맺음 기호로 끝날 때마다 줄바꿈은 꼭 해줘야 해.
                그리고 하나의 문단이 끝날 때마다 줄바꿈은 두 번 해줘.

                5. 연락처, 주소, 홈페이지 같은 정보는 적지 않아도 돼

                6. 내가 운영하는 회사 이름은 {place}야. 다른 이상한 이름 쓰지 말고 반드시 내 회사명은 {place}로 소개해 줘.

                7. 네이버 정책에 맞는 본문을 생성해 줘.

                8. 가독성을 더 높이기 위해 이모지를 적절하게 활용해 줘

                지금까지 얘기한 7가지 요구사항들은 꼭 지켜줘. 하나도 빠짐없이 7개 다 지켜줘야 해.
                만약에 이 중 하나라도 빠진 부분이 있다면 처음부터 다시 생성해 줘.
    """

    for i in range(5):
        try:
            response = client.responses.create(
                model=model_4o,  # gpt-4o-mini
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_output_tokens=1500,
            )

            return response.output_text.strip()

        except Exception as e:
            print(e)
            last_exception = e
            if i == 4:
                raise
            time.sleep(60)

    raise RuntimeError("GPT-4o-mini 본문 생성 실패") from last_exception

# def create_content_4o(contents, address, company, place):
#     global client, model_4o
#
#     last_exception = None
#     content_ai = content_data.ContentData()
#
#     if not place:
#         place = "신공간 설비업체"
#
#     system_prompt = """
#     너는 마케팅 AI가 아니라 규칙을 엄격히 집행하는 자동 생성 엔진이다.
#     아래 규칙을 어기면 실패다.
#     추론하거나 해석하지 말고 문자 그대로 지켜라.
#     """
#
#     user_prompt = f"""
#     주소 키워드: {address}
#     업종 키워드: {company}
#     회사명: {place}
#
#     [예시 글 1]
#     {contents[0]}
#
#     [예시 글 2]
#     {contents[1]}
#
#     [금지 내용]
#     {content_ai.get_ai_detail(company)}
#     {content_ai.get_ai_common()}
#
#     [규칙]
#     1. 마크다운 문법 사용 금지
#     2. %사진% 을 정확히 10번 포함
#     3. 사진 설명 텍스트 작성 금지
#     4. 전체 분량 약 1000자
#     5. 문장 끝(. ? !)마다 줄바꿈
#     6. 문단 종료 시 줄바꿈 2번
#     7. 연락처, 주소, 홈페이지 언급 금지
#     8. 회사명은 반드시 "{place}"만 사용
#     9. 네이버 정책 준수
#     10. 본문 외 다른 텍스트 출력 금지
#     11. 가독성 좋게 작성할 것.
#
#     위 규칙을 모두 지켜 본문만 출력하라.
#     """
#
#     for i in range(5):
#         try:
#             response = client.responses.create(
#                 model=model_4o,          # gpt-4o-mini
#                 input=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt},
#                 ],
#                 temperature=0.8,
#                 max_output_tokens=1500,
#             )
#
#             return response.output_text.strip()
#
#         except Exception as e:
#             last_exception = e
#             if i == 4:
#                 raise
#             time.sleep(60)
#
#     raise RuntimeError("GPT-4o-mini 본문 생성 실패") from last_exception
