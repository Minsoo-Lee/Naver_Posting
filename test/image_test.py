from media import image
import os
from PIL import Image

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

root_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(root_dir, "..", "sample", "sample1.jpg")
test_border_sample()