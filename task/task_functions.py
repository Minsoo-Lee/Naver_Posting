import os
import random

from web import login, webdriver, blog, cafe
from ip import ip_trans
from media import video, image
from data import box_data, text_data, button_data
from utils import parsing
from data.const import *
import time
from ui import log


def init():
    webdriver.init_chrome()

def execute_login(id_val, pw_val):
    get_waiting_time()
    log.append_log("Naver 로그인 화면에 접속합니다.")
    login.enter_naver_login()
    # log.append_log("로그인 화면에 진입합니다.")
    # login.enter_login_window()
    log.append_log(f"로그인을 실행합니다. id = {id_val}")
    login.input_id_pw(id_val, pw_val)
    login.click_login_button()
    if not login.check_capcha_appear():
        log.append_log("[ERROR] 캡챠가 발생했습니다. 수동으로 해제해주세요.")
        while True:
            if login.check_capcha_done() is True:
                break
    login.click_login_not_save()
    log.append_log("로그인을 완료하였습니다.")

# 키워드 조합 개수대로 블로그 발행
def post_blog(title, contents, category_name, only_blog):
    keyword_len = contents.get_keywords_length()
    for i in range(keyword_len):
        address, company = contents.get_address(i), contents.get_company(i)

        texts = text_data.TextData()
        texts.divide_title_body()
        texts.replace_title(address, company)
        title = texts.get_title()

        log.append_log("블로그에 진입합니다.")
        blog.enter_blog()

        # 카테고리가 정말 존재하는 카테고리인지 확인
        blog.is_category_exist(category_name)

        blog.enter_iframe()
        blog.enter_posting_window()
        # blog.enter_iframe()
        blog.cancel_continue()
        blog.exit_help()
        log.append_log(f"제목을 작성합니다. 제목 = {title}")
        blog.write_title(title)
        log.append_log("본문을 작성합니다.")
        blog.enter_context_input()
        # 주소, 업체 추출


        # 본문 제작
        article = parsing.parse_contents(address, company)

        # 사진 개수 파악
        count = sum(1 for text in article if text == PHOTO)
        image_len = contents.get_image_path_length()
        length = image_len if count > image_len else count

        write_content_blog(address, company, article, contents.get_random_image_path(length), length)

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
        blog.click_category_listbox()
        log.append_log(f"카테고리를 선택합니다. 카테고리 = {category_name}")

        blog.choose_category(category_name)
        # 해시태그 추가
        hashtags = contents.get_hashtags()
        print(hashtags)
        blog.click_hashtag()
        for hashtag in hashtags:
            blog.send_hashtag(hashtag)
            blog.insert_enter()
        blog.complete_posting()
        log.append_log("포스팅을 완료하였습니다.")
        blog.exit_iframe()
        blog.exit_tab()

    # if button_data.ButtonData().get_toggle_value() is True:
    #     log.append_log("IP를 변경합니다.")
    #     ip.toggle_airplane_mode()
    #     curren_ip = ip.get_current_ip()
    #     log.append_log(f"현재 IP = {curren_ip}")

    if not only_blog:
        total_time, minutes, seconds = get_waiting_time()
        log.append_log(f"다음 작업까지 대기합니다.\n대기시간 = {minutes}분 {seconds}초")
        time.sleep(total_time)

def write_content_blog(address, company, article, image_path, image_length):
    # 먼저, 썸네일 이미지부터 생성
    phone = text_data.TextData().get_phone_number()
    image.generate_image(phone, address + " " + company)
    video.generate_video()
    image_index = 0
    video_path = ""

    for content in article:
        # 썸네일일 경우
        if THUMBNAIL in content:
            # 이미지 생성 후 해당 이미지 업로드
            # 이미지 삭제는 글 작성을 완료한 후에 수행
            image.upload_image(THUMBNAIL_PATH)
        elif PHOTO in content and image_index < image_length:
            # 고객이 넣은 이미지를 테두리 입혀서 작성
            image.draw_border_sample(image_path[image_index])
            image.upload_image(NEW_IMAGE_PATH)
            image_index += 1
            image.remove_image(NEW_IMAGE_PATH)
        elif VIDEO in content:
            # 썸네일 사진을 이용한 영상을 업로드
            video_path = os.path.abspath(VIDEO_PATH)
            video.upload_video_to_blog(video_path, f"{address} {company}")
        elif ENTER is content:
            blog.insert_enter()
        else:
            blog.write_text(content)
        time.sleep(1)
    video.remove_video(video_path)
    image.remove_image(THUMBNAIL_PATH)

