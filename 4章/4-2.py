# -*- coding: utf-8 -*-

#前回の反省点 グローバル変数(リスト)/関数が多すぎた
#　　　　　　 classが多くてわかりにくい
#　　　　　　 単純に関数が多かった

import math
import random

class ColorBase:
    #連想配列にしたら、簡潔にかけました
    COLOR_BASE = {'black':'\033[30m','red':'\033[31m','green':'\033[32m',
                  'yellow':'\033[33m','blue':'\033[34m','magenta':'\033[35m',
                  'cyan':'\033[36m','end':'\033[0m'}
    def color_text(self, text, color):
        return self.COLOR_BASE[color] + str(text) + self.COLOR_BASE['end']
    
    def green_bar(self):
        return self.color_text('|', 'green')

class Player(ColorBase):
    def __init__(self, name, coin):
        self.name = str(name)
        self.coin = int(coin)
        self.bet_coin = 0
        self.bet_cell = 0
        self.bets = {}
        #書き方は良いかわからないが、関数を実行
        self.init_bets()
    
    def set_bet_coins(self):
        self.coin -= self.bet_coin
        print(super().color_text(self.name,'magenta') + 'は ' + 
              super().color_text(self.bet_coin,'cyan') + 'coinを ' + 
              super().color_text(self.bet_cell,'cyan') + 'に BETしました')

    def info(self):
        print(self.name + ' : ' + str(self.coin))

    def init_bets(self):
        self.bets = {}
        table_names = Cell.TABLE_NAMES
        for i in range(len(table_names)):
            self.bets[table_names[i]] = 0
    
    def update_bets(self):
        self.bets[self.bet_cell] = self.bet_coin
    
    def win_player(self, rate):
        get_coins = self.bet_coin * rate
        print(super().color_text(self.name,'magenta') + 'は' + 
              super().color_text(get_coins,'cyan') + 'coinを獲得しました')
        self.coin += get_coins

class Human(Player):
    def __init__(self, name, coin):
        super().__init__(name, coin)
    
    def get_bet_coins(self):
        max_bet_coin = min(self.coin,99)
        while True:
            bet_coin = input('何枚BETしますか? (1~' + str(max_bet_coin) + ') :')
            if bet_coin in [str(i+1) for i in range(max_bet_coin)]:
                break
            print('正しい値を入力してください!')
        self.bet_coin = int(bet_coin)

    def get_bet_cell(self):
        while True:
            bet_cell = input('どこにBETしますか? (R,B,1~8) :')
            if bet_cell in Cell.TABLE_NAMES:
                break
            print('正しい文字または値を入力してください!')
        self.bet_cell = bet_cell

class Cell():
    TABLE_NAMES = ['R','B','1','2','3','4','5','6','7','8']
    def __init__(self, name, rate, color):
        self.name = name
        self.rate = rate
        self.color = color

class Computer(Player):
    def __init__(self, name, coin):
        super().__init__(name, coin)
    
    def get_bet_coins(self):
        self.bet_coin = random.randint(1,min(self.coin,99))
    
    def get_bet_cell(self):
        table_names = Cell.TABLE_NAMES
        self.bet_cell = table_names[random.randrange(len(table_names))]

class Play(ColorBase):
    def __init__(self):
        self.players = []
        self.tables = []
        self.hit_name = 0

    def init(self):
        self.__create_tables()
        self.__create_players()
        self.__show_coin()

    def __input(self):
        self.__get_bet_coins()
        self.__get_bet_cell()

    def play(self):
        self.__init_bets()
        self.__input()
        self.__set_bet_coins()
        self.__update_bets()
        self.__show_table()
        self.__check_hit()
        self.__win_player()
        self.__show_coin()
        return self.__is_not_game_end()
    
    def __init_bets(self):
        for player in self.players:
            player.init_bets()

    def __show_coin(self):
        text = '[持ちコイン]'
        for player in self.players:
            text += ' ' + super().color_text(player.name,'magenta') + ':' + super().color_text(player.coin,'cyan') + ' /'
        print(text)

    def __check_hit(self):
        table_names = Cell.TABLE_NAMES
        self.hit_name = table_names[random.randrange(len(table_names))]
    
    def __win_player(self):
        print('選ばれたのは「' + super().color_text(self.hit_name,'magenta') + '」でした')
        rate = self.tables[Cell.TABLE_NAMES.index(self.hit_name)].rate
        for player in self.players:
            if player.bet_cell == self.hit_name:
                player.win_player(rate)

    def __set_bet_coins(self):
        for player in self.players:
            player.set_bet_coins()
    
    def __update_bets(self):
        for player in self.players:
            player.update_bets()

    def __show_table(self):
        green_bar = super().green_bar()

        text = ''
        #1番上の欄の文字を生成
        text += green_bar + ' _____ ' + green_bar
        for player in self.players:
            text += ' ' + super().color_text(player.name,'magenta') + ' ' + green_bar

        for table in self.tables:
            text += '\n' + green_bar + ' ' #左の緑のバー
            temp = table.name + '(×' + str(table.rate) + ')'
            text += super().color_text(temp , table.color)
            text += ' ' + green_bar #右の緑のバー
            for player in self.players:
                text += ' '
                text += str(player.bets[table.name]).zfill(2) #2桁で0埋め
                text += ' ' + green_bar
        print(text)

    def __create_players(self):
        self.players = []
        self.players.append(Human('MY',500))
        self.players.append(Computer('C1',500))
        self.players.append(Computer('C2',500))
        self.players.append(Computer('C3',500))
    
    def __get_bet_coins(self):
        for player in self.players:
            player.get_bet_coins()
    
    def __get_bet_cell(self):
        for player in self.players:
            player.get_bet_cell()
    
    def __create_tables(self):
        self.tables = []
        self.tables.append(Cell('R',8,'red'))
        self.tables.append(Cell('B',8,'black'))
        self.tables.append(Cell('1',2,'red'))
        self.tables.append(Cell('2',2,'black'))
        self.tables.append(Cell('3',2,'red'))
        self.tables.append(Cell('4',2,'black'))
        self.tables.append(Cell('5',2,'red'))
        self.tables.append(Cell('6',2,'black'))
        self.tables.append(Cell('7',2,'red'))
        self.tables.append(Cell('8',2,'black'))
    
    def __is_not_game_end(self):
        player_list = []
        for player in self.players:
            if player.coin == 0:
                player_list.append(player.name)
        if len(player_list) == 0:
            return False
        return player_list #空の文字列&リスト、0、Falseでない限り、全てTrue
    
    def game_end(self, player_l):
        player_list = player_l
        for i in range(len(player_list)):
            player_list[i] = super().color_text(player_list[i],'magenta')
        player_list = 'と'.join(player_list)
        print(player_list + 'の持ちコインがなくなったため、ゲームを終了します')

if __name__ == "__main__":
    play = Play()
    play.init()
    while True:
        player_list = play.play()
        if player_list:
            break
    play.game_end(player_list)
