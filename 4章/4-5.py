'''カジノゲーム'''

from random import randrange
from math import ceil


class Color:
    '''class Color'''
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    __end = '\033[0m'

    @classmethod
    def str2color(cls, color):
        '''str to color'''
        return {'black': cls.black,
                'red': cls.red,
                'green': cls.green,
                'yellow': cls.yellow,
                'blue': cls.blue,
                'magenta': cls.magenta,
                'cyan': cls.cyan,
                'B': cls.black,
                'R': cls.red
                }[color]

    @classmethod
    def color_text(cls, text, color):
        '''get color_text'''
        return color + str(text) + cls.__end

    @classmethod
    def greenbar(cls):
        '''get green_bar (|)'''
        return cls.color_text('|', cls.green)

    @classmethod
    def greenplus(cls):
        '''get green_plus_symbol (+)'''
        return cls.color_text('+', cls.green)

    @classmethod
    def greenminus(cls):
        '''get green_minus_symbol (-)'''
        return cls.color_text('-', cls.green)


class Show:
    '''class show'''
    green_bar = Color.greenbar()
    green_plus = Color.greenplus()
    green_minus = Color.greenminus()

    def __init__(self, players, tables):
        self.__players = players
        self.__tables = tables

    def __str__(self):
        return self.__show_text()

    def __get_flame_text(self):
        '''get (+--------+---+---+---+ ...)'''

        txt = ''
        txt += self.green_plus + \
            ''.join([self.green_minus]*9) + self.green_plus
        for _ in range(len(self.__players)):
            txt += ''.join([self.green_minus]*4) + self.green_plus
        txt += '\n'
        return txt

    def __get_player_text(self):
        txt = ''

        l = ['       ']
        for player in self.__players:
            l.append(player.name)  # プレイヤーの名前を表に追加

        txt += self.green_bar + ' '
        txt += (' ' + self.green_bar + ' ').join(l)
        txt += ' ' + self.green_bar + '\n'
        return txt

    @staticmethod
    def __get_betcoins_text(coins):
        betcoins = str(coins).zfill(2)
        if int(coins) < 20:
            return Color.color_text(betcoins, Color.black)
        if int(coins) < 40:
            return Color.color_text(betcoins, Color.green)
        if int(coins) < 75:
            return Color.color_text(betcoins, Color.yellow)
        return Color.color_text(betcoins, Color.red)

    def __get_bet_text(self):
        txt = ''

        for table in self.__tables:
            l = [str(table)]  # テーブル名を先頭に追加
            # スペース2マス分のスコア用のlistを追加
            l.extend(['  ' for _ in range(len(self.__players))])

            for i, player in enumerate(self.__players):
                # プレイヤーがbetしている場所なら
                if table.name == player.bet_cell:
                    # listを置き換える
                    l[i+1] = self.__get_betcoins_text(player.betcoins)

            txt += self.green_bar + ' '
            txt += (' ' + self.green_bar + ' ').join(l)
            txt += ' ' + self.green_bar + '\n'

        return txt

    def __show_text(self):
        txt = self.__get_flame_text()
        txt += self.__get_player_text()
        txt += self.__get_flame_text()
        txt += self.__get_bet_text()
        txt += self.__get_flame_text()
        return txt.rstrip()

    def show(self):
        '''show table'''
        print(self.__show_text())


class Cell:
    '''プレイヤーがbetするテーブル'''

    def __init__(self, name, rate,  color):
        self.__name = name  # 名前
        self.__rate = rate  # レート
        self.__color = color  # 色

    def __str__(self):
        return Color.color_text(
            f'{self.__name}(×{self.__rate})', Color.str2color(self.__color)
        )

    @property
    def name(self):
        '''get name'''
        return self.__name

    @property
    def rate(self):
        '''get rate'''
        return self.__rate

    @property
    def color(self):
        '''get color'''
        return self.__color


