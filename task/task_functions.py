from web import login, webdriver, blog, cafe
from ui import log
from utils import image, video
from data import box_data

def init():
    webdriver.init_chrome()

def execute_login(id_val, pw_val):
    login.enter_naver()
    login.enter_login_window()
    login.input_id_pw("minsoo1101", "msLee9164@@")
    login.click_login_button()
    log.append_log("[ERROR] 캡챠가 발생했습니다. 수동으로 해제해주세요.")
    while True:
        if login.check_capcha_done() is True:
            break
    login.click_login_not_save()

def post_blog(title, content):
    blog.enter_posting_window()
    blog.enter_iframe()
    blog.cancel_continue()
    blog.exit_help()
    blog.write_title(title)
    blog.write_content(content)

    # 영상 업로드 확인
    image.upload_image("/Users/minsoo/Desktop/Logo.jpg")
    print("image1 uploaded")
    image.upload_image("/Users/minsoo/Desktop/photo1.png")
    print("image2 uploaded")
    video.upload_video_to_blog("/Users/minsoo/Desktop/video1.mov")
    print("video1 uploaded")
    # 확인 끝

    blog.click_post_button()
    blog.complete_posting()
    blog.exit_iframe()

def post_cafe(title, content, board_name):
    cafe.enter_cafe()
    cafe.click_posting_button()

    if box_data.BoxData().get_cb_value() is False:
        cafe.disable_comment()

    cafe.click_board_choice()
    cafe.choose_board(board_name)
    cafe.write_title(title)

    cafe.enter_content_input()

    # 영상 업로드 확인
    cafe.write_content(content)

    image.upload_image("/Users/minsoo/Desktop/Logo.jpg")
    print("image1 uploaded")
    cafe.write_content(content)

    image.upload_image("/Users/minsoo/Desktop/photo1.png")
    print("image2 uploaded")
    cafe.write_content(content)

    video.upload_video_to_cafe("/Users/minsoo/Desktop/video1.mov")
    print("video1 uploaded")
    cafe.write_content(content)

    # cafe.enter_iframe()

    cafe.click_register_button()