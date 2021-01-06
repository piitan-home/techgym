import random
import time
import math


class RockPaperScissors:
    __DATA = list('見貝土士眠眼己巳尤犬到致斉斎棄菜矢失白臼干千回同夭天二ニ')
    __ALPHABET_UPPER = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    __ALPHABET_LOWER = list('abcdefghijklmnopqrstuvwxyz')
    __LANK = ['S', 'A', 'B', 'C', 'D', 'E']
    __LANK_SCORE = [960, 920, 840, 700, 500, 0]

    def __init__(self):
        self.__level = 1
        self.__data_size = round(len(self.__DATA)/2)
        self.__not_used_data = list(range(self.__data_size))

        self.__width = 3
        self.__height = 3
        self.__data_num = 0
        self.__mistake_num = 0
        self.__score = 0

    def __start_message(self):
        print('違う漢字の座標(例:A1)を入力してください')

    def __section_message(self):
        print('Lv' + str(self.__level))

    def __random_choice(self):
        self.__height = self.__level + 2
        self.__width = self.__level + 2

        rand = random.randrange(len(self.__not_used_data))
        self.__data_num = self.__not_used_data[rand]
        self.__not_used_data.pop(rand)

        self.__mistake_num = random.randrange(self.__width * self.__height)

    def __view_question(self):
        # 座標を出力
        t = ''
        t = t + '    '
        # マスが1つの時のエラー回避
        i = -1
        for i in range(self.__width-1):
            t = t + self.__ALPHABET_UPPER[i] + '　'
        t = t + self.__ALPHABET_UPPER[i+1] + '\n'

        # データの番号
        num = self.__data_num * 2
        for i in range(self.__height):
            t = t + str(i+1) + '　'
            if i+1 < 10:
                t = t + ' '
            for j in range(self.__width):
                # データを抜き出す
                if i * self.__width + j == self.__mistake_num:
                    t = t + self.__DATA[num + 1]
                else:
                    t = t + self.__DATA[num]
                # 最後は改行する必要はない
                if not self.__width - 1 == j:
                    t = t + ' '
            # 最後は改行する必要はない
            if not self.__height - 1 == i:
                t = t + '\n'
        print(t)

    def __change_input_number(self, input_str):
        if len(input_str) < 2:
            return 'error'
        # xとyを1~width,1~heightで表す(※1~です)
        try:
            x = self.__ALPHABET_UPPER.index(input_str[0]) + 1
        except ValueError:
            try:
                x = self.__ALPHABET_LOWER.index(input_str[0]) + 1
            except ValueError:
                return 'error'

        try:
            y = int(input_str[1:])
        except ValueError:
            return 'error'

        if (x > self.__width or 1 > x) or (y > self.__height or 1 > y):
            return 'error'
        return (y-1) * self.__width + x-1

    def __view_result(self, mistake_num, input_num, start_time):
        if mistake_num == input_num:
            print('正解です\n')
            self.__score -= (time.time()-start_time) * 2
        else:
            print('不正解です\n')
            self.__score = math.floor(self.__score / 2)

    def __get_input_number(self):
        while True:
            input_num = self.__change_input_number(input('座標を入力:'))
            if not input_num == 'error':
                return input_num

    def view_score(self):
        if self.__score < 0:
            self.__score = 0
        i = 0
        while self.__score < self.__LANK_SCORE[i]:
            i += 1
        print('あなたの点数は' + str(self.__score) + '点です')
        print('ランク' + self.__LANK[i])

    def play(self):
        start_time = time.time()
        self.__random_choice()
        self.__start_message()
        self.__section_message()
        self.__view_question()
        input_num = self.__get_input_number()
        self.__view_result(self.__mistake_num, input_num, start_time)
        self.__level += 1


if __name__ == '__main__':
    rps = RockPaperScissors()
    for i in range(10):
        rps.play()
    rps.view_score()
