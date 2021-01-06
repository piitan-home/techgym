import sys
import random
import math
import time

def start_message():
    print('1つだけ異なる漢字の番号を入力してください')
    print('レベル:' + str(level))

def settings():
    global data_num
    global mistake_num
    global col
    global row

    col = math.ceil(level/2) + 3
    row = math.floor(level/2) + 3

    k = random.randint(0,len(not_used)-1)
    data_num = not_used[k]
    not_used.pop(k)

    mistake_num = random.randint(0,col * row-1)

def view_question():
    #print('   a　b　c　d　e')
    t = '   '
    for i in range(col-1):
        t = t + alphabet[i] + '　'
    t = t + alphabet[i+1]
    print(t)

    #print('1　土 土 土 土 土')
    #print('2　土 土 土 土 土')...
    m = data[data_num]
    for i in range(row):
        t = str(i+1) + '　'
        for j in range(col):
            if mistake_num == i * col + j:
                t = t + m[1] + ' '
            else:
                t = t + m[0] + ' '
        print(t)

def change_input_number(input_str):
    global input_num
    #x座標に正しい番号(ローマ字)が入力されたか
    try:
        x = alphabet.index(str(input_str[0]))
    except ValueError:
        try:
            x = alphabet2.index(str(input_str[0]))
        except ValueError:
            print('入力された文字に誤りがあります')
            return True
    #y座標に正しい番号(ローマ字)が入力されたか
    try:
        y = int(input_str[1])-1
    except ValueError:
        print('入力された文字に誤りがあります')
        return True

    if len(input_str) != 2 or x < 0 or x >= col or y < 0 or y >= row :
        print('入力された文字に誤りがあります')
        return True
    #座標の計算
    input_num = y * col + x
    return False

def view_result():
    if input_num == mistake_num:
        print('正解です！')
    else:
        print('不正解です！')
        change_string()
    print('')

def change_string():
    print('正解は '
    +(alphabet[mistake_num%col]
    +str(math.floor(mistake_num/col)+1))
    +' でした')
    sys.exit(0)

def play():
    global level
    start_message()
    settings()
    view_question()
    while change_input_number(input('番号(例:A1)を入力:')):
        pass
    view_result()
    level += 1

#グローバル変数の宣言
alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
alphabet2 = list('abcdefghijklmnopqrstuvwxyz')
input_num = 0
level = 1
data_num = 0
mistake_num = 0
start_time = time.time()

col = 0
row = 0
data = [['見','貝'],['土','士'],['眠','眼'],['己','巳'],['尤','犬'],
['到','致'],['斉','斎'],['棄','菜'],['矢','失'],['白','臼'],
['干','千'],['回','同'],['夭','天'],['二','ニ']]
not_used = list(range(len(data)))

#マスの数は最大9*9
for l in range(9):
    play()
print('タイム:'+str(round(time.time()-start_time))+'s')
