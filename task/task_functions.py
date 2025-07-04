from web import login, webdriver, blog, cafe
from ui import log
from media import video, image
from data import box_data, content_data, text_data
from utils import parsing
from data.const import *

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

# 키워드 조합 개수대로 블로그 발행
def post_blog(title, contents):
    keyword_len = contents.get_keywords_length()
    for i in range(keyword_len):
        blog.enter_posting_window()
        blog.enter_iframe()
        blog.cancel_continue()
        blog.exit_help()
        blog.write_title(title)

        # 주소, 업체 추출
        address, company = contents.get_address(i), contents.get_company(i)

        # 본문 제작
        article = parsing.parse_contents(address, company)
        print(f"[article] = {article}")

        # 사진 개수 파악
        count = sum(1 for text in article if text == PHOTO)

        write_content_blog(address, company, article, contents.get_random_image_path(count))

        # blog.write_text(content)
        #
        # # 영상 업로드 확인
        # image.upload_image("/Users/minsoo/Desktop/Logo.jpg")
        # print("image1 uploaded")
        # image.upload_image("/Users/minsoo/Desktop/photo1.png")
        # print("image2 uploaded")
        # video.upload_video_to_blog("/Users/minsoo/Desktop/video1.mov")
        # print("video1 uploaded")
        # # 확인 끝

        blog.click_post_button()
        # 여기서 카테고리 코드 추가
        blog.complete_posting()
        blog.exit_iframe()

def write_content_blog(address, company, article, image_path):
    # 먼저, 썸네일 이미지부터 생성
    phone = text_data.TextData().get_phone_number()
    image.generate_image(phone, address + " " + company)
    video.generate_video()
    image_index = 0

    for content in article:
        # 썸네일일 경우
        if THUMBNAIL in content:
            # 이미지 생성 후 해당 이미지 업로드
            # 이미지 삭제는 글 작성을 완료한 후에 수행
            image.upload_image(THUMBNAIL_PATH)
        elif PHOTO in content:
            # 고객이 넣은 이미지를 테두리 입혀서 작성
            image.upload_image(image_path[image_index])
            image_index += 1
            pass
        elif VIDEO in content:
            # 썸네일 사진을 이용한 영상을 업로드
            video.upload_video_to_blog(VIDEO_PATH)
        else:
            blog.write_text(content)




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