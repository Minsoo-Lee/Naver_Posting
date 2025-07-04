import dotenv
import google.generativeai as genai
from dotenv import load_dotenv
from data import text_data
import os

# gemini_key = "AIzaSyDo6wlM9Q6SFKS-rpHoS_sJQabVt9OEDnI"
model = None


def init_gemini():
    global model
    # api_key = text_data.TextData().get_api_number()
    # genai.configure(api_key=api_key)
    # model = genai.GenerativeModel('gemini-1.5-flash')
    dotenv.load_dotenv()
    genai.configure(api_key=os.getenv("API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')


def create_content(contents):
    global model

    response = model.generate_content(f"""
            내가 성수동 설비업체와 관련된 글을 쓸건데, 예시 글들을 보여줄게.
            
            예시 1:
            {contents[0]}
    
            예시 2:
            {contents[1]}

            중간에 사진을 5장 넣을 건데, 너가 생성한 글에서 사진을 넣을 만한 장소에 %사진% 이라고 써 주고, 1500자 내외의 글로 작성해 줘.
            문장이 . ? ! 이런 끝맺음 기호로 끝날 때마다 줄바꿈은 꼭 해줘야 해.
            사진이 들어가는 공간은 문맥을 해치지 말아야 해. 예를 들면 본문이 하나 끝나고, 소제목이 들어가기 전에 넣어주면 좋겠어. 
            그리고 사진에 대한 설명을 적으면 글을 파싱하기 어려우니까, 사진에 대한 설명은 반드시 빼 줘.
            연락처, 주소, 홈페이지 같은 정보는 적지 않아도 돼
            또한, 인사말과 끝맺음말은 내가 직접 적을 거니까 그건 빼줘.
            그리고 **과 같은 마크다운 언어는 쓰지 마.
            .""")

    return response.text
