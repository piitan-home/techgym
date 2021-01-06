'''間違い探し'''

from random import randrange
from math import ceil, floor


class Point:
    '''class point\n
    x,y >= 0'''

    def __init__(self, x, y):
        self.new(x, y)

    def __eq__(self, obj):
        return obj.x == self._x and obj.y == self._y

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __add__(self, obj):
        return Point(self._x + obj.x, self._y + obj.y)

    def __sub__(self, obj):
        return Point(self._x - obj.x, self._y - obj.y)

    def __str__(self):
        return f'x:{self._x} y:{self._y}'

    @staticmethod
    def _alpha2num(alpha):
        if isinstance(alpha, int):
            return alpha
        if alpha.isdecimal():
            return int(alpha)
        if len(alpha) != 1:
            raise TypeError()
        return ord(alpha.upper()) - ord('A') + 1

    def new(self, x, y):
        '''set'''
        self._x = self._alpha2num(x)
        self._y = self._alpha2num(y)

    def set_(self, x, y):
        '''set'''
        self.new(x, y)

    def get(self):
        '''return x, y'''
        return (self._x, self._y)

    @property
    def x(self):
        '''x'''
        return self._x

    @property
    def y(self):
        '''y'''
        return self._y


class Game:
    '''間違い探しゲーム'''

    def __init__(self, text):
        self._text = text
        self._level = 1
        self._alphabet = [chr(i) for i in range(97, 97+26)]
        self._set_difficult()
        self._set_data()

        self._now_text = None
        self._answer = Point(0, 0)
        self._choice = Point(0, 0)
        self._type = 0

    def _get_size(self):
        return (self._difficult[self._level]['col'], self._difficult[self._level]['raw'])

    def _set_data(self):
        self._data = [[self._text[i*2+j]for j in range(2)]
                      for i in range(round(len(self._text)/2))]

    def _set_difficult(self):
        difficult = {}
        for i in range(13):
            difficult[i+1] = {'col': ceil(i/2)+3,
                              'raw': floor(i/2)+3}
        self._difficult = difficult

    def _set_text(self):
        rand = randrange(len(self._data))
        self._now_text = self._data[rand]

    def _set_answer(self):
        col, raw = self._get_size()
        self._answer.new(randrange(col), randrange(raw))

    def _set_choice(self):
        col, raw = self._get_size()
        while True:
            text = input('座標を入力してください (例:A1) :')
            if len(text) == 2:
                try:
                    choice = Point(text[0], text[1]) - Point(1, 1)
                except TypeError:
                    pass
                else:
                    if 0 <= choice.x < col and 0 <= choice.y < raw:
                        self._choice = choice
                        break

    def _show(self):
        col, raw = self._get_size()
        txt = ''
        txt += '  ' + ' '.join(self._alphabet[:col]) + '\n'
        for i in range(raw):
            txt += str(i+1) + ' '
            for j in range(col):
                if self._answer == Point(j, i):
                    txt += self._now_text[1]
                else:
                    txt += self._now_text[0]
            txt += '\n'
        print(txt.rstrip('\n'))

    def _is_answer(self):
        if self._answer == self._choice:
            print('正解です')
        else:
            print(
                f'間違いです 正解の座標:{self._alphabet[self._answer.y]}{self._answer.x + 1}')
        return self._answer == self._choice

    def play(self):
        while self._level <= 13:
            self._set_text()
            self._set_answer()
            self._show()
            self._set_choice()
            if self._is_answer():
                self._level += 1
            else:
                self._level = max(1, self._level-2)

        print('\nゲーム終了')

if __name__ == "__main__":
    game = Game('見貝土士眠眼己巳尤犬到致矢失白臼干千回同夭天二ニへヘ')
    game.play()
