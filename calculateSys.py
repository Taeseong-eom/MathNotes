import math, re 

testcase = [
    '5+5=',
    'sin(30)+tan(60)=',
    '70/(70+10)=',
    '6÷10=',
    'sin(70)x(cos(40)+7)='
]


def calString(eq):
    # 전처리하고 등호 제거하고 삼각함수에는 앞에 math. 붙이기
    # 괄호 종류는 모두 소괄호로
    # 곱셉 나눗셈은 *, /로  
    eq = eq.lower()
    replacements = {
    'x': '*',
    '÷': '/',
    '{': '(',
    '}': ')',
    '[': '(',
    ']': ')',
    '×':'*',
    'sin': 'math.sin',
    'cos': 'math.cos',
    'tan': 'math.tan'
    }
    # 교체 작업
    for old, new in replacements.items():
        eq = eq.replace(old, new)
    
    if eq[-1] == '=':
        eq = eq[:-1] 

    return eval(eq)  