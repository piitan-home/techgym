import random
import time

class RPS:
    def __init__(self):
        self.hands = ['グー','チョキ','パー']
        self.result = ['引き分けです','あなたの勝ちです','あなたの負けです']

    def start_message(self):
        print('じゃんけん、スタート！')

    def get_my_hand(self):
        print('あなたの手を入力してください')
        l = False
        #文字列を生成
        j = ''
        for i in range(len(self.hands)):
            if i != 0:
                j = j + ', '
            j = j + str(i) + ':' + self.hands[i]
        j = '(' + j + ')　:'
        #入力された文字が正しい値をとるまで繰り返し
        while not l:
            l = True
            k = input(j)
            try:
                k = int(k)
            except ValueError:
                print('正しい値を入力してください')
                l = False

            if l:
                if not(k%1 == 0 and 0 <= k and 2 >= k):
                    print('正しい値を入力してください')
                    l = False
        return k

    def get_you_hand(self):
        return random.randint(0, 2)

    def view_result(self,my_hand,you_hand,type_):
        global end
        if type_ == 0:
            print('じゃんけん')
        else:
            print('あいこで')
        time.sleep(1)
        print('ほい')
        time.sleep(1)
        print('あなたの手は ' + self.hands[my_hand])
        print('相手の手は ' + self.hands[you_hand])
        time.sleep(1)
        tmp = (you_hand - my_hand)%3
        if tmp == 0:
            print(self.result[tmp])
        else:
            print(self.result[tmp])
            end = True

end = False
rps = RPS()
rps.start_message()
rps.view_result(rps.get_my_hand(),rps.get_you_hand(),0)
while not end:
    rps.view_result(rps.get_my_hand(),rps.get_you_hand(),1)
