from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import re

def latex_to_handwritten_image(latex, font_family="Nanum Pen Script", font_size=200):
    # 웹 폰트 URL (예: Google Fonts에서 제공하는 URL)
    font_url = f"https://fonts.googleapis.com/css2?family={font_family.replace(' ', '+')}&display=swap"

    # 폰트 CSS 파일 다운로드
    response = requests.get(font_url)
    css_content = response.text

    # CSS에서 폰트 파일 URL 추출
    font_file_url = re.search(r"url\((.*?)\)", css_content).group(1)

    # 폰트 파일 다운로드
    font_response = requests.get(font_file_url)
    font = ImageFont.truetype(BytesIO(font_response.content), font_size)

    # 텍스트 크기 계산
    dummy_draw = ImageDraw.Draw(Image.new("RGB", (1, 1), "white"))
    text_bbox = dummy_draw.textbbox((0, 0), latex, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # 여백 추가
    padding = 150
    image_width = text_width + 2 * padding
    image_height = text_height + 2 * padding

    # RGBA 이미지 생성
    image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.text((padding, padding), latex, font=font, fill=(0, 0, 0, 255))

    return image