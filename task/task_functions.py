import os
import random
import threading

from selenium.webdriver.common.by import By

from web import login, webdriver, blog, cafe
from ip_trans import ip_trans_execute
from media import video, image
from data import box_data, text_data, button_data
from utils import parsing
from data.const import *
import time
from ui import log


def init():
    webdriver.init_chrome()

def execute_login(id_val, pw_val):
    log.append_log("Naver 로그인 화면에 접속합니다.")
    login.enter_naver_login()
    # log.append_log("로그인 화면에 진입합니다.")
    # login.enter_login_window()
    input_login_value(id_val, pw_val)

def input_login_value(id_val, pw_val):
    login.click_ID_phone()
    log.append_log(f"로그인을 실행합니다.\nid = {id_val}")
    login.input_id_pw(id_val, pw_val)
    login.click_login_button()
    # # 비밀번호 / 아이디 틀렸는지 검사
    # if not login.check_login_error():
    #     log.append_log("[ERROR] 아이디 또는 비밀번호가 잘못되었습니다.\n로그인을 다시 시도해 주세요.")
    #     while True:
    #         if login.check_login_done() is True:
    #             break
    #
    # 캡챠 떴는지 검사
    if login.check_capcha_appear():
        log.append_log("[ERROR] 캡챠가 발생했습니다. 수동으로 해제해주세요.")
        while True:
            if login.check_capcha_done() is True:
                break
    login.click_login_not_save()
    log.append_log("로그인을 완료하였습니다.")


# 키워드 조합 개수대로 블로그 발행
def post_blog(contents, category_name, id_val, pw_val, only_blog):
    is_ip_changed = False
    keyword_len = contents.get_keywords_length()

    for i in range(keyword_len):
        stop_event = threading.Event()
        task_thread = threading.Thread(target=check_image_error, args=(stop_event,), daemon=False)
        task_thread.start()
        # # 테스트 용도
        # if button_data.ButtonData().get_toggle_value() is True:
        #     ip_trans_execute.trans_ip()
        #     is_ip_changed = True

        # 주소, 업체 추출
        address, company = contents.get_address(i), contents.get_company(i)

        texts = text_data.TextData()
        texts.divide_title_body()
        texts.replace_title(address, company)
        title = texts.get_title()

        log.append_log("블로그에 진입합니다.")
        # if i == 0:
        #     print(1)
        #     blog.enter_blog(True)
        #     print(2)
        # else:
        #     print(3)
        #     blog.enter_blog(False)
        #     print(4)
        blog.enter_blog(True)

        blog.enter_iframe()

        # 카테고리가 정말 존재하는 카테고리인지 확인 -> iframe 안으로 들어가야 하나?
        # 하위 메뉴는 동적 생성이라 다른 방법을 찾아봐야 함
        # 그냥 포스팅 전에 끄는 방법도 있을듯?
        # or 작성 전에 포스팅 화면에서 발행 버튼 누르고 보는 방법이 나을듯...!
        blog.enter_posting_window()

        if is_ip_changed:
            login.switch_to_popup()
            input_login_value(id_val, pw_val)
            login.switch_to_prev_window()
            # blog.exit_tab()
            # blog.enter_blog()
            blog.enter_iframe()
            blog.enter_posting_window()

        # blog.enter_iframe()
        blog.cancel_continue()
        log.append_log("이어 작성하기를 취소합니다.")
        if i == 0:
            blog.exit_help()
            log.append_log("도움말 창을 닫습니다.")

        blog.click_post_button()
        # 포스팅 전에 카테고리가 있는지 확인
        blog.click_category_listbox()
        log.append_log(f"카테고리가 존재하는지 확인합니다.\n카테고리 = {category_name}")
        if not blog.choose_category(category_name):
            log.append_log(f"[ERROR] 카테고리가 존재하지 않습니다. 다음 작업으로 넘어갑니다.")
            get_waiting_time()
            break
        else:
            log.append_log("존재하는 카테고리입니다. 작성을 계속합니다.")
            blog.click_category_listbox()

        log.append_log(f"제목을 작성합니다.\n제목 = {title}")
        blog.write_title(title)
        log.append_log("본문을 작성합니다.")
        blog.enter_context_input()

        # 테스트를 위해 주석처리
        # 본문 제작
        article = parsing.parse_contents(address, company)

        # 사진 개수 파악
        count = sum(1 for text in article if text == PHOTO)
        image_len = contents.get_image_path_length()
        length = image_len if count > image_len else count

        write_content_blog(address, company, article, contents.get_random_image_path(length), length)
        # write_content_blog(address, company, "테스트", 3, 5)
        
        blog.click_post_button()
        blog.click_category_listbox()

        blog.choose_category(category_name)
        # 해시태그 추가
        hashtags = contents.get_hashtags()
        blog.click_hashtag()
        for hashtag in hashtags:
            blog.send_hashtag(hashtag)
            blog.insert_enter()
        blog.complete_posting()
        log.append_log("포스팅을 완료하였습니다.")
        blog.exit_iframe()
        blog.exit_tab()

        webdriver.enter_url("https://www.naver.com")
        time.sleep(3)

        if button_data.ButtonData().get_toggle_value() is True:
            ip_trans_execute.trans_ip()
            is_ip_changed = True

        if not only_blog:
            get_waiting_time()

        stop_event.set()
        task_thread.join()


