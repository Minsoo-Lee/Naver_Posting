import platform
import subprocess
import pyautogui
import time
import os

from selenium.webdriver import ActionChains, Keys
import colorsys
from PIL import ImageColor
import random

from utils.decorators import sleep_after
from web import webdriver
from PIL import Image, ImageDraw, ImageFont
from utils.colors import Colors

from data.const import *

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

def draw_border_thumbnail(draw, width, height, thickness=3, color="red"):
    for i in range(thickness):
        draw.rectangle(
            [i, i, width - i - 1, height - i - 1],
            outline=color
        )

def generate_image(phone, company):
    colors = Colors()
    text_color, bg_color = colors.get_random_colors()
    text_revised, bg_revised = adjust_color_preserving_contrast(text_color, bg_color)

    width, height = 400, 400
    image = Image.new('RGB', (width, height), bg_revised)
    draw = ImageDraw.Draw(image)

    font_size = 35
    line_spacing = int(font_size * 1.5)
    font = get_korean_font(font_size)
    lines = [phone, company]

    # ✅ 수정된 전체 텍스트 높이 계산
    total_text_height = font_size * len(lines) + line_spacing * (len(lines) - 1)
    start_y = (height - total_text_height) // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw_bold_text(draw, (x, start_y), line, font, fill=text_revised, boldness=0.5)
        start_y += font_size + line_spacing

    draw_border_thumbnail(draw, width, height, thickness=5, color=text_revised)
    image.save(THUMBNAIL_PATH)

def draw_border_sample(image_path, thickness=3, color="red"):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    for i in range(thickness):
        draw.rectangle(
            [i, i, width - i - 1, height - i - 1],
            outline=color
        )

    root_dir = os.path.dirname(os.path.abspath(__file__))
    new_image_path = os.path.join(root_dir, "..", "sample", "revised_sample1.jpg")
    image.save(new_image_path)

def get_luminance(rgb):
    srgb = [c / 255.0 for c in rgb]

    def linearize(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = map(linearize, srgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def get_contrast_ratio(rgb1, rgb2):
    l1 = get_luminance(rgb1)
    l2 = get_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def adjust_color_preserving_contrast(fg_color_name, bg_color_name, lightness_shift=0.08, saturation_shift=0.1, min_contrast=4.5):
    fg_rgb_orig = ImageColor.getrgb(fg_color_name)
    bg_rgb_orig = ImageColor.getrgb(bg_color_name)

    h, l, s = colorsys.rgb_to_hls(*[c / 255.0 for c in fg_rgb_orig])

    # 랜덤 조정
    l_new = min(max(l + random.uniform(-lightness_shift, lightness_shift), 0), 1)
    s_new = min(max(s + random.uniform(-saturation_shift, saturation_shift), 0), 1)

    r2, g2, b2 = colorsys.hls_to_rgb(h, l_new, s_new)
    fg_rgb_adj = tuple(int(c * 255) for c in (r2, g2, b2))

    # 대비 유지 확인
    contrast = get_contrast_ratio(fg_rgb_adj, bg_rgb_orig)
    original_contrast = get_contrast_ratio(fg_rgb_orig, bg_rgb_orig)

    if contrast >= min_contrast and contrast >= original_contrast * 0.9:  # 원래 대비의 90% 이상 유지
        return fg_rgb_adj, bg_rgb_orig
    else:
        return fg_rgb_orig, bg_rgb_orig  # 조정 실패 → 원본 반환

