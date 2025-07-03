from media import image
import os
from PIL import Image
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

# 기존 사진에 테두리 입히기
#   - 테두리 색: 썸네일 이미지 생성 시 사용하는 색 활용 (일단 빨간색으로 테스트)
#   - 테두리 굵기: 범위 내에서 랜덤으로 조절 (굵기 = 3으로 테스트)
def test_border_sample():
    global image_path
    image.draw_border_sample(image_path)

# 기존 사진 명도, 채도 랜덤으로 조절


# 썸네일 사진 생성
#   - 색 조합 50-100가지
#   - 명도, 채도 랜덤으로 조절
#   - 테두리 입히기
def test_generate_thumbnail():
    image.generate_image("010-9872-1349", "성수동 설비업체")

# root_dir = os.path.dirname(os.path.abspath(__file__))
# image_path = os.path.join(root_dir, "..", "sample", "sample1.jpg")
# test_border_sample()

# 색 대비 파악 - 100개 모두 출력
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
    for i in range(100):
        bg_color, text_color = colors.get_color(i)
        width, height = 400, 300
        thumbnail = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(thumbnail)

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
            draw_bold_text(draw, (x, start_y), line, font, fill=text_color, boldness=0.5)
            start_y += font_size + line_spacing

        draw_border_thumbnail(draw, width, height, thickness=3, color=text_color)
        thumbnail.save(f"../thumbnail/thumbnail{i}.png")

def generate_image_for_video(phone, company):
    colors = Colors()
    bg_color, text_color = colors.get_color(0)
    width, height = 300, 300
    thumbnail = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(thumbnail)

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
        draw_bold_text(draw, (x, start_y), line, font, fill=text_color, boldness=0.5)
        start_y += font_size + line_spacing

    draw_border_thumbnail(draw, width, height, thickness=3, color=text_color)
    thumbnail.save("thumbnail.png")

generate_image_for_video("010-9872-1349", "성수동 설비업체")