"""Pythonでブラックジャックゲームを作ります"""

import os
import json
import random
import requests
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


class Info:
    """ゲームルールを管理するclassです"""
    mark = ['heart', 'spade', 'diamond', 'club']
    mark_emoji = ['♥', '♠',  '♦', '♣']
    name = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    choice = ["hit", "stand"]
    number = [[1, 11], [2], [3], [4], [5], [6],
              [7], [8], [9], [10], [10], [10], [10]]
    blackjack = 21
    show_total_number = True
    start_coin = 100

    # 固定
    file_path = os.path.abspath(__file__ + '/../')
    int_min = -1

    def __init__(self):
        with open(self.file_path + '/Settings.json') as k:
            json_file = json.load(k)

        if 'show_total_number' in json_file:
            self.show_total_number = json_file['show_total_number']

        if 'start_coin' in json_file:
            self.start_coin = json_file['start_coin']


class Card:
    '''カードの情報が入ったclassです'''

    def __init__(self, mark: str, mark_num: int, name: str, name_num: int, number: int, image):
        self.mark = mark
        self.mark_num = mark_num
        self.name = name
        self.name_num = name_num
        self.number = number
        self.image = image


class Player:
    '''プレイヤー情報が入ったclassです'''

    def __init__(self, info, name: str, coin: int):
        self.info = info
        self.name = name
        self.coin = coin

        self.cards = []
        self.max_score = 0
        self.__total_number = []
        self.stand = False

        self.restart()

    def restart(self):
        self.cards = []
        self.max_score = 0
        self.__total_number = []
        self.stand = False

    def __get_total_number(self):
        total = np.array([0], dtype=np.int32)  # 初めはゼロ
        for card in self.cards:
            total_2 = np.array([], dtype=np.int32)
            for number in card.number:
                # すべてのパターンを計算(total+number)し、結合(np.block)
                total_2 = np.block([total_2, total + number])
            total = total_2
        # np.arrayから、listに変換し、重複を削除
        self.__total_number = list(set(total.tolist()))

    def __get_max_score(self):
        # total_number(全てのパターン)が、バーストしない場合を選択し、最大値を計算する 全てがバーストした場合、0とする
        self.max_score = max([i for i in self.__total_number if i <=
                              self.info.blackjack] + [self.info.int_min])

    def deal_card(self, card):
        self.cards.append(card)
        self.__get_total_number()
        self.__get_max_score()

    def show_cards(self, number=0):  # この前の関数でもnumber = Noneと定義されているので必要ないが一応書いておく
        if number == 0:
            num = len(self.cards)
        else:
            num = number

        txt = f'{self.name}のcard:' + str([self.info.mark_emoji[card.mark_num] + card.name for i,card in enumerate(self.cards) if i < num])
        if (self.info.show_total_number is True) and len(self.cards) == num:
            txt += f' total:{self.__total_number}'
        print(txt)

        for i in range(num):
            plt.subplot(1, 6, i+1)
            plt.axis("off")
            plt.imshow(self.cards[i].image)
        plt.show()


class Human(Player):
    def choice(self) -> int:
        while True:
            choice = input(
                ' '.join([f'{choice}:{i+1}' for i, choice in enumerate(self.info.choice)])+' ')
            if choice.isdecimal() is True:
                choice = int(choice)
                if choice <= len(self.info.choice) and choice > 0:
                    return self.info.choice[choice-1]


class Computer(Player):
    def __init__(self, info, name: str):
        super().__init__(info, name, 0)

class OneGame:
    def __init__(self, info, cards, *player):
        self.__info = info
        self.__cards = cards
        self.__computer = player[0]
        self.__human = player[1]

    def __restart_player(self):
        self.__computer.restart()
        self.__human.restart()

    def play(self):
        self.__restart_player()
        self.__deal_card(self.__human, 2)
        self.__deal_card(self.__computer, 2)

        self.__show_cards(self.__human)
        self.__show_cards(self.__computer,1)

        while not self.__computer.max_score >= 17:
            self.__deal_card(self.__computer, 1)
        
        while not (self.__human.stand is True or self.__human.max_score == self.__info.int_min):
            choice = self.__human.choice()
            if choice == 'hit':
                self.__deal_card(self.__human, 1)
            else:
                self.__human.stand = True

        self.__game_over()

        self.__show_cards(self.__human)
        self.__show_cards(self.__computer)

        return (self.__computer, self.__human)

    def __game_over(self):
        h_score = self.__human.max_score
        c_score = self.__computer.max_score
        if h_score == c_score:
            print('引き分けです')
        elif h_score > c_score:
            print(f'{self.__human.name}の勝ちです')
        elif h_score < c_score:
            print(f'{self.__human.name}の負けです')

    def __show_cards(self, player, number=0):
        player.show_cards(number)

    def __deal_card(self, player, number=1):
        if len(self.__cards) < number:
            raise Exception('NotEnoughCardsError')

        for _ in range(number):
            rand = random.randrange(len(self.__cards))
            player.deal_card(self.__cards[rand])
            self.__cards.pop(rand)


class Play:
    def __init__(self):
        self.__info = Info()
        self.__cards = self.__create_cards()
        self.__human = None
        self.__computer = None

    def play(self):
        self.__create_players()
        one_game = OneGame(self.__info, self.__cards,
                           self.__computer, self.__human)
        (self.__computer, self.__human) = one_game.play()

    def __create_players(self):
        self.__human = Human(self.__info, 'human', self.__info.start_coin)
        self.__computer = Computer(self.__info, 'computer')

    def __create_cards(self):
        image = self.__load_images()

        return [Card(mark, i, name, j, self.__info.number[j], image[i*len(self.__info.name)+j])
                for i, mark in enumerate(self.__info.mark) for j, name in enumerate(self.__info.name)]  # とてもわかりにくいですが、短くしました

    def __load_images(self):
        image_name = 'cards.jpg'
        image_path = f'{self.__info.file_path}/{image_name}'
        vsplit_number = 4
        hsplit_number = 13

        if not os.path.isfile(image_path):
            response = requests.get(
                'http://3156.bz/techgym/cards.jpg', allow_redirects=False)
            with open(image_name, 'wb') as image:
                image.write(response.content)

        img = cv.imread(image_path)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        h, w = img.shape[:2]
        crop_img = img[:h // vsplit_number * vsplit_number,
                       :w // hsplit_number * hsplit_number]

        return [v_image for h_image in np.vsplit(crop_img, vsplit_number) for v_image in np.hsplit(h_image, hsplit_number)]


if __name__ == "__main__":
    play = Play()
    play.play()
