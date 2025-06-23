import pyperclip
import pyautogui
import time

from utils.decorators import sleep_after
from web import webdriver

@sleep_after()
def input_title(xpath, title):
    webdriver.send_data_by_xpath(xpath, title)


@sleep_after()
def upload_video_to_blog(video_path):
    webdriver.hide_finder()

    webdriver.click_element_css("button[data-name='video']")
    time.sleep(2)

    webdriver.click_element_xpath("/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[4]/div[2]/div/div/div/div[2]/fieldset/div[1]/button[1]")
    # webdriver.click_element_xpath("/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[3]/div/div[1]/div/div[3]/div[2]/div/div/div/div[2]/fieldset/div[1]/button[1]")
    time.sleep(1)

    webdriver.send_data_by_xpath("//*[@type='file']", video_path)
    input_title("/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[4]/div[2]/div/div/div/div[2]/div[2]/div[2]/div/fieldset/div[1]/div[2]/input", "title")

    time.sleep(30)  # 업로드 대기

    complete_upload("/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[4]/div[2]/div/div/div/div[3]/button")

@sleep_after()
def upload_video_to_cafe(video_path):
    webdriver.hide_finder()

    webdriver.click_element_css("button[data-name='video']")
    time.sleep(2)

    webdriver.click_element_xpath("/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[3]/div/div[1]/div/div[3]/div[2]/div/div/div/div[2]/fieldset/div[1]/button[1]")
    time.sleep(1)

    webdriver.send_data_by_xpath("//*[@type='file']", video_path)
    time.sleep(1)
    input_title("/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[3]/div/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div[2]/div[2]/div/fieldset/div[1]/div[2]/input", "title")

    time.sleep(30)  # 업로드 대기

    complete_upload("/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[3]/div/div[1]/div/div[3]/div[2]/div/div/div/div[3]/button")

def click_video_inform():
    webdriver.click_element_xpath("/html/body/div[7]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[8]/div/div/button")

@sleep_after()
def complete_upload(xpath):
    webdriver.click_element_xpath(xpath)
