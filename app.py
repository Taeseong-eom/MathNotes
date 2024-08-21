import numpy as np
import gradio as gr
from PIL import Image
from io import BytesIO
from clovaAPI_gradio import getEquation
from calculateSys import calString
from GenImg_gradio import latex_to_handwritten_image
from image_process import merge_images

def process_equation(image):
    # 이미지 배열 추출
    imArray = np.array(image['composite'])
    # 알파 채널 제거
    alpha = imArray[:, :, 3] / 255.0
    rgb = imArray[:, :, :3]
    background = np.ones_like(rgb) * 255  # 흰색 배경

    blended = alpha[:, :, np.newaxis] * rgb + (1 - alpha[:, :, np.newaxis]) * background
    rgb_array = blended.astype(np.uint8)

    # RGB로 변환
    img = Image.fromarray(rgb_array, 'RGB')

    # Byte 스트림으로 변환
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    eq = getEquation(img_byte_arr)
    print("OCR 인식 부분 : " + eq)

    # 수식 계산
    latex_code = round(calString(eq), 2)
    print("result of cal : ", latex_code)
    latex_code_str = str(latex_code)
    print("계산된 결과 : " + latex_code_str)

    font_img = latex_to_handwritten_image(latex_code_str, font_family="Nanum Pen Script", font_size=80)

    # 결과 이미지 생성
    result_img = merge_images(imArray, font_img)

    return result_img, latex_code


custom_css = """
&lt;style&gt;
@import url('https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap');
body {
    font-family: 'Nanum Pen Script', cursive;
}
&lt;/style&gt;
"""

interface = gr.Interface(
    fn=process_equation,
    inputs=gr.Sketchpad(height=512, width=512),
    outputs=[gr.Image(type="pil", label="손글씨 계산 이미지"), gr.Number(label="계산 결과")],
    title="Handwriting Equation Notes",
    description="수식을 쓴 뒤 제출을 클릭하세요.",
    examples=[],
    cache_examples=False,
    css=custom_css
)

# 실행
interface.launch()