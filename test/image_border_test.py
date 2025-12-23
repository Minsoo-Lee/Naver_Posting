from PIL.Image import Image

import media.image
from media.image import generate_image, draw_border_sample

# generate_image("010-9872-1349", "성수동", "설비업체")

draw_border_sample("/Users/minsoo/coding/Naver_Posting/sample/sample1.jpg", "010-9872-1349", "성수동", "설비업체")

image = Image.open(image_path)
