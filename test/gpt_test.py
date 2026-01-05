import os
import random
import time
from collections import deque
from data import const
from openai import OpenAI

model_4o = "gpt-4o-mini"
model_5o = "gpt-5-mini"
api_key = ""

prev_title = ""
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

title_list = deque(maxlen=20)
client = None
titles = [
    "성수동 누수탐지 성동구 아파트 누수공사 전문 설비 업체",
"성수동하수구막힘 싱크대막힘 독보적 하수도뚫는곳 업체 마리오설비",
"누수되는 노후된 배관 교체 작업으로 누수를 해결한 사례_옥수동",
"가스온수기 설비 공사! 성수동 건물 배관 이설 작업 시공사례",
"성동구 배관설비 옥수동 하수배관 마감 시공 - 성수동 배관 수리 보수 전문 응봉동 출장 설비업체",
"성수동 습식 주방 설비 공사 설비 업체",
"성동구 씽크대막힘 성수동 옥수동 싱크대 뚫음 자주 막히는 배수구 뚫음 전문 설비 업체",
"성동구 변기교체 홍익동 성수동 화장실 투피스 양변기 수리 설치 설비업체",
"구의동 누수탐지 성수동 빌라주택에서 발생한 보일러 온수배관누수문제 설비공사해결전문업체",
"성수동 전기온수기 설치 사무실 싱크대 및 온수기 설비"]

address = "성수동"
company = "설비업체"
place = "신공간 설비업체"

ai_detail = """<들어가야 하는 내용>

|종합보수설비
[전문건설업 난방시공업 제1종 면허보유]
[도시가스 3종면허보유]
[에너지관리기능사 국가기술자격증보유]
1.수도누수탐지, 수도누수공사, 난방배관교체공사
2.결로방지공사, 홈통 및 우수배관공사
3.베란다(발코니)확장공사
4.보일러 및 온수기,전기온돌판넬 시공
5.겨울철 수도해빙(언수도녹임) 및 동파수리

|화장실 및 주방설비
1.하수도배관,수도배관,타일시공,욕조시공
2.세면대교체,양변기교체,샤워기교체
3.씽크대수도꼭지, 세면대수도꼭지, 세탁기수도꼭지 등 수전교체
4.화장실 수건장 및 거울 등 악세사리 시공
5.수도배관 위치 변경 및 하수구배관 위치  변경 공사 
6.화장실리모델링 ,주방 리모델링 공사

<들어가면 안 되는 내용>

1. 냉난방설비 설치 및 수리 각종 설비점검 및 유지보수는 안함. 이건 에어컨설비 임
2. 겨울철 난방 문제나 여름철 에어컨 고장으로 불편을 겪고 계신가요?저희는 냉난방 설비의 설치, 수리, 점검을 전문적으로 진행합니다.: 이건 에어컨설비 임
3. 공장 설비와 같은 산업용 설비의 관리 및 유지보수도 전문적으로 수행하고 있습니다. 생산성 향상과 안전을 위해 설비의 정기적인 점검과 관리가 필수적입니다. 저희는 다양한 산업 설비에 대한 깊이 있는 이해를 바탕으로 효율적인 관리 방안을 제시하고, 최적의 상태를 유지할 수 있도록 돕겠습니다.: 산업용설비아님 공장설비도 안함"""

ai_common = """<반드시 들어가면 안되는 내용>
1. 24시 긴급출동! 24시 대기!: 등등 24시 안함
2. 하수구 또는 양변기 막힘/뚫음 해결전문가: 양변기,하수구 막힌거 뚫는 건 하수구업자가함
3. 정확한 비용 산정 시스템을 운영하고 있습니다. 추가 비용 발생 없이, 미리 약속드린 금액으로 모든 작업을 완료합니다.: 미리 언급할 필요 없음, 간혹 공사를 하다보면 추가 되는 경우도 있긴 있음
4. 하자보증을 해준다거나, 하자보증보험을 가입해 준다거나, 하자를 몇 년간 봐준다거나,   하자에 대해 끝까지 책임 진다는 등의 하자관련 언급하면 안 됨
5. 24시간 연중무휴로 고객센터 운영하고 있음: 24시 안함
6. 제목이 됐든 내용이 됐든 10년 누수걱정 끝. 과 같은 내용을 기재해 10년간 하자보증해 주는 것으로 혼동되게 하는 멘트는 안해야 함
7. 출장비없이, 무료로, 무료상담받으세요.등등 출장비없다는 말과 무료상담받으라는 멘트금지
8. 씽크대수리는 씽크대업자가 함 우리가 안함
"""

def init_gpt():
    global client, api_key

    # 테스트 용도로 주석처리
    # api_key = text_data.TextData().get_api_number()

    client = OpenAI(api_key=api_key)


