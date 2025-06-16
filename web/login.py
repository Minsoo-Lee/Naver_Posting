import time
from operator import truediv

import pyperclip
from selenium.webdriver import ActionChains, Keys

from utils.decorators import sleep_after
from web import webdriver
from data.URL import *
from selenium.webdriver.common.by import By

@sleep_after()
def enter_naver():
    webdriver.driver.get(NAVER)

@sleep_after()
def enter_login_window():
    webdriver.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/div/a").click()


@sleep_after()
def input_id_pw(id_val, pw_val):
    webdriver.driver.find_element(By.XPATH,
                        "/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div/div[1]/input").send_keys(id_val)

    webdriver.driver.find_element(By.XPATH,
                        "/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div/div[2]/input").send_keys(pw_val)
    # IP 보안?

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