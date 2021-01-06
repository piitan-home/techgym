import random


class Play:
    RPS = ['グー', 'チョキ', 'パー']

    def play(self):
        print('じゃんけんスタート')
        my_hand = self.get_my_hand()
        com_hand = random.randint(1, 3)
        print('じゃんけん\nほい')
        self.winner(my_hand, com_hand)
        print(f'あなた:{self.RPS[my_hand-1]} コンピューター:{self.RPS[com_hand-1]}')

    @staticmethod
    def winner(my, com):
        tmp = (com-my) % 3
        if tmp == 0:
            print('引き分けです')
        elif tmp == 1:
            print('あなたの勝ちです')
        else:
            print('あなたの負けです')

    def get_my_hand(self):
        question = ','.join([f'{rps}:{i+1}' for i, rps in enumerate(self.RPS)])
        while True:
            my_hand = input(f'自分の手を入力してください\n({question})? ')
            if my_hand.isdecimal():
                my_hand = int(my_hand)
                if 1 <= my_hand and my_hand <= len(self.RPS):
                    return my_hand


if __name__ == "__main__":
    play = Play()
    play.play()
