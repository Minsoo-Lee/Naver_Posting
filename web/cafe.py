from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.decorators import sleep_after
from web import webdriver
from data.const import *
import time

@sleep_after(3)
def enter_cafe():
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()))
    webdriver.enter_url(CAFE)

@sleep_after(3)
def click_posting_button():
    webdriver.click_element_xpath("/html/body/div[3]/div/div[5]/div[1]/div[1]/div[1]/div[2]/a")
    time.sleep(1)
    webdriver.switch_tab()

@sleep_after(3)
def disable_comment():
    webdriver.click_element_xpath("/html/body/div[1]/div/div/section/div/div[2]/div[2]/div[2]/ul/li[1]/div/input")

@sleep_after()
def click_board_choice():
    webdriver.click_element_xpath("/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/button")

@sleep_after()
def choose_board(board_name):
    webdriver.click_element_among_classes("option_text", board_name)

@sleep_after()
def write_title(title):
    webdriver.click_element_xpath("/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[1]/div/div[2]/div/textarea")
    webdriver.send_keys_action(title)

@sleep_after()
def enter_iframe():
    webdriver.switch_frame('mainFrame')

@sleep_after()
def write_content(content):
    webdriver.click_element_xpath("/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[3]/div/div[1]/div/div[1]/div[2]")
    time.sleep(1)
    webdriver.send_keys_action(Keys.RETURN)
    webdriver.send_keys_action(content)

@sleep_after()
def click_register_button():
    webdriver.click_element_xpath("/html/body/div[1]/div/div/section/div/div[1]/div/a")
    time.sleep(1)
    webdriver.exit_tab()



@sleep_after()
def cancel_continue():
    try:
        webdriver.click_element_xpath("/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[4]/div[2]/div[3]/button[1]")
    except:
        pass

@sleep_after()
def exit_help():
    try:
        webdriver.click_element_xpath("/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/article/div/header/button")
    except:
        pass

@sleep_after()
def enter_content_input():
    webdriver.click_element_xpath("/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[3]/div/div[1]/div/div[1]/div[2]")

# def write_content(content):
#     # 1. 입력 칸 클릭
#     webdriver.click_element_xpath("/html/body/div[1]/div/div/section/div/div[2]/div[1]/div[3]/div/div[1]/div/div[1]/div[2]")
#     time.sleep(0.5)
#
#     # focused_element = webdriver.driver.switch_to.active_element
#
#     # focused_element.send_keys(Keys.RETURN)
#     # focused_element.send_keys(content)
#
#     # # 2. 진짜로 포커스가 갔는지 확인
#     # WebDriverWait(webdriver.driver, 10).until(
#     #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div.se-canvas-bottom'))
#     # ).click()
#     # time.sleep(0.2)
#     #
#     # # 3. 현재 활성화된 요소에 직접 입력
