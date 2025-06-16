from selenium.webdriver import ActionChains

from utils.decorators import sleep_after
from web import webdriver
from data.URL import *
from selenium.webdriver.common.by import By
import time

@sleep_after(3)
def enter_posting_window():
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()))
    webdriver.driver.get(f"{BLOG}/?Redirect=Write&")

@sleep_after()
def enter_iframe():
    webdriver.driver.switch_to.frame('mainFrame')

@sleep_after()
def cancel_continue():
    try:
        webdriver.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[4]/div[2]/div[3]/button[1]").click()
    except:
        print("can't find cancel button")
        pass

@sleep_after()
def exit_help():
    try:
        webdriver.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/article/div/header/button").click()
    except:
        pass

@sleep_after()
def write_title(title):
    title_input = webdriver.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[1]/div[1]/div/div/p/span[2]")
    title_input.click()
    actions = ActionChains(webdriver.driver)
    actions.send_keys(title).perform()

@sleep_after()
def write_content(content):
    title_input = webdriver.driver.find_element(By.XPATH,
                                                "/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[2]/div/div/div/div/p/span[2]")
    title_input.click()
    actions = ActionChains(webdriver.driver)
    actions.send_keys(content).perform()

@sleep_after()
def click_post_button():
    webdriver.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div[2]/button").click()

@sleep_after()
def complete_posting():
    webdriver.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div[2]/div/div/div/div[8]/div/button").click()

@sleep_after()
def exit_iframe():
    webdriver.driver.switch_to.default_content()