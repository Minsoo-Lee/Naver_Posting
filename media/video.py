import os
import time
from moviepy.video.VideoClip import ImageClip


from data.const import *
from utils.decorators import sleep_after
from web import webdriver

@sleep_after()
def input_title(xpath, title):
    webdriver.send_data_by_xpath(xpath, title)


@sleep_after(1)
def upload_video_to_blog(video_path, title):
    webdriver.hide_finder()

    webdriver.click_element_css("button[data-name='video']")
    time.sleep(2)

    webdriver.click_element_xpath("/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[4]/div[2]/div/div/div/div[2]/fieldset/div[1]/button[1]")
    # webdriver.click_element_xpath("/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[3]/div/div[1]/div/div[3]/div[2]/div/div/div/div[2]/fieldset/div[1]/button[1]")
    time.sleep(1)

    webdriver.send_data_by_xpath("//*[@type='file']", video_path)
    input_title("/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[4]/div[2]/div/div/div/div[2]/div[2]/div[2]/div/fieldset/div[1]/div[2]/input", title)

    time.sleep(30)  # 업로드 대기

    complete_upload("/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[4]/div[2]/div/div/div/div[3]/button")

@sleep_after()
def upload_video_to_cafe(video_path, video_title):
    webdriver.hide_finder()

    webdriver.click_element_css("button[data-name='video']")
    time.sleep(2)

    webdriver.click_element_xpath("/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[3]/div/div[1]/div/div[3]/div[2]/div/div/div/div[2]/fieldset/div[1]/button[1]")
    time.sleep(1)

    webdriver.send_data_by_xpath("//*[@type='file']", video_path)
    time.sleep(1)
    input_title("/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[3]/div/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div[2]/div[2]/div/fieldset/div[1]/div[2]/input", video_title)

    time.sleep(30)  # 업로드 대기

    complete_upload("/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[3]/div/div[1]/div/div[3]/div[2]/div/div/div/div[3]/button")

def click_video_inform():
    webdriver.click_element_xpath("/html/body/div[7]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[8]/div/div/button")

@sleep_after()
def complete_upload(xpath):
    webdriver.click_element_xpath(xpath)

@sleep_after()
def generate_video():

    # 1. 이미지 파일을 불러옴
    image_clip = ImageClip(THUMBNAIL_PATH)

    # 2. 클립의 지속 시간을 설정 (예: 10초)
    image_clip.duration = 10

    # 3. 출력 영상 크기 (선택사항)
    # image_clip = image_clip.resized(width=500, height=300)

    # 4. 영상으로 저장
    image_clip.write_videofile(VIDEO_PATH, fps=24)

@sleep_after()
def remove_video(video_path):
    os.remove(video_path)
