import os
import random
import requests
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

MARK = ['spade', 'club', 'diamond', 'heart']
NAME = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
NUMBER = [[1, 11], [2], [3], [4], [5], [6],
          [7], [8], [9], [10], [10], [10], [10]]
high_score_path = os.path.abspath(__file__ + '/../' + 'high_score.text')


class Card:
    def __init__(self, mark, name, number, image):
        self.mark = mark
        self.name = name
        self.number = number
        self.image = image


class Player:
    def __init__(self, name, coins):
        self.coins = coins
        self.name = name
        self.cards = []
        self.total_number = []
        self.bet_coins = 1

    def deal_cards(self, cards):
        self.cards.append(cards)
        self.set_total_number()

    def set_total_number(self):
        total_number = [0]
        for card in self.cards:
            number = []
            for i in card.number:
                # 全てのnumberの数値を計算
                number.extend([i+j for j in total_number if not i+j in number])
            total_number = number
        self.total_number = total_number

    def get_wdl(self):
        if 21 in self.total_number:
            return 'win'
        elif 21 < min(self.total_number):
            return 'lose'
        return 'none'

    def reset(self):
        self.cards = []
        self.total_number = [0]
        self.bet_coins = 1


class Human(Player):
    def __init__(self, name, coins):
        super().__init__(name, coins)

    def set_bet_coins(self):
        bet_coins = 0
        while not bet_coins in [str(i+1) for i in range(self.coins)]:
            print(f'{self.name}がBETするコインの枚数を入力してください')
            bet_coins = input(f'現在の所持コイン:{self.coins} (')
        self.bet_coins = int(bet_coins)

    def get_action(self):
        action = 0
        while not action in [str(i+1) for i in range(2)]:
            action = input('stand:1 hit:2 (')
        return int(action)

    def get_coins(self, mag):
        self.coins += self.bet_coins * mag


class Computer(Player):
    def __init__(self, name, coins):
        super().__init__(name, coins)

    def set_bet_coins(self):
        pass

    def get_action(self):
        pass

    def get_coins(self, mag):
        pass


