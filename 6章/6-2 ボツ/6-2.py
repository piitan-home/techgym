import os
import json
import random
import requests
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# import re で正規表現を使うといいらしい
# isdecimal() これでもいいかも
# テックジムのブラックジャックのルール説明がわかりませんでした
# [listに追加するもの for 変数 in リスト]
# [str(i) for i in range(10)] return -> 0~9までの文字が入ったlist



class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.total_num = [0]
        self.score = 0
        self.stand = False
        self.bet_coins = 1

    def deal_card(self, card):
        self.stand = False
        self.cards.append(card)
        self.get_total_number()
        self.get_score()

    def get_total_number(self):
        # 全ての合計の数値を計算
        self.total_num = [0]
        for card in self.cards:  # プレイヤーの持っているカード
            total = []
            for number in card.number:  # カードの番号1つ1つ取り出す 例)A→[1,11] 2→[2]
                # 取り出した番号と、現在のカードまでの番号をたす 例)A+2 = [1+2,11+2] = [3,13] numpyで行列を使っても良さそう
                total.extend(
                    [i+number for i in self.total_num if not i+number in total])
            self.total_num = total

        self.total_num.sort()  # 必要ないと思うが将来的なことを考えて追加

    def get_score(self):
        # blackjackを超えない最大値をスコアとして計算
        total_num = [i for i in self.total_num if i <= BLACKJACK]
        if len(total_num) == 0:  # 全てがblackjackを超えた場合
            self.score = INT_MIN
        else:
            self.score = max(total_num)

    def show_card(self, number):
        if number == 1:
            print(f'{self.name}のカードの1枚目 {[self.cards[0].name]}')
        else:
            # self.cardsから、nameを取り出す
            print(f'{self.name}のカード {[i.name for i in self.cards]}',end='')
            if SHOW_SUM:
                print(f' 合計{self.total_num}')
            else:
                print('')
        for i in range(number):
            plt.subplot(1, 6, i+1)
            plt.axis("off")
            plt.imshow(self.cards[i].image)
        plt.show()


class Human(Player):
    def choice(self):
        # choice pattern を一つ一つ読み込み、f'{choice}:{i+1}'を実行し、joinする
        # hit:1 stand:2 ...のようになる
        print(' or '.join(
            [f'{choice}:{i+1}' for i, choice in enumerate(CHOICE_PATTERN)]
        ))

        while True:
            number = input(f'{self.name}の行動を選択してください:')
            # number が数値なら
            if number.isdecimal():
                number = int(number)
                if 0 < number and number < len(CHOICE_PATTERN)+1:
                    return CHOICE_PATTERN[number-1]
            print('入力された文字に誤りがあります！')

    def bet(self):
        pass


class Computer(Player):
    def choice(self):
        return 'stand'

    def bet(self):
        self.bet_coins = 1


class Card:
    def __init__(self, mark, name, number, image):
        self.mark = mark
        self.name = name
        self.number = number
        self.image = image


class Play:
    def __init__(self):
        self.players = []
        self.cards = []


    def play(self):
        self.create_players()
        self.create_cards()
        one_game = OneGame(self.players, self.cards)
        self.players = one_game.one_game()

    def create_players(self):
        self.players.clear()
        self.players.append(Human('プレイヤー'))
        self.players.append(Computer('コンピューター'))

    def create_cards(self):
        image = self.load_image()
        self.cards.clear()
        for i, mark in enumerate(MARK):
            for j, name in enumerate(NAME):
                self.cards.append(
                    Card(mark, name, NUMBER[j], image[i*len(NAME)+j]))

    def load_image(self):
        image_name = 'cards.jpg'
        image_path = os.path.abspath(__file__ + '/../' + image_name)
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

        image = []
        for h_image in np.vsplit(crop_img, vsplit_number):
            for v_image in np.hsplit(h_image, hsplit_number):
                image.append(v_image)
        return image


class OneGame:
    def __init__(self, players, cards):
        self.players = players
        self.cards = cards

    def one_game(self):
        self.deal_card(self.players[0], 2)
        self.deal_card(self.players[1], 2)

        self.show_card(self.players[0])
        self.show_card(self.players[1], 1)

        while True:
            print()
            self.choice(self.players[0])
            print()
            self.choice(self.players[1])
            if self.is_game_over():
                break

        self.win_player()

        return self.players

    def win_player(self):
        # 全ての player の Score の最大値
        max_score = max([player.score for player in self.players])
        win_player = [player == max_score for player in self.players]

        # (負けた player がいない) または (勝った player がいない時)
        if not (False in win_player and True in win_player):
            pass
        else:
            pass

    def is_game_over(self):
        print([min(player.total_num) > BLACKJACK for player in self.players])
        # player に stand していない人がいないなら = 全ての人が stand したなら
        if not False in [player.stand for player in self.players]:
            return True
        # player に burst したひとがいるなら
        if True in [min(player.total_num) > BLACKJACK for player in self.players]:
            return True
        # player に blackjack したひとがいるなら
        if True in [BLACKJACK in player.total_num for player in self.players]:
            return True
        return False

    def choice(self, player):
        if player.stand is False:
            choice = player.choice()
            print(f'{player.name}は{choice}を選択しました')

            if choice == 'hit':
                self.deal_card(player)
            elif choice == 'stand':
                player.stand = True
        else:
            print(f'{player.name}はstandしています')

    def deal_card(self, player, number=1):
        if len(self.cards) < number:
            raise Exception('error:cardの枚数が足りません')
        for _ in range(number):
            rand = random.randrange(len(self.cards))
            player.deal_card(self.cards[rand])
            self.cards.pop(rand)

    def show_card(self, player, number=0):
        if number == 0:
            card_number = len(player.cards)
        else:
            card_number = number
        player.show_card(card_number)

class Settings():
    MARK = ['spade', 'club', 'diamond', 'heart']
    NAME = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    NUMBER = [[1, 11], [2], [3], [4], [5], [6],
            [7], [8], [9], [10], [10], [10], [10]]
    CHOICE_PATTERN = ["hit", "stand", "split",
                    "double_down", "surrender", "insurance"]
    INT_MIN = 0
    PATH = os.path.abspath(__file__ + '/../')

    BLACKJACK = 21
    SHOW_SUM = True
    setting = json.load(open(PATH + '/Settings.json', 'r'))

    choice = []
    for pattern in CHOICE_PATTERN:
        if pattern in setting['choice_pattern']:
            if setting['choice_pattern'][pattern] is True:
                choice.append(pattern)
        else:
            choice.append(pattern)

    CHOICE_PATTERN = choice

    SHOW_SUM = setting['show_sum']

if __name__ == "__main__":
    settings()
    play = Play()
    play.play()
