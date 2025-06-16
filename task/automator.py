from task.task_functions import *

def start_task(id_val, pw_val):
    # 크롬 초기화
    init()
    # 로그인
    login(id_val, pw_val)
    post_blog("title", "content")
