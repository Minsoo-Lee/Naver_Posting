import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from data.const import *
from utils.decorators import sleep_after
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = None
URL = "https://localhost:"
PORT = "9004"
main_window = None
main_tab = None
inp_check = None
actions = None

@sleep_after()
def init_chrome():
    global driver, main_window, actions
    if driver is None:
        chrome_options = Options()

        # ✅ 필수: Headless 서버 환경에서 필요한 옵션
        #chrome_options.add_argument('--headless')  # 화면 없이 실행
        chrome_options.add_argument('--no-sandbox')  # 보안 샌드박스 비활성화
        chrome_options.add_argument('--disable-dev-shm-usage')  # 메모리 사용 제한 해제
        chrome_options.add_argument('--disable-gpu')  # GPU 비활성화 (가끔 필요)
        chrome_options.add_argument('--window-size=1920x1080')  # 뷰포트 설정

        # 선택 옵션
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 1
        })
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=chrome_options)

        # webdriver 속성 제거
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """
        })

        time.sleep(1)

    main_window = driver.current_window_handle
    actions = ActionChains(driver)

def enter_url(url):
    driver.get(url)

def click_element_xpath(xpath):
    while True:
        try:
            driver.find_element(By.XPATH, xpath).click()
            break
        except:
            time.sleep(1)
            continue

def click_element_xpath_error(xpath):
    for i in range(15):
        try:
            driver.find_element(By.XPATH, xpath).click()
            break
        except:
            time.sleep(1)
            continue


def click_element_css(css):
    driver.find_element(By.CSS_SELECTOR, css).click()

def click_element_link_text(link_text):
    driver.find_element(By.LINK_TEXT, link_text).click()

def get_element_xpath(xpath):
    return driver.find_element(By.XPATH, xpath)

def get_element_class(class_name):
    return driver.find_element(By.CLASS_NAME, class_name)

def get_element_css(css):
    return driver.find_element(By.CSS_SELECTOR, css)

def execute_javascript(js_code, element):
    driver.execute_script(js_code, element)

def find_category(category_name):
    elements = driver.find_elements(By.CLASS_NAME, "tlink")
    elements = driver.find_elements(By.XPATH, '//*[starts-with(@class, "tlink")]')
    print(elements)

    for element in elements:
        a_tags = element.find_elements(By.TAG_NAME, "a")
        for a_tag in a_tags:
            print(a_tag.text)

def click_element_among_classes(class_name, text):
    elements = driver.find_elements(By.CLASS_NAME, class_name)

    for element in elements:
        if element.text == text:
            element.click()  # 클릭하고 싶으면 이 줄 사용
            return True
    return False

def switch_frame(frame):
    driver.switch_to.frame(frame)

def switch_frame_to_default():
    driver.switch_to.default_content()

def switch_window():
    tab = driver.window_handles[-1]
    driver.switch_to.window(window_name=tab)

def exit_tab():
    driver.close()
    driver.switch_to.window(main_window)

def send_keys_action(value):
    global actions
    actions = ActionChains(driver)
    actions.send_keys(value).perform()

def get_actions():
    global actions
    return actions

def send_data_by_xpath(xpath, value):
    driver.find_element(By.XPATH, xpath).send_keys(value)

def hide_finder():
    driver.execute_script("""
    	document.addEventListener('click', function(event) {
    		if (event.target.tagName === 'INPUT' && event.target.type && event.target.type === 'file') {
    			event.preventDefault();
    		}
    	}, true);
    """)
    time.sleep(3)

def get_active_element():
    return driver.switch_to.active_element()

def recover_window():
    driver.switch_to.window(main_window)

@sleep_after()
def switch_to_alert():
    try:
        alert = driver.switch_to.alert
        alert.accept()
        return True
    except:
        return False