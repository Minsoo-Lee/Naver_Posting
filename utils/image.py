import platform
import subprocess
import pyautogui
import time
import os

from selenium.webdriver import ActionChains, Keys

from utils.decorators import sleep_after
from web import webdriver
from PIL import Image, ImageDraw, ImageFont
from utils.colors import Colors
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


def get_korean_font(size=24):
    try:
        system = platform.system()
        if system == "Windows":
            return ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", size)
        elif system == "Darwin":
            return ImageFont.truetype("/System/Library/Fonts/AppleGothic.ttf", size)
        else:
            return ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", size)
    except IOError:
        return ImageFont.load_default()

def draw_bold_text(draw, position, text, font, fill, boldness=1.0):
    x, y = position
    offsets = [(0, 0)]
    i = 0.5
    while i <= boldness:
        offsets.extend([(i, 0), (0, i), (i, i)])
        i += 0.5
    for ox, oy in offsets:
        draw.text((x + ox, y + oy), text, font=font, fill=fill)

def draw_border(draw, width, height, thickness=3, color="red"):
    for i in range(thickness):
        draw.rectangle(
            [i, i, width - i - 1, height - i - 1],
            outline=color
        )

def generate_image():
    colors = Colors()
    text_color, bg_color = colors.get_colors()
    width, height = 400, 300
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    font_size = 35
    line_spacing = int(font_size * 1.5)
    font = get_korean_font(font_size)
    lines = ["010-9872-1349", "성수동 설비업체"]

    # ✅ 수정된 전체 텍스트 높이 계산
    total_text_height = font_size * len(lines) + line_spacing * (len(lines) - 1)
    start_y = (height - total_text_height) // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw_bold_text(draw, (x, start_y), line, font, fill=text_color, boldness=0.5)
        start_y += font_size + line_spacing

    draw_border(draw, width, height, thickness=5, color=text_color)
    image.save("output.png")