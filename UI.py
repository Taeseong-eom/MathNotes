from tkinter import *
from PIL import Image, ImageGrab
import os
from clovaAPI import getEquation
from calculateSys import calString
from GenImg import latex_to_handwritten_image
from Paste import pasteResult, extract_black_part

mycolor = "black"

# 초기 좌표를 저장할 변수
old_x = None
old_y = None

window = Tk()
window.title("Handwritten Equation Solver")

# 캔버스 크기 지정
canvas = Canvas(window, bg='white', width=400, height=300)
canvas.pack()

# 그리는 함수, 선을 부드럽게 연결
def paint(event):
    global old_x, old_y

    if old_x and old_y:
        # 이전 좌표와 현재 좌표를 연결하는 선을 그림
        canvas.create_line(old_x, old_y, event.x, event.y, fill=mycolor, width=3, capstyle=ROUND, smooth=True)

    # 현재 좌표를 저장
    old_x = event.x
    old_y = event.y

# 마우스 버튼을 놓았을 때 초기화
def reset(event):
    global old_x, old_y
    old_x = None
    old_y = None

def capture():
    # 이미지가 저장될 폴더 확인 및 생성
    if not os.path.exists('capture'):
        os.makedirs('capture')

    # 캔버스의 좌표와 크기를 기준으로 스크린샷을 캡처
    x0 = canvas.winfo_rootx() # + 40
    y0 = canvas.winfo_rooty() # + 60
    x1 = x0 + canvas.winfo_width()
    y1 = y0 + canvas.winfo_height()

    im = ImageGrab.grab((x0, y0, x1, y1))
    im.save('capture/equation.png')
    
    # OCR로 수식을 추출
    eq, Xmax, Xmin, Ymax, Ymin = getEquation()
    print("OCR 인식 부분 : " + eq)
 
    # 수식 계산
    latex_code = round(calString(eq), 2)
    print("result of cal : ", latex_code)
    latex_code_str = str(latex_code)  # 계산된 값을 문자열로 변환
    print("계산된 결과 : " + latex_code_str)
    output_file = "handwritten_latex_equation.png"
    font_path = 'font/나눔손글씨 무궁화.ttf'  # 실제 폰트 경로로 변경

    # 폰트 파일이 존재하는지 확인
    if not os.path.exists(font_path):
        print("폰트 경로가 잘못되었습니다. 손글씨 폰트를 다운로드하고 경로를 업데이트하세요.")
    else:
        latex_to_handwritten_image(latex_code_str, output_file, font_path)
        print(f"이미지가 {output_file}로 저장되었습니다.")
        
        # 결과를 UI에 표시
        result_label.config(text=f"계산 결과: {latex_code_str}")

        # 결과를 Canvas에 붙여넣기.
        Xpaste = (Xmax-Xmin)/(2*len(eq))+Xmax
        Ypaste = Ymin+(Ymax-Ymin)/2
        image = extract_black_part()
        print(f"Xp:{Xpaste}, Yp:{Ypaste}")
 

        pasteResult(canvas, image, Xpaste, Ypaste)

 

# 계산 결과를 표시할 라벨 추가
result_label = Label(window, text="계산 결과: ", font=("Helvetica", 14))
result_label.pack()

# 왼쪽 마우스를 누르고 움직일 때 그려지도록 함
canvas.bind("<B1-Motion>", paint)
# 마우스 버튼을 놓으면 좌표를 초기화
canvas.bind("<ButtonRelease-1>", reset)

# "입력" 버튼을 누르면 capture 함수 호출
button = Button(window, text="입력", command=capture)
button.pack()

window.mainloop()
