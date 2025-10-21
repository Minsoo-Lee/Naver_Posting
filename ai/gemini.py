import re

from ui import log
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted\
from data import text_data
from data import content_data
from collections import deque

# gemini_key = "AIzaSyDo6wlM9Q6SFKS-rpHoS_sJQabVt9OEDnI"
model = None

title_list = deque(maxlen=20)

def init_gemini():
    global model
    # 테스트 용도로 주석처리
    api_key = text_data.TextData().get_api_number()
    genai.configure(api_key=api_key)

    # genai.configure(api_key=gemini_key)

    model = genai.GenerativeModel('gemini-2.0-flash')
    # dotenv.load_dotenv()
    # genai.configure(api_key=os.getenv("API_KEY"))
    # model = genai.GenerativeModel('gemini-1.5-flash')
    # model = genai.GenerativeModel('gemini-1.0-pro')

def create_title(titles, address, company, place):
    global model, title_list
    contents = content_data.ContentData()
    titles_str = "\n".join(titles)
    if place == "":
        place = "신공간 설비업체"
    print("place = " + place)
    try:
        response = model.generate_content(f"""
                    내가 제목을 작성을 할 거야. 주소 키워드는 {address}, 업종 키워드는 {company}야.
                    한 마디로, 나는 {address} 지역에서 {place}라는 회사를 운영하는데, "홍보 글의 제목"을 작성하고 싶어.
                    내가 수집한 제목 리스트를 보여줄게. 이 리스트들은 상위 노출된 10개 글의 제목들이야.
                    
                    {titles_str}
                    내가 쓰는 글도 상위 노출이 될 수 있게끔 저 리스트들을 참고해서 제목을 하나 작성해 줘.
                
                    그리고 다음 사항들은 반드시 지켜줘. 하나라도 빼먹으면 안 돼.

                    1. 우리 업체에 관한 내용과 제목에 넣지 말아야 하는 내용은 다음과 같아.
                    
                    {contents.get_ai_detail(company)}
                    {contents.get_ai_common()}
                    
                    너가 넣지 말아야 하는 내용을 넣어버리면 법적 분쟁에 휘말려 큰 손해를 볼 수도 있어. 하지 말라는 내용은 반드시 빼 줘.
                    
                    2. ** 또는 ##와 같은 마크다운 언어는 쓰지 마.
                    제발. 마크다운 언어는 절대 포함하지 마. 어차피 적용 안돼
                    
                    3. 그리고 너가 준 제목으로 바로 포스팅을 할거야. 다른 제목 옵션 주지 말고 그냥 제목 딱 한줄만 넘겨줘.
                    이게 중요해. 다른 제목 옵션 주지 말고 제목 딱 한줄만 넘겨줘 제발.
                    그래야 글이 꼬이지 않아.
                    
                    4. 내가 운영하는 회사 이름은 {place}야. 다른 이상한 이름 쓰지 말고 반드시 내 회사명은 {place}로 소개해 줘.
                    
                    5. 아래 리스트는 지금까지 너가 생성해 준 제목 리스트야. 너가 지금 새로 생성할 제목과 비교했을 때, 문장 구조나 단어 배열 등 느낌이 겹치지 않게 생성해 줘.
                    {title_list}
                    
                    지금까지 얘기한 3가지 요구사항들은 꼭 지켜줘. 하나도 빠짐없이 3개 다 지켜줘야 해.
                    만약에 이 중 하나라도 빠진 부분이 있다면 처음부터 다시 생성해 줘.
                    .""")
        title_list.append(response.text)
        return response.text
    except ResourceExhausted as e:
        match = re.search(r'quota_id: "(.*?)"', str(e))
        if match:
            quota_id = match.group(1)
            log.append_log(f"[ERROR] 무료 요금제의 하루 일일 요청을 초과하였습니다.\nquota_id: {quota_id}")
            log.append_log("[ERROR] 충분한 시간이 흐른 뒤에 프로그램을 재시작해 주세요.")
        raise
    except Exception as e2:
        log.append_log("[ERROR] Gemini 소통 중 오류가 발생하였습니다.")
        log.append_log(f"[ERROR] 오류 이름: {type(e2).__name__}")
        raise

def create_content(contents, address, company, place):
    global model
    content_ai = content_data.ContentData()
    if place == "":
        place = "신공간 설비업체"
    print("place = " + place)
    try:
        response = model.generate_content(f"""
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

                지금까지 얘기한 5가지 요구사항들은 꼭 지켜줘. 하나도 빠짐없이 5개 다 지켜줘야 해.
                만약에 이 중 하나라도 빠진 부분이 있다면 처음부터 다시 생성해 줘.
                .""")

        return response.text
    except ResourceExhausted as e:
        match = re.search(r'quota_id: "(.*?)"', str(e))
        if match:
            quota_id = match.group(1)
            log.append_log(f"[ERROR] 무료 요금제의 하루 일일 요청을 초과하였습니다.\nquota_id: {quota_id}")
            log.append_log("[ERROR] 충분한 시간이 흐른 뒤에 프로그램을 재시작해 주세요.")
        raise
    except Exception as e2:
        log.append_log("[ERROR] Gemini 소통 중 오류가 발생하였습니다.")
        log.append_log(f"[ERROR] 오류 이름: {type(e2).__name__}")
        raise


# def create_title(address, company, article):
#     global model
#
#     response = model.generate_content(f"""
#                 다음은 너가 써 준 글이야.
#
#                 {article}
#
#                 이 글에 맞는 제목을 작성하고 싶어.
#
#
#
#                 내가 글을 쓸건데, 키워드는 {address}, {company}야.
#                 예시 글들을 보여줄게.
#
#                 예시 1:
#                 {contents[0]}
#
#                 예시 2:
#                 {contents[1]}
#
#                 중간에 사진을 10장 넣을 건데, 너가 생성한 글에서 사진을 넣을 만한 장소에 %사진% 이라고 써 주고, 1500자 내외의 글로 작성해 줘.
#                 반드시 사진을 10장 넣게 해 줘야 해.
#                 문장이 . ? ! 이런 끝맺음 기호로 끝날 때마다 줄바꿈은 꼭 해줘야 해.
#                 사진이 들어가는 공간은 문맥을 해치지 말아야 해. 예를 들면 본문이 하나 끝나고, 소제목이 들어가기 전에 넣어주면 좋겠어.
#                 그리고 사진에 대한 설명을 적으면 글을 파싱하기 어려우니까, 사진에 대한 설명은 반드시 빼 줘.
#                 연락처, 주소, 홈페이지 같은 정보는 적지 않아도 돼
#                 또한, 인사말과 끝맺음말은 내가 직접 적을 거니까 그건 빼줘.
#                 그리고 **과 같은 마크다운 언어는 쓰지 마.
#                 .""")
#
#     return response.text