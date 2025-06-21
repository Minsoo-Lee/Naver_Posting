from task.task_functions import *
from data import parsing_data
from data import text_data
from ui import log

def start_task():
    text_collection = text_data.TextData()
    parse_collection = parsing_data.ParseData()

    # log.append_log(f"waiting_max: {text_collection.get_waiting_max()}")
    # log.append_log(f"waiting_min: {text_collection.get_waiting_min()}")
    # log.append_log(f"phone_number: {text_collection.get_phone_number()}")
    # log.append_log(f"api_key: {text_collection.get_api_number()}")
    # log.append_log("")
    # log.append_log(f"keyword_data: {parse_collection.keyword_data}")
    # log.append_log(f"account_data: {parse_collection.account_data}")
    # log.append_log(f"blog_data: {parse_collection.blog_data}")
    # log.append_log(f"cafe_data: {parse_collection.cafe_data}")
    # log.append_log(f"content_data: {parse_collection.content_data}")

    # 크롬 초기화
    init()

    # 계정 정보 가져오기
    login_list = parse_collection.account_data
    print(login_list)

    # 로그인 반복
    # for id_val, pw_val in login_list:
    execute_login("1", "2")
        # 여기서는 키워드 X 키워드대로 글을 생성하여 자동 포스팅 -> 반복문으로 감쌀 것 (for문은 한개만 사용!)
    post_blog("title", "content")
        # post_cafe("dsarwercqeadfadsgag", "dascxvasraw", "자유게시판")
