import tkinter as tk
from PIL import Image, ImageTk, ImageOps, ImageChops
import numpy as np

# 이미지 불러오기


def extract_black_part():
    # 이미지를 열기
    image = Image.open('handwritten_latex_equation.png').convert("RGBA")
    
    # 모든 픽셀을 흰색으로 바꾼 이미지 생성 (배경)
    background = Image.new('RGBA', image.size, (255, 255, 255, 0))
    
    # 이미지에서 흑백으로 변환하여 검은 부분만 남기기
    grayscale_image = image.convert('L')
    mask = ImageOps.invert(grayscale_image).point(lambda p: p < 128 and 255)

    # 검은 부분만 남긴 이미지 추출
    black_part = Image.composite(image, background, mask)
    black_part.save('black_part.png', format='PNG')
    return black_part



def pasteResult(canvas, image, x, y):
    # 이미지를 Tkinter Canvas에 붙일 수 있는 포맷으로 변환
    image = Image.open('black_part.png') 
    photo = tk.PhotoImage(file='handwritten_latex_equation.png')

    print(x, y)
    
    # Canvas에 이미지 붙이기
    canvas.create_image(x, y, anchor=tk.NW, image=photo, state='normal')  
    canvas.image = photo  # 참조를 유지하기 위해 저장해둠
    

    print("Canvas에도 저장.")