class Play:
    def __init__(self):
        self.image = self.load_image()
        self.cards = self.get_cards(self.image)
        self.human = Human('あなた', 100)
        self.computer = Computer('コンピューター', 100)
        self.cards_number = []
        self.turns = 1

    def rules(self):
        print('\nプレイヤーの目標は、21を超えないように手持ちのカードの点数の合計を21に近づけ、\nその点数がディーラー(コンピューター)を上回ることです\n')
        print('各カードの点数は以下のとおりです(複数の点数がある場合は好きな方を選択)')
        list_score = []
        for i, name in enumerate(NAME):
            list_score.append(
                f'{name}:{"または".join([str(j) for j in NUMBER[i]])}点')
        print(list_score)
        print('\nまず、プレイヤーに2枚のカードが配られ、')
        print('ディーラーはカードの合計点数が17点を超すまでカードを引きます\n')

        print('プレイヤー、ディーラーともに、カードの合計点数が21点を超えると負け(バスト)、')
        print('21点ぴったりの場合は勝ち(ブラックジャック)となります\n')

        print('この時点で勝負がついていない場合、')
        print('プレイヤーは行動を選択します\n')

        print('stand:いまのカードで勝負 hit:もう一枚引いて勝負')
        print('(プレイヤーは21点を超えるまでhitすることができます)\n')

        print('ここで、バスト、ブラックジャックの場合は勝ちが確定します')
        print('(双方バスト、またはブラックジャックの場合は引き分け)\n')

        print('バスト、ブラックジャックでない場合、合計点数が多い方の勝ちとなります')
        input('エンターキーでゲームを開始します')

    def play(self):
        print('ブラックジャックを始めます')

        rule = input('ルールを聞きますか? Y/n (')
        if rule in ['Y', 'y', 'yes', 'Yes', 'YES']:
            self.rules()

        print('\nゲームスタート!\n')

        self.show_coins()
        end = 'y'
        while end in ['Y', 'y', 'yes', 'Yes', 'YES']:
            self.one_game()
            self.show_coins()
            if self.human.coins == 0:
                print(f'{self.human.name}のコインの枚数が0枚になったためゲームを終了します')
            end = input('続けますか? Y/n (')
            print()
        self.high_score()

    def show_coins(self):
        print(f'{self.human.name}の所持コイン:{self.human.coins}')

    def high_score(self):
        if self.human.coins > self.get_high_score():
            print('ハイスコア更新!')
            self.show_coins()
            self.update_high_score()
        else:
            self.show_coins()
            print(f'ハイスコア:{self.get_high_score()}')

    def update_high_score(self):
        with open(high_score_path) as f:
            high_score = f.read()
        with open(high_score_path, mode='w') as f:
            f.write(high_score + '\n' + str(self.human.coins))

    def get_high_score(self):
        with open(high_score_path) as f:
            high_score = [s.strip() for s in f.readlines()][-1]
        return int(high_score)

    def one_game(self):
        self.reset()
        self.deal_cards(self.human, self.human, self.computer, self.computer)
        self.show_cards(self.human)
        self.show_one_card(self.computer)
        print()
        self.human.set_bet_coins()
        print()

        while max(self.computer.total_number) < 17:
            self.deal_cards(self.computer)
        while True:
            if self.is_game_end():
                break

            self.turns += 1
            self.show_cards(self.human)

            action = self.human.get_action()
            if action == 1:
                break
            elif action == 2:
                self.deal_cards(self.human)
            print()

        self.winner()

    def winner(self):
        human = self.human.get_wdl()
        computer = self.computer.get_wdl()
        print()
        if (human == 'win' and computer == 'win') or (human == 'lose' and computer == 'lose'):
            print('引き分けです')

        elif human == 'win' or computer == 'lose':
            if self.turns == 1:
                self.human.get_coins(1.5)
                print(f'{self.human.name}の勝ちです 払い戻し*2.5')
            else:
                self.human.get_coins(1)
                print(f'{self.human.name}の勝ちです 払い戻し*2')

        elif human == 'lose' or computer == 'win':
            self.human.get_coins(-1)
            print(f'{self.human.name}の負けです')

        else:
            human_total = max([i for i in self.human.total_number if i < 22])
            computer_total = max(
                [i for i in self.computer.total_number if i < 22])

            if human_total > computer_total:
                self.human.get_coins(1)
                print(f'{self.human.name}の勝ちです 払い戻し*2')
            elif human_total == computer_total:
                print('引き分けです')
            else:
                self.human.get_coins(-1)
                print(f'{self.human.name}の負けです')

        self.show_cards(self.computer)
        self.show_cards(self.human)

    def is_game_end(self):
        return not (self.human.get_wdl() == 'none' and self.computer.get_wdl() == 'none')

    def reset(self):
        self.human.reset()
        self.computer.reset()
        self.cards_number = list(range(len(self.cards)))
        self.turns = 1

    def show_cards(self, players):
        print(
            f'{players.name}のカード {[i.name for i in players.cards]} total:{players.total_number}')
        for j, card in enumerate(players.cards):
            plt.subplot(1, 6, j+1)
            plt.axis("off")
            plt.imshow(card.image)
        plt.show()

    def show_one_card(self, players):
        print(
            f'{players.name}のカードの1枚目 {[players.cards[0].name]}')
        plt.subplot(1, 6, 1)
        plt.axis("off")
        plt.imshow(players.cards[0].image)
        plt.show()

    def deal_cards(self, *players):
        for player in players:
            rand = random.randrange(len(self.cards_number))
            player.deal_cards(self.cards[rand])
            self.cards_number.pop(rand)

    def get_cards(self, image):
        card = []
        for i, mark in enumerate(MARK):
            for j, name in enumerate(NAME):
                card.append(Card(mark, name, NUMBER[j], image[i*len(NAME)+j]))
        return card

    def load_image(self):
        card_images = []
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

        card_images.clear()
        for h_image in np.vsplit(crop_img, vsplit_number):
            for v_image in np.hsplit(h_image, hsplit_number):
                card_images.append(v_image)

        return card_images


if __name__ == "__main__":
    play = Play()
    play.play()