class _Player:
    '''class player'''

    def __init__(self, name, coins, max_betcoins=99):
        self.__name = name
        self.__coins = coins
        self.__bet_cell = None
        self.__betcoins = 0
        self.__max_betcoins = max_betcoins
        self.__max_cell_number = None
        self.__double_up_coins = None

    def __str__(self):
        self.get_info()

    def reset(self):
        '''reset'''
        self.__bet_cell = None
        self.__betcoins = 0

    @property
    def name(self):
        '''get name'''
        return self.__name

    @property
    def coins(self):
        '''get coin'''
        return self.__coins

    @coins.setter
    def coins(self, coins):
        '''set coin'''
        self.__coins = coins

    @property
    def bet_cell(self):
        '''get bet_number'''
        return self.__bet_cell

    @bet_cell.setter
    def bet_cell(self, bet_cell):
        '''set bet_cell'''
        self.__bet_cell = str(bet_cell)

    @property
    def betcoins(self):
        '''get betcoins'''
        return self.__betcoins

    @betcoins.setter
    def betcoins(self, betcoins):
        '''set betcoins'''
        self.__betcoins = int(betcoins)
        self.__coins -= int(betcoins)

    @property
    def max_betcoins(self):
        '''max_betcoins'''
        return min(self.__coins, self.__max_betcoins)

    @property
    def max_cell(self):
        '''get max_cell_number'''
        return self.__max_cell_number

    @max_cell.setter
    def max_cell(self, number):
        '''set max_cell_number'''
        self.__max_cell_number = number

    @property
    def double_up_coins(self):
        '''get double_up_coins'''
        return self.__double_up_coins

    @double_up_coins.setter
    def double_up_coins(self, coins):
        '''set double_up_coins'''
        self.__double_up_coins = coins

    def get_info(self):
        '''get player_info'''
        return f'{self.__name}は {self.__coins}coin 所持しています'

    def get_betcoins_info(self):
        '''get get_betcoins_info'''
        return f'{self.__name}は {self.__bet_cell}に {self.__betcoins}coin BETしました'


class Human(_Player):
    '''class Human'''

    @staticmethod
    def __question_number(text, *exclusion, min_num=1, max_num=1):
        while True:
            number = input(text)
            if number.isdecimal():  # 数値である
                if min_num <= int(number) <= max_num:  # 範囲に収まっている
                    return number
            elif number in exclusion:  # 除外listに含んでいるなら
                return number

    def __bet(self):
        txt = f'何枚BETしますか? (1~{self.max_betcoins}) :'
        cell = self.__question_number(
            txt, max_num=self.max_betcoins)
        return cell

    def __bet_double_up(self):
        txt = f'何枚BETしますか? (1~{self.max_betcoins},{self.double_up_coins}) :'
        cell = self.__question_number(
            txt, str(self.double_up_coins), max_num=self.max_betcoins)
        return cell

    def bet(self):
        '''bet'''
        if self.max_cell is None:  # 初期のままの状態なら
            raise ValueError()

        if self.double_up_coins is None:
            betcoins = self.__bet()
        else:
            betcoins = self.__bet_double_up()
            self.double_up_coins = None

        self.betcoins = betcoins

        txt = f'どこにBETしますか? (R,B,1~{self.max_cell}) :'
        cell = self.__question_number(
            txt, 'R', 'B', max_num=self.max_cell)

        self.bet_cell = cell


class Computer(_Player):
    '''class Computer'''

    def bet(self):
        '''bet'''
        if self.double_up_coins is not None and randrange(0, 1) == 0:
            betcoins = self.double_up_coins
        else:
            betcoins = randrange(1, self.max_betcoins+1)

        self.betcoins = betcoins

        # cellのlistを生成
        cell_list = CasinoGame.get_cell_name(self.max_cell)
        cell_num = randrange(0, self.max_cell + 2)  # 乱数を取得
        self.bet_cell = cell_list[cell_num]


