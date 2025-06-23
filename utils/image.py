import platform
import subprocess
import pyautogui
import time
import os

from selenium.webdriver import ActionChains, Keys

from utils.decorators import sleep_after
from web import webdriver


# 시각 자료 넣기
@sleep_after()
def upload_image(image_path):
    actions = ActionChains(webdriver.driver)
    copy_image_to_clipboard(image_path)
    time.sleep(1)
    # 윈도우면 Keys.CONTROL
    actions.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()

@sleep_after()
def copy_image_to_clipboard(image_path):
    system = platform.system()

    if system == "Darwin":  # macOS
        script = f'''
            set imgFile to POSIX file "{image_path}" as alias
            set the clipboard to (read imgFile as JPEG picture)
            '''
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Clipboard error: {result.stderr}")
        else:
            print("Clipboard updated.")
        time.sleep(1)  # 클립보드 반영 시간 확보
    elif system == "Windows":
        # Windows에서는 pyautogui로 우회하여 드래그 복사
        # 이미지 아이콘을 직접 선택해야 해서, 다음과 같은 방식 사용
        if not os.path.exists(image_path):
            raise FileNotFoundError("Image path not found")
        os.startfile(os.path.dirname(image_path))  # 폴더 열기
        time.sleep(1)
        pyautogui.hotkey("ctrl", "a")  # 폴더 내 전체 선택 (해당 폴더에 이미지 1개만 있다고 가정)
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "c")  # 복사
        time.sleep(0.5)
    else:
        raise NotImplementedError("Unsupported OS")

