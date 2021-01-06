'''ジャンケンゲーム〜'''
import random


class Play:
    '''class play'''
    RPS = ['グー', 'チョキ', 'パー']

    def __init__(self, life=3):
        self.life = life
        self.player_life = None
        self.computer_life = None
        self.reset()

    def color_text(self, text, color):
        '''return color text'''
        COLOR_BASE = {'black': '\033[30m', 'red': '\033[31m', 'green': '\033[32m',
                      'yellow': '\033[33m', 'blue': '\033[34m', 'magenta': '\033[35m',
                      'cyan': '\033[36m', 'end': '\033[0m'}
        return COLOR_BASE[color] + str(text) + COLOR_BASE['end']

    def reset(self):
        '''restartします'''
        self.player_life = self.life
        self.computer_life = self.life

    def play(self):
        '''ライフが0になるまでゲームを実行します'''
        while True:
            while not (self.player_life == 0 or self.computer_life == 0):
                self.one_game()
            if self.player_life == 0:
                print(self.color_text('\n最終結果:コンピューターの勝ち', 'magenta'))
            else:
                print(self.color_text('\n最終結果:あなたの勝ち', 'cyan'))

            if self.replay() is False:
                break
            self.reset()

    @staticmethod
    def replay():
        '''もう一度プレイするか入力します'''
        while True:
            text = input('再戦しますか Y/n:')
            if text.lower() in ['yes', 'y', 'no', 'n']:
                return text.lower() in ['yes', 'y']
            print('入力に誤りがあります')

    def one_game(self):
        '''1ゲームだけ行います'''
        print('じゃんけんスタート')
        my_hand = self.get_my_hand()
        com_hand = self.get_com_hand()

        print('\nじゃんけん ほい')
        self.winner(my_hand, com_hand)

        print(f'あなた:{self.RPS[my_hand-1]} コンピューター:{self.RPS[com_hand-1]}')
        print(f'あなたのライフ:{self.player_life} コンピューター:{self.computer_life}\n')

    @staticmethod
    def get_com_hand():
        '''get -> computer_hand'''
        return random.randint(1, 3)

    def winner(self, my_hand, com_hand):
        '''winner'''
        tmp = (com_hand-my_hand) % 3
        if tmp == 0:
            print(self.color_text('引き分けです', 'green'))
        elif tmp == 1:
            print(self.color_text('あなたの勝ちです', 'cyan'))
            self.computer_life -= 1
        else:
            print(self.color_text('あなたの負けです', 'magenta'))
            self.player_life -= 1

    def get_my_hand(self):
        '''get -> my_hand'''
        question = ','.join([f'{rps}:{i+1}' for i, rps in enumerate(self.RPS)])
        while True:
            my_hand = input(f'自分の手を入力してください\n({question})? ')
            if my_hand.isdecimal():
                my_hand = int(my_hand)
                if 1 <= my_hand <= len(self.RPS):
                    return my_hand


if __name__ == "__main__":
    play = Play()
    play.play()
