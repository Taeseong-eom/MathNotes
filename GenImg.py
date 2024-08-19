import matplotlib.pyplot as plt 
from PIL import Image, ImageDraw, ImageFont
import os

def latex_to_handwritten_image(latex: str, filename: str, font_path: str):
    # 흰색 배경의 빈 이미지 생성
    image_width, image_height = 50, 50
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # 손글씨 스타일 폰트 사용
    try:
        font = ImageFont.truetype(font_path, 50)
    except IOError:
        print("폰트 파일을 찾을 수 없습니다. 경로를 확인해 주세요.")
        return

    # 손글씨 폰트로 LaTeX 텍스트 크기 계산
    bbox = draw.textbbox((0, 0), latex, font=font)
    text_width = 3*(bbox[2] - bbox[0])
    text_height = 3*(bbox[3] - bbox[1])
    
    text_x = (image_width - text_width) # // 2
    text_y = (image_height - text_height) # // 2

    # 텍스트를 이미지에 그리기
    draw.text((text_x, text_y), latex, font=font, fill="black")

    # 이미지 저장 
    image.save(filename)
    print(f"손글씨 스타일 이미지로 저장되었습니다: {filename}")

