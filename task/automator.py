from task.task_functions import *
from data import parsing_data, text_data, content_data, list_data
from cache import download_cache
import os
from utils import parsing

# def start_task():
#     download_cache.download_JSON()
#     download_cache.download_CSV()
#     content = parsing.parse_contents()
#     print(content)

def start_task():
    # 캐시 먼저 저장
    download_cache.download_JSON()
    download_cache.download_CSV()

    text_collection = text_data.TextData()
    parse_collection = parsing_data.ParseData()

    # 크롬 초기화
    init()

    # 계정 정보 가져오기
    login_list = parse_collection.account_data
    # print(login_list)
    # print(os.path.exists("/Users/minsoo/Desktop/photo1.jpg"))  # True여야 함

    # 키워드 리스트(4열) 불러오기
    keywords = list_data.ListData().keyword_list

    # 키워드, 이미지 경로 저장
    # 이미지 경로 셔플은 블로그 진입 및 컨텐츠 작성 전에 수행
    contents = content_data.ContentData()
    contents.set_keywords([(row[0], row[1]) for row in keywords])
    contents.combinate_keywords()
    contents.set_image_path(row[2] for row in keywords)

    # 로그인 반복
    for id_val, pw_val in login_list:
        execute_login("1", "2")
        # 여기서는 키워드 X 키워드대로 글을 생성하여 자동 포스팅 -> 반복문으로 감쌀 것 (for문은 한개만 사용!)

        post_blog("TITLE", contents)
        # post_cafe("TITLE", "content", "자유게시판")