def write_content_blog(address, company, article, image_path, image_length):
    # 먼저, 썸네일 이미지부터 생성
    phone = text_data.TextData().get_phone_number()
    log.append_log("썸네일 이미지를 제작합니다.")
    image.generate_image(phone, address, company)
    log.append_log("썸네일 이미지를 이용한 영상을 제작합니다.")
    video.generate_video()
    log.append_log("썸네일 이미지와 영상 제작이 완료되었습니다.")
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
            try:
                image.draw_border_sample(image_path[image_index])
                image.upload_image(NEW_IMAGE_PATH)
                image.remove_image(NEW_IMAGE_PATH)
            except FileNotFoundError:
                log.append_log(f"[ERROR] 이미지 경로 [{image_path[image_index]}]를 찾을 수 없습니다. 다음 작업으로 넘어갑니다.")
            finally:
                image_index += 1
                image.blog_upload_image_error()
        elif VIDEO in content:
            # 썸네일 사진을 이용한 영상을 업로드
            video_path = os.path.abspath(VIDEO_PATH)
            video.upload_video_to_blog(video_path, f"{address} {company}")
        elif ENTER is content:
            blog.insert_enter()
        else:
            blog.write_text(content)


    # 테스트 용도로 주석처리
    video.remove_video(video_path)
    image.remove_image(THUMBNAIL_PATH)

def post_cafe(contents, cafe_list, id_val, pw_val):
    for cafe_index in range(len(cafe_list)):
        keyword_len = contents.get_keywords_length()
        for i in range(keyword_len):
            # # 테스트 용도
            # if button_data.ButtonData().get_toggle_value() is True:
            #     ip_trans_execute.trans_ip()
            #     is_ip_changed = True

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
                # 생각해보기
                log.append_log("[ERROR] 가입하지 않은 카페입니다. 다음 카페로 넘어갑니다.")
                break
            log.append_log("가입된 카페입니다. 컨텐츠 작성을 계속합니다.")
            cafe.click_posting_button()

            # 여기서 카테고리 찾기 -> 없으면 다음 단계로
            if box_data.BoxData().get_cb_value() is False:
                cafe.disable_comment()

            cafe.click_board_choice()
            log.append_log(f"카테고리를 선택합니다.\n카테고리 = {board_name}")
            if not cafe.choose_board(board_name):
                log.append_log(f"[ERROR] 카테고리가 존재하지 않습니다. 다음 작업으로 넘어갑니다.")
                get_waiting_time()
                break
            log.append_log(f"제목을 작성합니다.\n제목 = {title}")
            cafe.write_title(title)

            cafe.enter_content_input()

            # 주소, 업체 추출

            # 테스트 용도로 주석처리
            # 본문 제작
            article = parsing.parse_contents(address, company)

            # 사진 개수 파악
            count = sum(1 for text in article if text == PHOTO)
            image_len = contents.get_image_path_length()
            length = image_len if count > image_len else count

            write_content_cafe(address, company, article, contents.get_random_image_path(length), length)
            # write_content_cafe(address, company, "테스트", 3, 5)

            log.append_log("본문을 작성합니다.")

            # 해시태그 추가
            hashtags = contents.get_hashtags()
            print(hashtags)
            cafe.click_hashtag()
            for hashtag in hashtags:
                cafe.send_hashtag(hashtag)
                cafe.insert_enter()

            cafe.click_register_button()
            if webdriver.switch_to_alert():
                login.switch_to_popup()
                input_login_value(id_val, pw_val)
                login.switch_to_prev_window()
                cafe.click_register_button()
            webdriver.exit_tab()

            log.append_log("포스팅을 완료하였습니다.")

            if button_data.ButtonData().get_toggle_value() is True:
                ip_trans_execute.trans_ip()
            if cafe_index < len(cafe_list) - 1:
                get_waiting_time()


def write_content_cafe(address, company, article, image_path, image_length):
    # 먼저, 썸네일 이미지부터 생성
    phone = text_data.TextData().get_phone_number()
    image.generate_image(phone, address, company)
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
            try:
                image.draw_border_sample(image_path[image_index])
                image.upload_image(NEW_IMAGE_PATH)
                image.remove_image(NEW_IMAGE_PATH)
            except FileNotFoundError:
                log.append_log(f"[ERROR] 이미지 경로 [{image_path[image_index]}]를 찾을 수 없습니다. 다음 작업으로 넘어갑니다.")
            finally:
                image_index += 1
                image.cafe_upload_image_error()
        elif VIDEO in content:
            # 썸네일 사진을 이용한 영상을 업로드
            video_path = os.path.abspath(VIDEO_PATH)
            video.upload_video_to_cafe(video_path, f"{address} {company}")
        elif ENTER is content:
            cafe.insert_enter()
        else:
            cafe.write_text(content)

    # 테스트 용도로 주석처리
    video.remove_video(video_path)
    image.remove_image(THUMBNAIL_PATH)

def get_waiting_time():
    min_time = text_data.TextData().get_waiting_min()
    max_time = text_data.TextData().get_waiting_max()
    print(f"min_time = {min_time}")
    print(f"max_time = {max_time}")
    total_time = random.randint(min_time, max_time)
    minutes = total_time // 60
    seconds = total_time - minutes * 60

    log.append_log(f"다음 작업까지 대기합니다.\n대기시간 = {minutes}분 {seconds}초")
    time.sleep(total_time)

    return total_time, minutes, seconds

def check_image_error(stop_event):
    while not stop_event.is_set():
        try:
            webdriver.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[4]/div[2]/div[3]/button")
        except:
            continue