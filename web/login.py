import time
from operator import truediv

import pyperclip
from selenium.webdriver import ActionChains, Keys

from utils.decorators import sleep_after
from web import webdriver
from data.const import *
from selenium.webdriver.common.by import By

@sleep_after()
def enter_naver():
    webdriver.driver.get(NAVER)

@sleep_after()
def enter_login_window():
    webdriver.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/div/a").click()


@sleep_after()
def input_id_pw(id_val, pw_val):
    # 천천히 입력하여 캡챠 우회 (되는지 확인 필요)
    id_input = webdriver.get_element_xpath("/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div/div[1]/input")
    pw_input = webdriver.get_element_xpath("/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div/div[2]/input")

    for ch in id_val:
        id_input.send_keys(ch)
        time.sleep(0.2)

    for ch in pw_val:
        pw_input.send_keys(ch)
        time.sleep(0.2)

    # 기존 코드
    # webdriver.driver.find_element(By.XPATH,
    #                     "/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div/div[1]/input").send_keys(id_val)
    #
    # webdriver.driver.find_element(By.XPATH,
    #                     "/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div/div[2]/input").send_keys(pw_val)

@sleep_after()
def click_login_button():
    # driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[11]/button").click()
    webdriver.driver.find_element(By.ID, "log.login").click()

@sleep_after()
def check_capcha_done():
    try:
        webdriver.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/form/fieldset/span[2]/a")
        return True
    except:
        return False

@sleep_after()
def click_login_not_save():
    webdriver.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/form/fieldset/span[2]/a").click()

@sleep_after()
def click_logout():
    webdriver.click_element_xpath("/html/body/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/div[1]/div/button")
