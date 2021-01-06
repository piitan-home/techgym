'''野球ゲーム'''

import random

def color_text(text, color):
    '''get color_text'''
    color_base = {'black': '\033[30m', 'red': '\033[31m', 'green': '\033[32m',
                    'yellow': '\033[33m', 'blue': '\033[34m', 'magenta': '\033[35m',
                    'cyan': '\033[36m', 'end': '\033[0m'}
    return color_base[color] + str(text) + color_base['end']


class Rating():
    '''class rating'''
    k = 32

    def __init__(self, rating=1500):
        self._rating = rating
        self._count = 0
        self._win_count = 0
        self._lose_count = 0
        self._draw_count = 0

    def __str__(self):
        txt = ''
        txt += f'rating:{color_text(round(self._rating,2),"red")}　('
        txt += f'win:{color_text(self._win_count,"magenta")}　'
        txt += f'lose:{color_text(self._lose_count,"blue")}　'
        txt += f'draw:{color_text(self._draw_count,"green")}　'
        txt += f'{color_text(round(self._win_count/self._count,2),"yellow")})'
        return txt

    @property
    def rating(self):
        '''get rating'''
        return round(self._rating, 2)

    def _win_1p(self, enemy_rating):
        return 1 / (10 ** ((self._rating - enemy_rating)/400) + 1)

    def win(self, enemy_rating):
        '''win'''
        win_1p = self._win_1p(enemy_rating)
        self._rating += self.k * win_1p
        self._win_count += 1
        self._count += 1

    def lose(self, enemy_rating):
        '''lose'''
        win_1p = self._win_1p(enemy_rating)
        win_2p = 1 - win_1p
        self._rating -= self.k * win_2p
        self._lose_count += 1
        self._count += 1

    def draw(self, enemy_rating):
        '''draw'''
        win_1p = self._win_1p(enemy_rating)
        win_2p = 1 - win_1p
        self._rating += self.k * (win_1p - win_2p) * 0.5
        self._draw_count += 1
        self._count += 1


class Team():
    '''class team'''

    def __init__(self, name, attack, defence, critical):
        self._name = name
        self._attack = attack
        self._defence = defence
        self._critical = critical
        # 初期レーディング
        self._rating = Rating()
        self._hit_rate = None
        self._out_rate = None

    def __str__(self):
        return color_text(self._name,"cyan") + '　' + self._rating.__str__()

    def update_rating(self, win, enemy_rating):
        '''update rating'''
        if win == 'win':
            self._rating.win(enemy_rating)
        elif win == 'lose':
            self._rating.lose(enemy_rating)
        else:
            self._rating.draw(enemy_rating)

    @property
    def name(self):
        '''get name'''
        return self._name

    @property
    def rating(self):
        '''get rating'''
        return self._rating.rating

    def set_rate(self):
        self._hit_rate = random.randint(10, self._attack)
        self._out_rate = random.randint(10, self._defence)
        if self._critical >= random.random()*100:
            self._hit_rate *= 2
            self._out_rate *= 2

    @property
    def hit_rate(self):
        '''get hit_rate'''
        return self._hit_rate

    @property
    def out_rate(self):
        '''get out_rate'''
        return self._out_rate