def post_cafe(title, contents, cafe_list):
    waiting_time = get_waiting_time()
    for cafe_index in range(len(cafe_list)):
        keyword_len = contents.get_keywords_length()
        for i in range(keyword_len):
            # 주소, 업체 추출
            address, company = contents.get_address(i), contents.get_company(i)

            texts = text_data.TextData()
            texts.divide_title_body()
            texts.replace_title(address, company)
            title = texts.get_title()

            # cafe_data[0] = url
            # cafe_data[1] = board_name
            url = cafe_list[cafe_index][0]
            board_name = cafe_list[cafe_index][1]

            log.append_log("카페에 진입합니다.")
            cafe.enter_cafe(url)
            # 가입했는지 여부 확인
            if not cafe.is_signed_up():
                log.append_log("가입하지 않은 카페입니다. 다음 카페로 넘어갑니다.")
                continue
            cafe.click_posting_button()

            if box_data.BoxData().get_cb_value() is False:
                cafe.disable_comment()

            cafe.click_board_choice()
            log.append_log(f"카테고리를 선택합니다. 카테고리 = {board_name}")
            cafe.choose_board(board_name)
            log.append_log(f"제목을 작성합니다. 제목 = {title}")
            cafe.write_title(title)

            cafe.enter_content_input()

            # 주소, 업체 추출

            # 본문 제작
            article = parsing.parse_contents(address, company)

            # 사진 개수 파악
            count = sum(1 for text in article if text == PHOTO)
            image_len = contents.get_image_path_length()
            length = image_len if count > image_len else count

            log.append_log("본문을 작성합니다.")
            write_content_cafe(address, company, article, contents.get_random_image_path(length), length)

            # 해시태그 추가
            hashtags = contents.get_hashtags()
            print(hashtags)
            cafe.click_hashtag()
            for hashtag in hashtags:
                cafe.send_hashtag(hashtag)
                cafe.insert_enter()

            # # 영상 업로드 확인
            # cafe.write_content(content)
            #
            # image.upload_image("/Users/minsoo/Desktop/Logo.jpg")
            # print("image1 uploaded")
            # cafe.write_content(content)
            #
            # image.upload_image("/Users/minsoo/Desktop/photo1.png")
            # print("image2 uploaded")
            # cafe.write_content(content)
            #
            # video.upload_video_to_cafe("/Users/minsoo/Desktop/video1.mov")
            # print("video1 uploaded")
            # cafe.write_content(content)

            # cafe.enter_iframe()

            cafe.click_register_button()
            log.append_log("포스팅을 완료하였습니다.")

    # if button_data.ButtonData().get_toggle_value() is True:
    #     log.append_log("IP를 변경합니다.")
    #     ip.toggle_airplane_mode()
    #     curren_ip = ip.get_current_ip()
    #     log.append_log(f"현재 IP = {curren_ip}")
        if cafe_index < len(cafe_list) - 1:
            total_time, minutes, seconds = get_waiting_time()
            log.append_log(f"다음 작업까지 대기합니다.\n대기시간 = {minutes}분 {seconds}초")
            time.sleep(total_time)

def write_content_cafe(address, company, article, image_path, image_length):
    # 먼저, 썸네일 이미지부터 생성
    phone = text_data.TextData().get_phone_number()
    image.generate_image(phone, address + " " + company)
    video.generate_video()
    image_index = 0
    video_path = ""

    for content in article:
        # 썸네일일 경우
        if THUMBNAIL in content:
            # 이미지 생성 후 해당 이미지 업로드
            # 이미지 삭제는 글 작성을 완료한 후에 수행
            image.upload_image(THUMBNAIL_PATH)
        elif PHOTO in content and image_index < image_length:
            # 고객이 넣은 이미지를 테두리 입혀서 작성
            image.draw_border_sample(image_path[image_index])
            image.upload_image(NEW_IMAGE_PATH)
            image_index += 1
            image.remove_image(NEW_IMAGE_PATH)
        elif VIDEO in content:
            # 썸네일 사진을 이용한 영상을 업로드
            video_path = os.path.abspath(VIDEO_PATH)
            video.upload_video_to_cafe(video_path, f"{address} {company}")
        elif ENTER is content:
            cafe.insert_enter()
        else:
            cafe.write_text(content)

    video.remove_video(video_path)
    image.remove_image(THUMBNAIL_PATH)

def get_waiting_time():
    min_time = text_data.TextData().get_waiting_min()
    max_time = text_data.TextData().get_waiting_max()
    print(f"min_time = {min_time}")
    print(f"max_time = {max_time}")
    total_time = random.randint(min_time, max_time)
    minutes = total_time / 60
    seconds = total_time - minutes * 60
    return total_time, minutes, seconds