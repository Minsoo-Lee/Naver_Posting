from task.task_functions import *

def start_task(id_val, pw_val):
    # 크롬 초기화
    init()
    # 로그인
    execute_login(id_val, pw_val)
    # post_blog("title", "content")
    post_cafe("dsarwercqeadfadsgag", "dascxvasraw", "자유게시판")
