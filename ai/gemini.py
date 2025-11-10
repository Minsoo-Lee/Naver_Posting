import re
import time
import types

from google.genai.errors import ServerError
from google.generativeai import GenerationConfig

from ui import log
import google.generativeai as g_genai
from google.api_core.exceptions import ResourceExhausted
from data import text_data
from data import content_data
from collections import deque
from google import genai
from google.genai import types

# gemini_key = "AIzaSyDo6wlM9Q6SFKS-rpHoS_sJQabVt9OEDnI"
model = None
# client = None

# 추가: 25.11.03
api_key = ""

title_list = deque(maxlen=20)

def init_gemini():
    global model, api_key

    # 테스트 용도로 주석처리
    api_key = text_data.TextData().get_api_number()
    # api_key = "AIzaSyDo6wlM9Q6SFKS-rpHoS_sJQabVt9OEDnI"
    g_genai.configure(api_key=api_key)

    # 여기는 공식문서에서 가져온 부분
    # client = genai.Client(api_key="YOUR_API_KEY")

    # genai.configure(api_key=gemini_key)

    # model = genai.GenerativeModel('gemini-2.0-flash')
    # dotenv.load_dotenv()
    # genai.configure(api_key=os.getenv("API_KEY"))
    # model = genai.GenerativeModel('gemini-1.5-flash')
    # model = genai.GenerativeModel('gemini-1.0-pro')

