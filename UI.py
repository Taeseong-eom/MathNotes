from tkinter import *
from PIL import Image, ImageGrab
from clovaAPI import getEquation
from calculateSys import calString

mycolor = "black"

# 초기 좌표를 저장할 변수
old_x = None
old_y = None

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
    x0 = canvas.winfo_rootx()
    y0 = canvas.winfo_rooty()
    x1 = x0 + canvas.winfo_width()
    y1 = y0 + canvas.winfo_height()

    im = ImageGrab.grab((x0, y0, x1, y1))
    im.save('capture/equation.png')
    eq = getEquation()
    print(calString(eq))

window = Tk()
canvas = Canvas(window, bg='white')
canvas.pack()

# 왼쪽 마우스를 누르고 움직일 때 그려지도록 함
canvas.bind("<B1-Motion>", paint)
# 마우스 버튼을 놓으면 좌표를 초기화
canvas.bind("<ButtonRelease-1>", reset)

# "입력" 버튼을 누르면 capture 함수 호출
button = Button(window, text="입력", command=capture)
button.pack()

window.mainloop()
