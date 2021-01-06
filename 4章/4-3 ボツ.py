#自分でも、よくわからないプログラムになったので、中断しました
#目標 もう少し、変数/関数を隠す
#command shift p → python select interpreter
import os
import sys
import random

class Player():
    def __init__(self, name, coin, tables):
        #変数を隠してみる
        self.__name = str(name)
        self.__coin = int(coin)
        self.__bet_coin = 0
        self.__tables = tables
        self.__bets = self.__init_bets()
    
    def __init_bets(self):
        bets = {}
        for table in self.__tables:
            bets[table.get_info()['name']] = 0
        return bets
    
    def get_bets_info(self, name):
        return self.__bets[name]
    
    def info(self):
        print(self.__name + ' : ' + str(self.__coin))
    
    def set_bet_coin(self, coin):
        self.__bet_coin = coin
        self.__coin -= coin
    
    def show_bet_coin(self):
        print(self.__name + 'は' + str(self.__bet_coin) + 'coin BETしました')
    
    def get_max_bet_coin(self):
        return min(99,self.__coin)
    
    def get_name(self):
        return self.__name

class Human(Player):
    def __init__(self, name, coin, tables):
        super().__init__(name, coin, tables)
    
    def bet(self):
        while True:
            max_bet_coin = super().get_max_bet_coin()
            bet_coin = input('何枚BETしますか? (1-' + str(max_bet_coin) + ') :')
            if bet_coin in [str(i+1) for i in range(max_bet_coin)]:
                super().set_bet_coin(int(bet_coin))
                break
            print('正しい値を入力してください')

class Computer(Player):
    def __init__(self, name, coin, tables):
        super().__init__(name, coin, tables)

    def bet(self):
        bet_coin = random.randint(1,super().get_max_bet_coin())
        super().set_bet_coin(bet_coin)

class ColorBase():
    COLOR_BASE = {'black':'\033[30m','red':'\033[31m','green':'\033[32m',
                  'yellow':'\033[33m','blue':'\033[34m','magenta':'\033[35m',
                  'cyan':'\033[36m','end':'\033[0m'}

    def color_text(self, text, color):
        return self.COLOR_BASE[color] + str(text) + self.COLOR_BASE['end']
    def green_bar(self):
        return self.color_text('|', 'green')

class Cell():
    def __init__(self, name, length):
        self.__name = str(name)
        if name in ['R','B']:
            self.__rate = 2
            self.__color = {'R':'red','B':'black'}[name]
        else:
            self.__rate = length-2
            self.__color = {1:'red',0:'black'}[int(name)%2]
        self.length = length

    def get_info(self):
        return {'name':self.__name, 'rate':self.__rate, 'color':self.__color}

class Play():
    def __init__(self):
        self.__players = []
        self.__tables = []
        self.__tables_names = []
        #委譲?
        self.__color_base = ColorBase()

    def play(self):
        self.__create_tables()
        self.__create_players()
        self.__show_players()
        self.__bet()
        self.__show_bet_coin()
        self.__show_tables()
    
    def __create_players(self):
        self.__players.clear()
        self.__players.append(Human('MY', 500, self.__tables))
        self.__players.append(Computer('C1', 500, self.__tables))
        self.__players.append(Computer('C2', 500, self.__tables))
        self.__players.append(Computer('C3', 500, self.__tables))
    
    def __bet(self):
        for player in self.__players:
            player.bet()

    def __show_bet_coin(self):
        for player in self.__players:
            player.show_bet_coin()

    def __show_players(self):
        for player in self.__players:
            player.info()

    def __show_tables(self):
        green_bar = self.__color_base.green_bar()

        txt = green_bar + ' _____ ' + green_bar
        for player in self.__players:
            txt += ' ' + self.__color_base.color_text(player.get_name(),'red') + ' ' + green_bar
        for info in self.__get_table_info():
            txt += '\n' + green_bar + ' '
            txt += self.__color_base.color_text(info['name'] + '(x' + str(info['rate']) + ') ',info['color'])
            txt += green_bar
            for player in self.__players:
                txt += ' ' + str(player.get_bets_info(info['name'])).zfill(2) + ' ' + green_bar
        print(txt)     

    def __get_table_info(self):
        table_info = []
        for table in self.__tables:
            table_info.append(table.get_info())
        return table_info

    def __create_tables(self):
        self.__tables.clear()

        names = [str(i+1) for i in range(6)]
        names.insert(0,'R')
        names.insert(1,'B')
        self.__tables_names = names

        for name in names:
            self.__tables.append(Cell(name, len(names)))
        

if __name__ == "__main__":
    play = Play()
    play.play()