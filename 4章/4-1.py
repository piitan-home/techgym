# -*- coding: utf-8 -*-
import math
import random


class Player():
    def __init__(self, name, coin):
        self.cells = ['R','B','1','2','3','4','5','6','7','8','9']
        self.name = str(name)
        self.coin = coin
        self.bet_coin = 0
        self.bet_table = 0
        self.bets = {'R':0,'B':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0}

    def reset_table(self):
        self.bets = {'R':0,'B':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0}

    def info(self):
        print(self.name + ' : ' + str(self.coin))
    
    def show_coin(self):
        print(self.name + ':' + str(self.coin), end='')

    def get_coin(self):
        return self.coin

    def set_bet_coin(self):
        self.coin -= self.bet_coin
    
    def get_bets(self,name):
        return str(self.bets[name])
    
    def get_bet_table(self):
        return self.bet_table

    def show_bet_coin(self):
        print(self.name + 'は ' + str(self.bet_coin) + 'coin BETしました')
    
    def get_name(self):
        return self.name
    
    def set_bets(self):
        self.bets[self.bet_table] = self.bet_coin
        print(self.name + 'は ' + str(self.bet_coin) + 'コインを ' + self.bet_table + ' にBETしました')
    
    def get_cells(self):
        return self.cells
    
    def win_player(self, rate):
        self.coin += self.bet_coin * rate
        self.show_win_player(rate)
    
    def show_win_player(self, rate):
        print(self.name + 'は 当たりました  ' + str(self.bet_coin * rate) + 'コイン 獲得しました')

class Computer(Player):
    def __init__(self, name, coin):
        super().__init__(name, coin)

    def bet(self):
        bet_coin = random.randint(1,99)
        bet_coin = min(bet_coin, self.coin)
        self.bet_coin = bet_coin
    
    def set_bet_tables(self):
        self.bet_table = self.cells[random.randint(0,len(self.cells)-1)]
        self.set_bets()

#Playerを継承
class Human(Player):
    def __init__(self, name, coin):
        super().__init__(name, coin)

    def bet(self):
        max_bet_coin = min(99,self.coin)
        while True:
            bet_coin = input('何枚BETしますか? (1~' + str(max_bet_coin) + ') :')
            #入力された文字が正しければ終了
            if self.__enable_bet_coin(bet_coin, max_bet_coin):
                self.bet_coin = int(bet_coin)
                break
            print('正しい値を入力してください!')

    def __enable_bet_coin(self, string, max_bet_coin):
        #i+1の数字を文字に変換し、bet_coinを含んでいるかどうか
        return string in [str(i+1) for i in range(max_bet_coin)]
    
    def __enable_bet_cell(self, string):
        return string in self.cells

    def set_bet_tables(self):
        while True:
            bet_table = input('どこにBETしますか? (R,B,1~8) :')
            if self.__enable_bet_cell(bet_table):
                self.bet_table = bet_table
                self.set_bets()
                break
            print('正しい文字または値を入力してください!')

class Cell():
    def __init__(self, name, rate, color):
        self.name = str(name)
        self.rate = rate
        self.color = color
    
    def get_rate(self):
        return self.rate

    def __color_text(self,text,color):
        if color == 'red':
            color_base = ColorBase.RED
        elif color == 'green':
            color_base = ColorBase.GREEN
        else:
            color_base = ColorBase.BLACK

        print(color_base + str(text) + ColorBase.END,end='')

    def __green_bar(self):
        self.__color_text('|','green')

    def space(self):
        print(' ',end='')

    def show_tables(self,players):
        self.__green_bar()
        self.space()
        self.__color_text(self.name + '(×' + str(self.rate) + ')',self.color)
        self.space()
        self.__green_bar()
        for i in range(len(players)):
            self.space()
            print(players[i].get_bets(self.name).zfill(2),end='')
            self.space()
            self.__green_bar()
        print()
    
    def show_names(self,players):
        self.__green_bar()
        print(' _____ ',end='')
        self.__green_bar()
        for i in range(len(players)):
            self.space()
            print(players[i].get_name(),end='')
            self.space()
            self.__green_bar()
        print()

class ColorBase:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    END = '\033[0m'

def create_players():
    global players
    players.append(Human('MY',500))
    players.append(Computer('C1',500))
    players.append(Computer('C2',500))
    players.append(Computer('C3',500))

def bet():
    for player in players:
        player.bet()

def set_bet_coin():
    for player in players:
        player.set_bet_coin()
    
def set_bet_tables():
    for player in players:
        player.set_bet_tables()

def show_players():
    for player in players:
        player.info()

def show_coin():
    print('[持ちコイン] ', end='')
    for player in players:
        player.show_coin()
        print(' / ', end='')
    print()

def show_bet_coin():
    for player in players:
        player.show_bet_coin()

def reset_table():
    for player in players:
        player.reset_table()

def create_tables():
    global tables
    tables.append(Cell('R',8,'red'))
    tables.append(Cell('B',8,'black'))
    tables.append(Cell('1',2,'red'))
    tables.append(Cell('2',2,'black'))
    tables.append(Cell('3',2,'red'))
    tables.append(Cell('4',2,'black'))
    tables.append(Cell('5',2,'red'))
    tables.append(Cell('6',2,'black'))
    tables.append(Cell('7',2,'red'))
    tables.append(Cell('8',2,'black'))

def show_tables():
    tables[0].show_names(players)
    for table in tables:
        table.show_tables(players)

def check_hit():
    cells = players[0].get_cells()
    return cells[random.randint(0, len(cells)-1)]

def win_player(hit_cell):
    cells = players[0].get_cells()
    for player in players:
        bet_table = player.get_bet_table()
        if bet_table == hit_cell:
            number = cells.index(bet_table)
            rate = tables[number].get_rate()
            player.win_player(rate)

def show_check_hit_num(hit_cell):
    print('選ばれたのは 「' + hit_cell + '」 でした')

def reset():
    create_players()
    create_tables()

def is_game_end():
    for i in range(len(players)):
        if players[i].get_coin() == 0:
            return True
    return False

def play():
    show_tables()

    bet()

    set_bet_coin()
    set_bet_tables()

    show_tables()

    hit_cell = check_hit()
    show_check_hit_num(hit_cell)
    win_player(hit_cell)

    show_coin()

    return is_game_end()

players = []
tables = []
if __name__ == '__main__':
    reset()
    while True:
        if play():
            break
    print('持ちコインが0になったプレイヤーがいるので、ゲームを終了します。')