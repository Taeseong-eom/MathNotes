import numpy as np
from PIL import Image
def merge_images(main_array, font_img):
    # 이미지를 numpy로 변환
    font_array = np.array(font_img)

    font_x = main_array.shape[1] - font_array.shape[1]
    font_y = (main_array.shape[0] - font_array.shape[0]) // 2

    # 새로운 이미지 배열 생성
    new_array = main_array.copy()

    # 영역 조정
    font_x = min(font_x, main_array.shape[1] - font_array.shape[1])
    font_y = max(0, min(font_y, main_array.shape[0] - font_array.shape[0]))

    alpha_font = font_array[:, :, 3] / 255.0
    alpha_main = 1.0 - alpha_font

    for c in range(3):  # RGB 채널에 대해 알파 블렌딩
        new_array[font_y:font_y + font_array.shape[0], font_x:font_x + font_array.shape[1], c] = (
                alpha_font * font_array[:, :, c] +
                alpha_main * new_array[font_y:font_y + font_array.shape[0], font_x:font_x + font_array.shape[1], c]
        )

    # 알파 채널 업데이트
    new_array[font_y:font_y + font_array.shape[0], font_x:font_x + font_array.shape[1], 3] = np.maximum(
        new_array[font_y:font_y + font_array.shape[0], font_x:font_x + font_array.shape[1], 3],
        font_array[:, :, 3]
    )

    return Image.fromarray(new_array)
