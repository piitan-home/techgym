'''cardの情報を扱っています'''
import os
import random

import requests
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from .combinations import ListCombinations


class CardInfo:
    '''CardInfomation'''
    MARK = ('heart', 'spade', 'diamond', 'club')
    MARK_NUM = 4
    MARK_EMOJI = ('♥', '♠',  '♦', '♣')
    NAME = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    NAME_NUM = 13
    NUMBER = ((1, 11), 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10)
    BLACKJACK_SCORE = 21
    BUST_SCORE = -1
    SURRENDER_SCORE = -2
    BASE_SCORE = 0


class Card:
    '''Cardの情報を持つclassです'''

    def __init__(self, mark_num: str, name_num: str, image):
        self.mark_num = mark_num
        self.name_num = name_num
        self.image = image

    def __str__(self):
        return f'{self.mark_emoji}{self.name}'

    def __eq__(self, obj):
        if isinstance(obj, Card):
            return obj.name_num == self.name_num
        if isinstance(obj, int):
            return obj == self.name_num+1
        return False

    def __ne__(self, obj):
        return not self.__eq__(obj)

    @property
    def mark(self) -> str:
        '''return mark'''
        return CardInfo.MARK[self.mark_num]

    @property
    def name(self) -> str:
        '''return name'''
        return CardInfo.NAME[self.name_num]

    @property
    def mark_emoji(self) -> str:
        '''return mark_emoji'''
        return CardInfo.MARK_EMOJI[self.mark_num]

    @property
    def number(self) -> str:
        '''return number'''
        return CardInfo.NUMBER[self.name_num]


class CardSet:
    '''class card_set'''

    def __init__(self):
        self.cards = []
        self.numbers = []

    @staticmethod
    def __get_images() -> list:
        '''トランプの画像を読み込みます'''

        os.chdir(os.path.abspath(__file__+'/../../'))

        h_num = CardInfo.MARK_NUM
        w_num = CardInfo.NAME_NUM
        image_name = 'cards.jpg'

        if not os.path.isfile(image_name):
            response = requests.get(
                'http://3156.bz/techgym/cards.jpg', allow_redirects=False)
            with open(image_name, 'wb') as image:
                image.write(response.content)

        img = cv.imread('./'+image_name)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        h, w = img.shape[:2]
        crop_img = img[:h // h_num * h_num,
                       :w // w_num * w_num]

        images = []
        for h_image in np.vsplit(crop_img, h_num):
            for v_image in np.hsplit(h_image, w_num):
                images.append(v_image)
        return images

    def __get_cards(self) -> list:
        '''get cards'''
        mark_num = CardInfo.MARK_NUM
        name_num = CardInfo.NAME_NUM
        images = self.__get_images()
        cards = []
        for i in range(mark_num):
            for j in range(name_num):
                cards.append(Card(i, j, images[i*name_num+j]))
        return cards

    def reset(self):
        '''reset'''
        self.cards = self.__get_cards()
        self.numbers = list(range(len(self.cards)))
        self.shuffle()

    def shuffle(self):
        '''shuffle'''
        random.shuffle(self.numbers)

    def deal(self, leave=False) -> Card:
        '''deal cards'''
        number = random.randrange(len(self.numbers))
        if not leave:
            self.numbers.pop(number)
        return self.cards[number]


class PlayerCard:
    '''プレイヤーのカード情報を保存します'''

    def __init__(self):
        self.cards = []
        self.is_stand = False
        self.is_surrender = False
        self.reset()

    def reset(self):
        '''reset'''
        self.cards = []
        self.is_stand = False
        self.is_surrender = False

    def set_surrender(self):
        '''set surrender'''
        self.is_surrender = True
        self.set_stand()

    def set_stand(self):
        '''set stand'''
        self.is_stand = True

    def __auto_stand(self):
        if self.score <= CardInfo.BUST_SCORE or self.score == CardInfo.BLACKJACK_SCORE:
            self.set_stand()

    def add(self, *cards: Card):
        '''add'''
        self.cards.extend(list(cards))
        self.__auto_stand()

    @property
    def is_bust(self):
        '''is bust'''
        return self.score <= CardInfo.BUST_SCORE

    @property
    def total(self) -> list:
        '''get total'''

        ListCombinations()
        total = ListCombinations.combinations(
            [card.number for card in self.cards])
        total = [sum(t)+CardInfo.BASE_SCORE for t in total]

        return tuple(set(total))  # 複数要素を除外

    @property
    def score(self) -> int:
        '''get score'''
        if self.is_surrender:
            return CardInfo.SURRENDER_SCORE

        score = self.total + (CardInfo.BUST_SCORE,)
        # ブラックジャックの数字よりも超えているもの（バースト）を排除
        score_list = [i for i in score if i <= CardInfo.BLACKJACK_SCORE]
        return max(score_list)

    def show(self, row=1, col=6):
        '''show_cards'''
        for i, card in enumerate(self.cards):
            plt.subplot(row, col, i + 1)
            plt.axis('off')
            plt.imshow(card.image)
        plt.show()

    def text(self):
        '''get card text'''
        txt = ''
        for card in self.cards:
            txt += f"[{str(card)}]"
        return txt.rstrip()
