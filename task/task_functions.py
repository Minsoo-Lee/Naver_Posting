from web.login import *
from web.webdriver import *
from web.blog import *
from ui import log

def init():
    init_chrome()

def login(id_val, pw_val):
    enter_naver()
    enter_login_window()
    input_id_pw("minsoo1101", "msLee9164@@")
    click_login_button()
    log.append_log("[ERROR] 캡챠가 발생했습니다. 수동으로 해제해주세요.")
    while True:
        if check_capcha_done() is True:
            break
    click_login_not_save()

def post_blog(title, content):
    enter_posting_window()
    enter_iframe()
    cancel_continue()
    exit_help()
    write_title(title)
    write_content(content)
    click_post_button()
    complete_posting()
    exit_iframe()

def post_cafe(title, content):
    pass