def create_title(titles, address, company, place):
    global model, title_list, api_key
    contents = content_data.ContentData()
    titles_str = "\n".join(titles)
    if place == "":
        place = "신공간 설비업체"
    prompt = f"""
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
    
                     2. 아래 리스트는 지금까지 너가 생성해 준 제목 리스트야. 너가 지금 새로 생성할 제목과 비교했을 때, 문장 구조나 단어 배열 등 느낌이 겹치지 않게 생성해 줘.
                     특히, 앞 부분의 구조가 절대 중복되지 않도록 제대로 봐줘.
                     {title_list}.
    
                     3. ** 또는 ##와 같은 마크다운 언어는 쓰지 마.
                     제발. 마크다운 언어는 절대 포함하지 마. 어차피 적용 안돼
    
                     4. 그리고 너가 준 제목으로 바로 포스팅을 할거야. 다른 제목 옵션 주지 말고 그냥 제목 딱 한줄만 넘겨줘.
                     이게 중요해. 다른 제목 옵션 주지 말고 제목 딱 한줄만 넘겨줘 제발.
                     그래야 글이 꼬이지 않아.
    
                     5. 내가 운영하는 회사 이름은 {place}야. 다른 이상한 이름 쓰지 말고 반드시 내 회사명은 {place}로 소개해 줘.
    
                     6. 제목 글자 수는 50자 이내로 작성해 줘. 함축적으로 작성해주면 더 좋아. 100자가 넘어가면 제목 입력이 되지 않아.
    
                     지금까지 얘기한 6가지 요구사항들은 꼭 지켜줘. 하나도 빠짐없이 6개 다 지켜줘야 해.
                     만약에 이 중 하나라도 빠진 부분이 있다면 처음부터 다시 생성해 줘.
                     ."""
    response = None
    for i in range(5):
        try:
            client = genai.Client(api_key=api_key)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=1,
                )
            )

            break

            # 여기는 이전 작업물 참고
            # generation_config = GenerationConfig(
            #     temperature=1,
            #     top_p=0.95,
            #     top_k=64,
            #     max_output_tokens=8192,
            #     response_mime_type="text/plain",
            # )
            # safety_settings = []
            #
            # genai.configure(api_key=api_key)
            # model = genai.GenerativeModel(
            #     model_name="gemini-2.0-flash",
            #     safety_settings=safety_settings,
            #     generation_config=generation_config,
            # )
            #
            # chat_session = model.start_chat(history=[])
            # response = chat_session.send_message(prompt)
            # return response.text
        except ServerError:
            log.append_log("[ERROR] GEMINI 서버에 오류가 발생했습니다.")
            log.append_log("[ERROR] 1시간 후 요청을 재개합니다.")
            time.sleep(3600)
        except ResourceExhausted:
            log.append_log("[ERROR] 무료 요금제의 하루 일일 요청을 초과하였습니다.")
            if i < 4:
                log.append_log("[ERROR] 2분 후 요청을 재개합니다.")
                time.sleep(120)
            else:
                raise
        except Exception as e:
            log.append_log("[ERROR] Gemini 소통 중 오류가 발생하였습니다.")
            if i < 4:
                log.append_log("[ERROR] 2분 후 요청을 재개합니다.")
                time.sleep(120)
            else:
                raise
    time.sleep(120)
    return response.text

    # try:
    #     response = model.generate_content(f"""
    #                 내가 제목을 작성을 할 거야. 주소 키워드는 {address}, 업종 키워드는 {company}야.
    #                 한 마디로, 나는 {address} 지역에서 {place}라는 회사를 운영하는데, "홍보 글의 제목"을 작성하고 싶어.
    #                 내가 수집한 제목 리스트를 보여줄게. 이 리스트들은 상위 노출된 10개 글의 제목들이야.
    #
    #                 {titles_str}
    #                 내가 쓰는 글도 상위 노출이 될 수 있게끔 저 리스트들을 참고해서 제목을 하나 작성해 줘.
    #
    #                 그리고 다음 사항들은 반드시 지켜줘. 하나라도 빼먹으면 안 돼.
    #
    #                 1. 우리 업체에 관한 내용과 제목에 넣지 말아야 하는 내용은 다음과 같아.
    #
    #                 {contents.get_ai_detail(company)}
    #                 {contents.get_ai_common()}
    #
    #                 너가 넣지 말아야 하는 내용을 넣어버리면 법적 분쟁에 휘말려 큰 손해를 볼 수도 있어. 하지 말라는 내용은 반드시 빼 줘
    #
    #                 2. 아래 리스트는 지금까지 너가 생성해 준 제목 리스트야. 너가 지금 새로 생성할 제목과 비교했을 때, 문장 구조나 단어 배열 등 느낌이 겹치지 않게 생성해 줘.
    #                 특히, 앞 부분의 구조가 절대 중복되지 않도록 제대로 봐줘.
    #                 {title_list}.
    #
    #                 3. ** 또는 ##와 같은 마크다운 언어는 쓰지 마.
    #                 제발. 마크다운 언어는 절대 포함하지 마. 어차피 적용 안돼
    #
    #                 4. 그리고 너가 준 제목으로 바로 포스팅을 할거야. 다른 제목 옵션 주지 말고 그냥 제목 딱 한줄만 넘겨줘.
    #                 이게 중요해. 다른 제목 옵션 주지 말고 제목 딱 한줄만 넘겨줘 제발.
    #                 그래야 글이 꼬이지 않아.
    #
    #                 5. 내가 운영하는 회사 이름은 {place}야. 다른 이상한 이름 쓰지 말고 반드시 내 회사명은 {place}로 소개해 줘.
    #
    #                 6. 제목 글자 수는 50자 이내로 작성해 줘. 함축적으로 작성해주면 더 좋아. 100자가 넘어가면 제목 입력이 되지 않아.
    #
    #                 지금까지 얘기한 6가지 요구사항들은 꼭 지켜줘. 하나도 빠짐없이 6개 다 지켜줘야 해.
    #                 만약에 이 중 하나라도 빠진 부분이 있다면 처음부터 다시 생성해 줘.
    #                 .""")
    #     title_list.append(response.text)
    #     print(title_list)
    #     time.sleep(60)
    #     return response.text
    # except ResourceExhausted:
    #     log.append_log("[ERROR] 무료 요금제의 하루 일일 요청을 초과하였습니다.")
    #     log.append_log("[ERROR] 충분한 시간이 흐른 뒤에 프로그램을 재시작해 주세요.")
    #     # match = re.search(r'quota_id: "(.*?)"', str(e))
    #     # if match:
    #     #     quota_id = match.group(1)
    #     #     log.append_log(f"[ERROR] 무료 요금제의 하루 일일 요청을 초과하였습니다.\nquota_id: {quota_id}")
    #     #     log.append_log("[ERROR] 충분한 시간이 흐른 뒤에 프로그램을 재시작해 주세요.")
    #     raise
    # except Exception as e:
    #     log.append_log("[ERROR] Gemini 소통 중 오류가 발생하였습니다.")
    #     log.append_log(f"[ERROR] 오류 이름: {type(e).__name__}")
    #     raise

