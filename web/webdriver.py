import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from data.URL import *
from utils.decorators import sleep_after

driver = None
URL = "https://localhost:"
PORT = "9004"
main_window = None
main_tab = None
inp_check = None

@sleep_after()
def init_chrome():
    global driver, main_window
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

        time.sleep(1)

    main_window = driver.current_window_handle

@sleep_after()
def enter_url(url):
    driver.get(url)
