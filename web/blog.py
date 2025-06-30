from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from utils.decorators import sleep_after
from web import webdriver
from data.const import *
import time
from utils import image, video
from web.webdriver import hide_finder

# 윈도우일 경우 다르게 (혹은 운영체제 감지해서 다르게 작동하게)
KEY = Keys.COMMAND

@sleep_after(3)
def enter_posting_window():
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()))
    webdriver.enter_url(f"{BLOG}/?Redirect=Write&")

@sleep_after()
def enter_iframe():
    webdriver.switch_frame('mainFrame')

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
def write_title(title):
    webdriver.click_element_xpath("/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[1]/div[1]/div/div/p/span[2]")
    webdriver.send_keys_action(title)
    # title_input = webdriver.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[1]/div[1]/div/div/p/span[2]")
    # title_input.click()
    # actions = ActionChains(webdriver.driver)
    # actions.send_keys(title).perform()

@sleep_after()
def write_content(content):
    webdriver.click_element_xpath("/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[2]/div/div/div/div/p/span[2]")
    webdriver.send_keys_action(Keys.RETURN)
    webdriver.send_keys_action(content)
    # title_input = webdriver.driver.find_element(By.XPATH,
    #                                             "/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[2]/div/div/div/div/p/span[2]")
    # title_input.click()
    # actions = ActionChains(webdriver.driver)
    # actions.send_keys(content).perform()

@sleep_after()
def click_post_button():
    webdriver.click_element_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div[2]/button")
    # webdriver.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div[2]/button").click()

@sleep_after()
def complete_posting():
    webdriver.click_element_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div[2]/div/div/div/div[8]/div/button")
    # webdriver.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div[2]/div/div/div/div[8]/div/button").click()

@sleep_after()
def exit_iframe():
    webdriver.switch_frame_to_default()