def create_content(contents, address, company, place):
    global model
    content_ai = content_data.ContentData()
    if place == "":
        place = "신공간 설비업체"
    print("place = " + place)

    prompt = f"""
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
                ."""

    response = None
    for i in range(5):
        try:
            client = genai.Client(api_key=api_key)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=1,
                )
            )

            break
            # response = model.generate_content(f"""
            #         내가 글을 쓸건데, 주소 키워드는 {address}, 업종 키워드는 {company}야.
            #         그리고 '{place}'라는 회사를 운영하고 있어.
            #         예시 글들을 보여줄게.
            #
            #         예시 1:
            #         {contents[0]}
            #
            #         예시 2:
            #         {contents[1]}
            #
            #         그리고 다음 사항들은 반드시 지켜줘. 하나라도 빼먹으면 안 돼.
            #
            #         1. 우리 업체에 관한 내용과 본문에 넣지 말아야 하는 내용은 다음과 같아.
            #
            #         {content_ai.get_ai_detail(company)}
            #         {content_ai.get_ai_common()}
            #
            #         너가 넣지 말아야 하는 내용을 넣어버리면 법적 분쟁에 휘말려 큰 손해를 볼 수도 있어. 하지 말라는 내용은 반드시 빼 줘.
            #
            #         2. ** 또는 ##와 같은 마크다운 언어는 쓰지 마.
            #         제발. 마크다운 언어는 절대 포함하지 마. 어차피 적용 안돼
            #
            #         3. 중간에 사진을 10장 넣을 건데, 너가 생성한 글에서 사진을 넣을 만한 장소에 %사진% 이라고 써 주고, 1000자 내외의 글로 작성해 줘.
            #         반드시 사진을 10장 넣게 해 줘야 해. 꼭.
            #         사진이 들어가는 공간은 문맥을 해치지 말아야 해.
            #         그리고 사진에 대한 설명을 적으면 글을 파싱하기 어려우니까, 사진에 대한 설명은 반드시 빼 줘.
            #
            #         4. 문장이 . ? ! 이런 끝맺음 기호로 끝날 때마다 줄바꿈은 꼭 해줘야 해.
            #         그리고 하나의 문단이 끝날 때마다 줄바꿈은 두 번 해줘.
            #
            #         5. 연락처, 주소, 홈페이지 같은 정보는 적지 않아도 돼
            #
            #         6. 내가 운영하는 회사 이름은 {place}야. 다른 이상한 이름 쓰지 말고 반드시 내 회사명은 {place}로 소개해 줘.
            #
            #         지금까지 얘기한 5가지 요구사항들은 꼭 지켜줘. 하나도 빠짐없이 5개 다 지켜줘야 해.
            #         만약에 이 중 하나라도 빠진 부분이 있다면 처음부터 다시 생성해 줘.
            #         .""")
            #
            # time.sleep(60)
            # return response.text
        except ServerError:
            log.append_log("[ERROR] GEMINI 서버에 오류가 발생했습니다.")
            log.append_log("[ERROR] 1시간 후 요청을 재개합니다.")
            time.sleep(3600)
        except ResourceExhausted:
            log.append_log("[ERROR] 무료 요금제의 하루 일일 요청을 초과하였습니다.")
            if i < 4:
                log.append_log("[ERROR] 2분 후 요청을 재개합니다.")
                time.sleep(120)
            else:
                raise
        except Exception as e:
            log.append_log("[ERROR] Gemini 소통 중 오류가 발생하였습니다.")
            log.append_log(f"[ERROR] 오류 이름: {type(e).__name__}")
            if i < 4:
                log.append_log("[ERROR] 2분 후 요청을 재개합니다.")
                time.sleep(120)
            else:
                raise
    time.sleep(120)
    return response.text