class OneGame():
    '''class one_game'''

    def __init__(self, player_1, player_2):
        self._1p = player_1
        self._2p = player_2
        self._score_boards = []
        self._number = 0
        self._max_number = 9

    @staticmethod
    def _get_sum(list_):
        '''get sum'''
        sum_l = list_
        while 'X' in sum_l:
            sum_l.remove('X')
        return sum(sum_l)

    def _get_score(self, type_, type_return='sum'):
        if type_ in ['1', '1p']:
            score_l = [i[0] for i in self._score_boards]
        else:
            score_l = [i[1] for i in self._score_boards]
        if type_return == 'sum':
            return self._get_sum(score_l)
        return score_l

    def _get_inning(self, type_):
        if type_ in ['1', '1p']:
            score = self._1p.hit_rate - self._2p.out_rate
        else:
            score = self._2p.hit_rate - self._1p.out_rate
        if score < 0:
            score = 0
        score //= 10  # 切り捨て
        return score

    def _get_winner(self):
        if self._get_score('1p') < self._get_score('2p'):
            return '2p'
        if self._get_score('1p') == self._get_score('2p'):
            return 'draw'
        return '1p'

    def _update_rating(self):
        winner = self._get_winner()
        if winner == '1p':
            self._1p.update_rating('win', self._2p.rating)
            self._2p.update_rating('lose', self._1p.rating)
        elif winner == '2p':
            self._1p.update_rating('lose', self._2p.rating)
            self._2p.update_rating('win', self._1p.rating)
        else:
            self._1p.update_rating('draw', self._2p.rating)
            self._2p.update_rating('draw', self._1p.rating)

    def play(self):
        '''play'''
        for _ in range(8):
            self._number += 1
            self._set_rate()
            self._score_boards.append(
                [self._get_inning('1p'), self._get_inning('2p')])
        while True:
            self._number += 1
            self._set_rate()
            self._score_boards.append([self._get_inning('1p'), 0])
            if self._get_score('1p') < self._get_score('2p'):
                self._score_boards[-1][1] = 'X'
            else:
                self._score_boards[-1][1] = self._get_inning('2p')

            if self._number > self._max_number or self._get_score('1p') != self._get_score('2p'):
                break
        self._update_rating()

    def _set_rate(self):
        self._1p.set_rate()
        self._2p.set_rate()

    def show_winner(self):
        '''show winner'''
        txt = f'{self._1p.name}:{self._get_score("1p")} 対 {self._2p.name}:{self._get_score("2p")} で'
        if self._get_winner() == 'draw':
            txt += '引き分けです'
        elif self._get_winner() == '1p':
            txt += f'{self._1p.name}の勝ちです'
        else:
            txt += f'{self._2p.name}の勝ちです'
        print(txt)

    def show_score(self):
        '''show score'''
        score_1p = self._get_score('1p', 'list')
        score_2p = self._get_score('2p', 'list')
        show_list = []
        # スコアボードの1行目
        show_list.append([''] + list(range(1, self._number+1)) + ['R'])
        show_list.append([self._1p.name] + score_1p + [self._get_score('1p')])
        show_list.append([self._2p.name] + score_2p + [self._get_score('2p')])
        list_length = []
        for i in range(self._number+2):
            list_length.append(
                max([len(str(show_list[j][i])) for j in range(3)]))

        txt = ''
        for i in range(3):
            for j in range(len(show_list[i])):
                txt += str(show_list[i][j]).rjust(list_length[j], ' ') + ' | '
            txt += '\n'
        print(txt.rstrip())


class Main():
    '''class main'''

    def __init__(self):
        self._team = []

    def _match(self, now):
        length = len(self._team)-now-1
        if length == 0:
            return 0
        for i in range(length):
            self._one_game(self._team[now], self._team[i+now+1])
        self._match(now+1)
        return 0

    def main(self):
        '''main'''
        self._create_teams()
        for _ in range(300):
            self._match(0)
        self._show_battle_record()

    def _create_teams(self):
        team_l = self._team
        team_l.append(Team('attackers', 80, 20, 20))
        team_l.append(Team('defenders', 30, 90, 20))
        team_l.append(Team('averages', 60, 60, 20))
        team_l.append(Team('super_attackers', 90, 10, 20))
        team_l.append(Team('super_defenders', 15, 500, 20))
        team_l.append(Team('strongest_team', 100, 10, 50))
        team_l.append(Team('weakest_team', 30, 30, 10))
        self._team = team_l

    @staticmethod
    def _one_game(player_1, player_2):
        one_game = OneGame(player_1, player_2)
        one_game.play()
        # one_game.show_score()
        # one_game.show_winner()
        # print()

    def _show_battle_record(self):
        team_info = list(zip([t.rating for t in self._team],self._team))
        team_info.sort(reverse=True)
        _, team_sort = zip(*team_info)

        for team in team_sort:
            print(team)


if __name__ == '__main__':
    main = Main()
    main.main()
