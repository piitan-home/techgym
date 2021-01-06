import random
import sys
import math
import time

class RockPaperScissors():
    __RPS_NAME = ['グー','チョキ','パー']

    def __init__(self):
        tmp = 0
        self.hand = [[0,0,0],[0,0,0],[0,0,0]]

    def main(self):
        for i in range(30):
            self.__one_game()
        print(self.hand)

    def __one_game(self):
        com_hand = self.__get_com_hand()
        AI_hand = self.__get_AI_hand(com_hand)
        result = self.__get_WDL(com_hand,AI_hand)
        self.__update_AI(com_hand,AI_hand,result)
        self.__view_result(com_hand,AI_hand,result)

    def __get_AI_hand(self,com_hand):
        max = -1
        num = -1
        for i in range(3):
            if self.hand[com_hand][i] > max:
                max = self.hand[com_hand][i]
                num = i
            else:
                #逆数のほうがいいかも?
                if random.randrange(100 - (max - self.hand[com_hand][i])) > 50:
                    max = self.hand[com_hand][i]
                    num = i
                    
        return num

    def __get_WDL(self,com_hand,AI_hand):
        tmp = (com_hand - AI_hand)%3
        if tmp == 1:
            return 'win'
        elif tmp == 0:
            return 'draw'
        return 'lose'

    def __get_com_hand(self):
        return random.randint(0,2)

    def __update_AI(self,com_hand,AI_hand,result):
        #評価関数が思いつかなかったので一番簡単な方法を取りました
        if result == 'win':
            self.hand[com_hand][AI_hand] += 5
        elif result == 'lose':
            self.hand[com_hand][AI_hand] -= 5
        else:
            self.hand[com_hand][AI_hand] -= 1

    def __view_result(self,com_hand,AI_hand,result):
        print('乱数:' + self.__RPS_NAME[com_hand] + ' 対 コンピューター:' + self.__RPS_NAME[AI_hand] + 'の対戦の結果、', end = '')
        if result == 'win':
            print('コンピューターが勝ちました')
        elif result == 'draw':
            print('引き分けでした')
        else:
            print('コンピューターが負けました')

if __name__ == '__main__':
    rps = RockPaperScissors()
    rps.main()
