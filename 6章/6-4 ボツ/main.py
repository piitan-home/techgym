"""Pythonでブラックジャックゲーム（トランプ）を作成します"""

import os
import json
import random
import requests
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

MARK = ['heart', 'spade', 'diamond', 'club']
MARK_EMOJI = ['♥', '♠',  '♦', '♣']
NAME = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
STANDARD_CHOICE = ["hit", "stand"]
NUMBER = [[1, 11], [2], [3], [4], [5], [6],
          [7], [8], [9], [10], [10], [10], [10]]
BLACKJACK = 21
BURST_SCORE = -1

SHOW_TOTAL_NUMBER = True
# コンピューターがディーラーの動作をするか、プレイヤーの動作をするか選択できます
COMPUTER_IS_DEALER = True
START_COIN = 100


class Card:
    '''cardが保存されているclassです'''
    def __init__(self, mark: str, name: str, number: int, image):
        self.mark = mark
        self.name = name
        self.number = number
        self.image = image

class Player:
    '''playerのclassです'''

    def __init__(self, name: str, coin: int):
        self.name = name
        self.coin = coin

        self._cards = []
        self._total_number = []
        self._score = 0

    def reset(self):
        '''playerの情報を初期化します'''
        self._cards.clear()
        self._total_number.clear()
        self._score = 0

    def show_cards(self):
        pass

    def _get_total_number(self):
        '''カードの合計値を求めます'''
        # [0]の行列を作成
        total_array = np.array([0], dtype=np.int32)
        # カードひとつづつで考える
        for card in self._cards:
            # 計算した番号を入れる用
            total = np.array([], dtype=np.int32)
            # カードの中の数字(Aは1と11に対応しているなど)を分割する
            for number in card.number:
                # totalに計算した番号を追加する
                total = np.block([total, total_array + number])
            total_array = total
        # np.arrayをlistにして、重複要素を削除する
        self._total_number = list(set(total_array.tolist()))

        # バーストしていない番号
        not_burst_number = [
            total for total in self._total_number if total <= BLACKJACK]
        self._score = max(not_burst_number + [BURST_SCORE])


    def deal_cards(self,*cards):
        for card in cards:
            self._cards.append(card)

class Human(Player):
    def choice(self):
        pass


class Computer(Player):
    def __init__(self, name: str, coin=0):
        super().__init__(name, coin)


class OneGame:
    def __init__(self, cards, *player):
        self._cards = cards
        self._human = player[0]
        self._computer = player[1]

    def deal_cards(self, player, number=1):
        if len(self._cards) < number:
            raise IndexError

        l = []
        for _ in range(number):
            rand = random.randrange(len(self._cards))
            l.append(self._cards[rand])
        
        player.deal_cards(l)

    def play(self):
        return (self._human, self._computer)


class Play:
    def __init__(self):
        self._human = None
        self._computer = None
        self._cards = []

    @staticmethod
    def _load_images():
        '''トランプの画像を読み込みます'''
        image_name = 'cards.jpg'
        image_path = os.path.abspath(f'{__file__}/{image_name}')
        vsplit_number = 4
        hsplit_number = 13

        if not os.path.isfile(image_path):
            response = requests.get(
                'http://3156.bz/techgym/cards.jpg', allow_redirects=False)
            with open(image_name, 'wb') as image:
                image.write(response.content)

        img = cv.imread(image_path)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        height, width = img.shape[:2]
        crop_img = img[:height // vsplit_number * vsplit_number,
                       :width // hsplit_number * hsplit_number]

        return [v_image for h_image in np.vsplit(crop_img, vsplit_number) for v_image in np.hsplit(h_image, hsplit_number)]

    def _get_cards(self):
        self._cards.clear()
        image = self._load_images()
        for i, mark in enumerate(MARK):
            for j, name in enumerate(NAME):
                self._cards.append(
                    {"mark": mark, "name": name, "number": name[j], 'mark_emoji': MARK_EMOJI[i], 'image': image[i*13+j]})

    def play(self):
        onegame = OneGame(self._cards, self._human, self._computer)
        self._human, self._computer = onegame.play()


play = Play()
play.play()