class CasinoGame:
    '''class Onegame'''

    cell_num = 8

    def __init__(self, players, max_betcoins=99):
        self.__players = players
        self.__tables = []
        self.__hit_cell = None
        self.__max_betcoins = max_betcoins

    @classmethod
    def get_cell_name(cls, number):
        '''get cell_list'''
        return ['R', 'B'] + [str(i+1) for i in range(number)]

    def __create_table(self):
        number = 0.9
        self.__tables.clear()
        self.__tables.append(Cell('R', 2 * number, 'R'))
        self.__tables.append(Cell('B', 2 * number, 'B'))
        for i in range(self.cell_num):
            self.__tables.append(
                Cell(str(i+1), self.cell_num * number, ['R', 'B'][i % 2])
            )

    def __reset__players(self):
        for player in self.__players:
            player.reset()

    def __bet__players(self):
        for player in self.__players:
            player.bet()

    def __set_max_cell(self):
        for player in self.__players:
            player.max_cell = self.cell_num

    def __show_betcoins(self):
        txt = ''
        for player in self.__players:
            txt += player.get_betcoins_info() + '\n'
        print(txt.rstrip())

    def __show_table(self):
        print(Show(self.__players, self.__tables))

    def __show__players(self):
        txt = ''
        for player in self.__players:
            txt += player.get_info() + '\n'
        print(txt.rstrip())

    def __select_hit(self):
        cell_num = randrange(0, self.cell_num + 2)
        self.__hit_cell = self.__tables[cell_num]

    def __check_hit(self):
        table_name = [table.name for table in self.__tables]  # テーブルの名前を取得
        # テーブルの名前の場所を取得(hit cell)
        num = table_name.index(self.__hit_cell.name)
        rate = self.__tables[num].rate  # レートを取得

        red_num = table_name.index('R')
        red_rate = self.__tables[red_num].rate

        black_num = table_name.index('B')
        black_rate = self.__tables[black_num].rate

        l = []
        for player in self.__players:
            if self.__hit_cell.name == player.bet_cell:
                l.append({'player': player, 'rate': rate})
            elif player.bet_cell == self.__hit_cell.color == 'R':
                l.append({'player': player, 'rate': red_rate})
            elif player.bet_cell == self.__hit_cell.color == 'B':
                l.append({'player': player, 'rate': black_rate})

        return l

    def __get_hit_coins(self):
        for l in self.__check_hit():
            player = l['player']
            rate = l['rate']
            player.coins += ceil(player.betcoins * rate)

            # 一番左は必要ないが確認する
            if player.coins >= player.betcoins * 2 > self.__max_betcoins:
                player.double_up_coins = player.betcoins * 2

    def __show_hit(self):
        txt = f'あたりは{self.__hit_cell.name}({self.__hit_cell.color})\n'
        for l in self.__check_hit():
            player = l['player']
            rate = l['rate']
            txt += f'{player.name}は {ceil(player.betcoins * rate)}coin GETしました\n'
        print(txt.rstrip())

    def __is_game_over(self):
        for player in self.__players:
            if player.coins <= 0:
                return True
        return False

    def play(self):
        '''play'''
        self.__reset__players()

        self.__create_table()
        self.__set_max_cell()

        while True:
            self.__show__players()
            print()
            self.__show_table()
            print()

            self.__bet__players()
            print()

            self.__show_betcoins()
            print()
            self.__show_table()

            self.__select_hit()
            self.__get_hit_coins()
            self.__show_hit()

            if self.__is_game_over():
                break
            print()
            if input('終了しますか(Y/n) :').lower() in ['y', 'yes']:
                break
            print('\n\n\n\n\n')

        print('最終結果:')
        self.__bet__players()


class Games:
    '''class all_games'''

    def __init__(self):
        self.__players = []
        self.__max_betcoins = 99

    def __create__players(self):
        self.__players.clear()
        self.__players.append(
            Human('MY', 500, max_betcoins=self.__max_betcoins))
        self.__players.append(
            Computer('C1', 500, max_betcoins=self.__max_betcoins))
        self.__players.append(
            Computer('C2', 500, max_betcoins=self.__max_betcoins))
        self.__players.append(
            Computer('C3', 500, max_betcoins=self.__max_betcoins))

    def __show__players(self):
        for player in self.__players:
            print(player)

    def play(self):
        '''play'''
        self.__create__players()
        game = CasinoGame(self.__players, max_betcoins=self.__max_betcoins)
        game.play()


if __name__ == '__main__':
    games = Games()
    games.play()