def create_title_div(titles, address, company, place):
    global model, title_list
    contents = content_data.ContentData()
    titles_str = "\n".join(titles)
    if place == "":
        place = "신공간 설비업체"
    print("place = " + place)
    try:
        # 첫 번째 프롬프트 - 규칙 구조 인식
        prompt1 = f"""
                        나는 {address} 지역에서 {place}라는 회사를 운영 중이며, 
                        {company} 업종 홍보 글 제목을 작성하려고 해.
                    
                        아래는 제목을 작성할 때 반드시 지켜야 할 6가지 규칙이야.
                    
                        1. 우리 업체에 관한 내용과 제목에 넣지 말아야 하는 내용이 존재함
                        2. 기존에 생성한 제목 리스트(title_list)와 문장 구조나 단어 배열이 겹치지 않아야 함
                        3. **, ## 같은 마크다운 문법은 절대 쓰지 않기
                        4. 제목은 딱 한 줄만 제시하기
                        5. 회사명은 반드시 {place}로 써야 함
                        6. 제목은 50자 이내, 함축적으로 작성
                    
                        이 규칙을 요약해서 한 단락으로 정리해 줘.
                        그 요약문은 다음 단계에서 참고할 거야.
                        """
        rule_summary = model.generate_content(prompt1).text
        print("==================================================================")
        print("rule_summary = " + rule_summary)
        print("==================================================================")
        time.sleep(120)

        # 두 번째 프롬프트 - 금지어 전달 및 맥락 결합
        prompt2 = f"""
            아래는 제목 작성 시 반드시 지켜야 할 규칙 요약문이야:
            {rule_summary}
    
            이제 제목에 절대 포함하면 안 되는 내용들을 알려줄게.
    
            {contents.get_ai_detail(company)}
            {contents.get_ai_common()}
    
            위 내용을 포함하지 말아야 한다는 점을 반영해서,
            ‘규칙과 금지사항 요약문’을 하나의 단락으로 다시 정리해 줘.
            그 요약문은 다음 단계에서 제목 생성 시 그대로 사용할 거야.
            """
        ban_summary = model.generate_content(prompt2).text
        print("==================================================================")
        print("rule_summary = " + ban_summary)
        print("==================================================================")
        time.sleep(120)

        # 세 번째 프롬프트 - 제목 생성
        prompt3 = f"""
            아래는 제목 작성 시 반드시 따라야 할 모든 규칙 및 금지사항 요약문이야:
            {ban_summary}
            
            아래는 상위 노출된 10개 제목 리스트야.
            {titles_str}
            
            아래는 지금까지 네가 생성한 제목 리스트야.
            {title_list}
            
            위 모든 내용을 참고해서 내 회사 {place}에 맞는 제목을 50자 이내로 함축적으로 하나 작성해 줘.
            규칙 1~6 전부 반드시 지켜야 해.
            제목은 오직 한 줄만 줘. 다른 옵션은 절대 주지 마.
            """
        response = model.generate_content(prompt3).text
        print("==================================================================")
        print("rule_summary = " + response)
        print("==================================================================")
        time.sleep(120)

        title_list.append(response)
        return response
    except ResourceExhausted:
        log.append_log("[ERROR] 무료 요금제 제한을 초과하였습니다.")
        raise
    except Exception:
        log.append_log("[ERROR] GEMINI 오류가 발생하였습니다.")
        raise
