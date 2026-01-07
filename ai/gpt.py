import random
import time
from data import text_data, const
from data import content_data
from collections import deque

from openai import OpenAI

model_4o = "gpt-4o-mini"
model_5o = "gpt-5o-mini"
api_key = ""

prev_title = ""
title_list = deque(maxlen=20)
client = None

title_types = ["후기형", "문장형", "긴급형", "정보형"]

def get_title_ex(address, company, place, key, index):
    title_type_ex = {
        "정보형": [
            f"1.{address} 지역에서 {company} 점검이 필요한 주요 상황 정리, {place}",
        f"2.	{company} 공사가 필요한 신호를 {address} 사례로 정리한 {place} 안내",
        f"3.	{address} 현장에서 자주 발생하는 {company} 문제와 해결 방향, {place}",
        f"4.	{company} 작업 전 알아두면 좋은 기준을 {address} 기준으로 정리한 {place}",
        f"5.	{address} 기준으로 살펴본 {company} 점검과 공사 흐름, {place}]"],
        "긴급형": [
            f"1.	갑작스러운 문제 발생 시 {address}에서 필요한 {company} 대응, {place}",
        f"2.	방치하면 커지는 {company} 문제, {address}에서 빠른 대응이 필요한 이유와 {place}",
        f"3.	예상치 못한 고장 상황에서 {address} {company} 조치가 중요한 이유, {place}",
        f"4.	반복되는 증상이라면 {address}에서 즉시 확인해야 할 {company}, {place}",
        f"5.	긴급 조치가 필요한 {company} 상황을 {address} 기준으로 정리한 {place}"
        ],
        "후기형": [
        f"1.	작업 이후 달라진 현장 상태, {address} {company} 진행 후 {place} 정리",
        f"2.	공사 완료 후 확인된 변화, {address} {company} 작업 결과와 {place}",
        f"3.	실제 작업을 마친 뒤 느낀 차이, {address} {company} 경험 정리 {place}",
        f"4.	시공 후 관리가 편해진 이유, {address} {company} 작업과 {place}",
        f"5.	작업 전후 비교로 본 변화, {address} {company} 진행 결과 {place}"
        ],
        "문장형": [
        f"1.	{address}에서 신중한 {company} 진행이 중요한 이유를 설명하는 {place}",
        f"2.	안정적인 환경을 위해 {address}에서 선택되는 {company}, {place}",
        f"3.	오래 쓰기 위해 고려해야 할 {company}, {address} 기준으로 보는 {place}",
        f"4.	환경에 맞는 {company} 선택이 중요한 {address} 현장과 {place}",
        f"5.	관리 부담을 줄이기 위한 {address} {company} 방향을 제시하는 {place}"
        ]
    }

    return title_type_ex[key][index]

def init_gpt():
    global client, api_key

    # 테스트 용도로 주석처리
    api_key = text_data.TextData().get_api_number()
    client = OpenAI(api_key=api_key)

def create_title_4o_legacy(titles, address, company, place):
    global title_list, model_4o, client, prev_title
    last_exception = None
    contents = content_data.ContentData()
    titles_str = "\n".join(titles)
    keyword_order = [address, company, place]
    random.shuffle(keyword_order)

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
                     
                     7. 키워드들의 순서는 다음과 같이 해 줘.
                     
                     {keyword_order[0]}, {keyword_order[1]}, {keyword_order[2]}

                     8. 아래 리스트는 지금까지 너가 생성해 준 제목 리스트야. 
                     너가 지금 새로 생성한 제목과 비교해서, 전혀 다른 제목으로 생성해 줘.

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

def create_title_4o(title, address, company, place):
    global title_list, model_4o, client, prev_title
    last_exception = None
    random.shuffle(title)
    contents = content_data.ContentData()

    title_key = title_types[random.randint(0, len(title_types) - 1)]
    title_index = random.randint(0, 4)
    title_template = get_title_ex(address, company, place, title_key, title_index)

    if not place:
        place = "신공간 설비업체"

    system_prompt = """
                        너는 홍보 글을 제공하는 마케터야.
                        내가 알려주는 규칙을 반드시 지키며 제목을 생성해 줘.
                        """

    user_prompt = f"""
                        반드시 아래 내용을 지켜서 홍보 글을 생성하라.
                        지역: {address}
                        업종: {company}
                        상호명: {place}

                        [회사에 관한 내용과 넣지 말아야 하는 내용 - 법적 분쟁에 휘말릴 수 있으니 넣지 말아야 하는 내용은 반드시 뺼 것]

                        {contents.get_ai_detail(company)}
                        {contents.get_ai_common()}

                        [이전에 생성한 제목 - 문장 구조를 이전 제목과 공유하지 말 것]

                        {prev_title}

                         1. 마크다운 언어 사용 금지
                         2. 추가 옵션 외에 제목 한 줄만 응답
                         3. 제목 글자 수는 25-40자
                         4. 아래 제목 템플릿을 활용하여 새로운 제목을 생성할 것.
                         {title_template}
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

def create_content_4o_legacy(contents, address, company, place):
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

def create_content_4o(content, address, company, place):
    global client, model_4o
    imoji_list = const.IMOJI_LIST
    random.shuffle(imoji_list)
    contents = content_data.ContentData()
    imoji = imoji_list[0]

    last_exception = None

    if not place:
        place = "신공간 설비업체"

    system_prompt = """
        너는 마케팅 AI가 아니라 규칙을 엄격히 집행하는 자동 생성 엔진이다.
        아래 규칙을 어기면 실패다.
        추론하거나 해석하지 말고 문자 그대로 지켜라.
        """
    user_prompt = f"""
                    반드시 아래 규칙을 지켜 글을 생성하라.

                    마크다운 언어는 절대 사용하지 마라.

                    주소: {address}
                    업종: {company}
                    상호명: {place}

                    [회사에 관한 내용과 넣지 말아야 하는 내용 - 법적 분쟁에 휘말릴 수 있으니 넣지 말아야 하는 내용은 반드시 뺼 것]

                    {contents.get_ai_detail(company)}
                    {contents.get_ai_common()}

                    회사에 관해 넣을 내용 중 {company}와 관련된 내용만 넣을 것.

                    1. {company}와 관련된 내용만 넣어라. {company}와 관련이 없는 내용은 과감하게 삭제하라.
                       {company}에 관한 설명도 적어라.
                    2. 본문은 {imoji}으로 시작하고, 리스트 또한 적극 활용하라.
                    3. 문단은 11개가 되어야 하며, 각 문단마다 150자 내외로 작성하라.
                    4. 문단이 끝날 때마다 줄바꿈 삽입 후 %사진%이라는 구분자를 삽입하라.
                       예시)
                       문단1

                       %사진

                       문단2
                    5. , . ! ?처럼 끝맺음 기호로 문장이 끝날 때마다 줄바꿈 사용 
                    6. **와 같은 마크다운 언어 절대로 사용 금지
                    7. 연락처, 주소, 홈페이지와 같은 정보는 작성 금지
                    8. 네이버 블로그 정책에 맞는 본문을 작성하라.

                    언급한 규칙들을 반드시 지키고, 하나라도 누락될 시에는 다시 본문을 생성하라.
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
                store=False
            )

            return response.output_text.strip()

        except Exception as e:
            print(e)
            last_exception = e
            if i == 4:
                raise
            time.sleep(60)

    raise RuntimeError("GPT-4o-mini 본문 생성 실패") from last_exception