def create_title_4o(titles, address, company, place):
    global title_list, model_4o, client, prev_title, ai_detail, ai_common
    last_exception = None
    random.shuffle(titles)
    titles_str = "\n".join(titles)
    keyword_order = [address, company, place]
    random.shuffle(keyword_order)

    # title_list_value = "\n".join(title_list)
    # title_type = random.choice(title_types)
    # print("title_type = " + title_type)

    if not place:
        place = "신공간 설비업체"

    system_prompt = """
                    너는 홍보 글을 제공하는 마케터야.
                    내가 알려주는 규칙을 반드시 지키며 제목을 생성해 줘.
                    """

    user_prompt = f"""
                    내가 제목을 작성을 할 거야. 주소 키워드는 {address}, 업종 키워드는 {company}야.
                     한 마디로, 나는 {address} 지역에서 {place}라는 회사를 운영하는데, "홍보 글의 제목"을 작성하고 싶어.
                     
                     아래 규칙들을 반드시 지켜줘.
                     
                     1. 내가 수집한 제목 리스트를 보여줄게. 이 리스트들은 상위 노출된 10개 글의 제목들이야.

                     {titles_str}
                     
                     내가 쓰는 글도 상위 노출이 될 수 있게끔 저 리스트들을 참고해서 제목을 하나 작성해 줘.

                     그리고 다음 사항들은 반드시 지켜줘. 하나라도 빼먹으면 안 돼.

                     2. 우리 업체에 관한 내용과 제목에 넣지 말아야 하는 내용은 다음과 같아.

                     {ai_detail}
                     {ai_common}

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

                     7. 아래 제목은 너가 이전에 생성해 준 제목이야.
                     동일한 제목 뼈대(문장 골격)를 이전 제목과 공유해서는 안돼.
                     
                     {prev_title}
                     
                     이전 제목과 문장 구조상 유사도가 높다고 판단되면 규칙 위반이야.
                     
                     8. 키워드들의 순서는 다음과 같이 해 줘.

                     {keyword_order[0]}, {keyword_order[1]}, {keyword_order[2]}
                     
                     위의 순서대로 키워드가 등장해야 하는데, 단어들을 나열만 해서는 안돼. 
                     자연스럽게 문장이 이어지도록 해 줘.
                     
                     반드시 위의 8개의 규칙을 꼭 지켜줘. 
                     만약 규칙이 하나라도 지켜지지 않았다면 제목을 다시 생성해 줘.
                    
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

            with open("gpt_with_keywords.txt", "a", encoding="utf-8") as f:
                f.write("================================" + "\n")
                f.write(str(keyword_order) + "\n")
                f.write(title + "\n")

            with open("gpt_test.txt", "a", encoding="utf-8") as f:
                f.write(title + "\n")

            return title

        except Exception as e:
            print(e)
            if i == 4:
                raise
            time.sleep(60)

    raise RuntimeError("GPT-4o-mini 제목 생성 실패") from last_exception

def create_title_5o(titles, address, company, place):
    global title_list, client, model_5o, ai_detail, ai_common

    last_exception = None

    titles_str = "\n".join(titles)
    title_list_value = "\n".join(title_list)

    if not place:
        place = "신공간 설비업체"

    system_prompt = """
                    너는 창의적인 AI가 아니다.
                    규칙을 어기면 즉시 실패로 간주된다.
                    판단, 추론, 최적화, 의도 해석을 금지한다.
                    """

    user_prompt = f"""
너는 제목 생성기다.
아래 규칙을 어기면 실패다.

[참고할 제목 리스트]
{titles_str}

[입력 정보]
주소: {address}
업종: {company}
회사명: {place}

[이미 사용된 제목 – 절대 겹치지 말 것]
{title_list_value}

[중요 규칙]
- 제목은 한 줄
- 25~40자
- 마크다운 금지
- 제목 외 텍스트 출력 금지
- "사례 소개", "성공 사례", "사례 공유" 문구 사용 금지
- "A의 B 공사" 형태 금지
- "지역 + 업체명 + 공사명 나열" 구조 금지

[구조 선택 – 반드시 하나만 선택]
이미 사용된 구조는 절대 사용 금지다.

[제목 시작 규칙 — 반드시 준수]
제목은 반드시 아래 중 하나로 시작하라. 이미 사용된 구조는 절대 사용 금지다.

A. 질문형
- 왜 / 언제 / 어떤 경우 / 어떻게

B. 문제 상황
- 갑작스러운 / 반복되는 / 오래된 / 예상치 못한

C. 행동/선택 유도
- 지금 필요한 / 이런 경우라면 / 선택이 중요한 순간

D. 정보/가이드
- 꼭 알아야 할 / 놓치기 쉬운 / 많이 묻는

E. 결과/변화
- 누수 해결 후 / 공사 이후 달라진 / 시공 후 확인한

[구조 판별 규칙]
- 제목 시작 5어절이 기존 제목과 유사하면 실패
- 조사 "의 / 에서 / 의" 연속 구조 사용 시 실패

위 규칙을 모두 만족하는 제목 하나만 출력하라.
"""

    for i in range(5):
        try:
            response = client.responses.create(
                reasoning={"effort": "minimal"},  # ⭐ 핵심
                model=model_5o,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_output_tokens=100,
            )
            print(response)
            title = response.output_text.strip()
            title_list.append(title)
            return title

        except Exception as e:
            print(e)
            if i == 4:
                raise
            time.sleep(60)

    raise RuntimeError("GPT-5o-mini 제목 생성 실패") from last_exception

def create_content_4o(contents, address, company, place):
    global client, model_4o, ai_detail, ai_common

    last_exception = None

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
                {const.CONTENT_EX1}

                예시 2:
                {const.CONTENT_EX2}

                그리고 다음 사항들은 반드시 지켜줘. 하나라도 빼먹으면 안 돼.

                1. 우리 업체에 관한 내용과 본문에 넣지 말아야 하는 내용은 다음과 같아.

                {ai_detail}
                {ai_common}

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

init_gpt()
for i in range(50):
    create_title_4o(titles, address, company, place)
    print(str(i + 1) + "번째 끝")



