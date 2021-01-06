import math
import random

class Team():
    def __init__(self, name, attack, defence):
        self.__name = name
        self.__attack = attack
        self.__defence = defence
        #初期レーディング
        self.__rating = 1500

    def update_attack(self,attack):
        self.__attack = attack

    def update_defence(self,defence):
        self.__defence = defence

    def get_name(self):
        return self.__name

    def get_rating(self):
        return self.__rating

    def update_rating(self,rating):
        self.__rating = rating

    def get_hit_rate(self):
        return random.randint(10,self.__attack)

    def get_out_rate(self):
        return random.randint(10,self.__defence)

class Play():
    def __init__(self,team_list,num_1p,num_2p):
        #team_listを継承
        self.__team_list = team_list
        self.__score_borads_1p = []
        self.__score_borads_2p = []
        self.__num_1p = num_1p
        self.__num_2p = num_2p
        self.__win = 0

    def main(self):
        self.__win = self.__play()
        #self.__show_WDL(self.__win)
        return self.__win

    def __show_WDL(self,win):
        team_l = self.__team_list
        name_1p = team_l[self.__num_1p].get_name()
        name_2p = team_l[self.__num_2p].get_name()
        if win == 0:
            print(name_1p + 'と' + name_2p + 'が戦った結果、前者が勝ちました')
        elif win == 1:
            print(name_1p + 'と' + name_2p + 'が戦った結果、後者が勝ちました')
        else:
            print(name_1p + 'と' + name_2p + 'が戦った結果、引き分けでした')

    def __play(self):
        for _ in range(9):
            self.__score_borads_1p.append(self.__get_play_inning('1p'))
            self.__score_borads_2p.append(self.__get_play_inning('2p'))

        score_1p = sum(self.__score_borads_1p)
        score_2p = sum(self.__score_borads_2p)
        if score_1p > score_2p:
            return 0
        if score_2p > score_1p:
            return 1
        else:
            return 2

    def __get_play_inning(self,type_):
        team_l = self.__team_list
        if type_ == '1p':
            one_inning = team_l[self.__num_1p].get_hit_rate() - team_l[self.__num_2p].get_out_rate()
        else:
            one_inning = team_l[self.__num_2p].get_hit_rate() - team_l[self.__num_1p].get_out_rate()
        one_inning = math.floor(one_inning /10)
        if one_inning < 0:
            return 0
        return one_inning

    def get_WDL_1p(self):
        return self.__win

    def get_WDL_2p(self):
        if self.__win == 0:
            return 1
        elif self.__win == 1:
            return 0
        else:
            return 2

    def get_1p_num(self):
        return self.__num_1p

    def get_2p_num(self):
        return self.__num_2p

class Main():
    def __init__(self):
        self.__team_list = []
        self.__match_information = []
        self.__WDL = []
        self.__sort_num = []

    def main(self):
        self.__create_teams()

        for _ in range(300):
            number_of_teams = len(self.__team_list)
            for i in range(number_of_teams):
                for j in range(number_of_teams -1 -i):
                    self.__one_game(i,i+j+1)

        self.__calculation_WDL()
        self.__sort_rating()
        self.__show_battle_record()

    def __create_teams(self):
        team_l = self.__team_list
        team_l.append(Team('アタッカーズ',80,20))
        team_l.append(Team('ディフェンダーズ',30,70))
        team_l.append(Team('アベレージーズ',50,50))
        team_l.append(Team('超アタッカーズ',90,10))
        team_l.append(Team('超ディフェンダーズ',15,75))

        team_l.append(Team('ディフェンダーズ<調整値>',40,80))
        team_l.append(Team('超ディフェンダーズ<調整値>',10,10000))
        team_l.append(Team('チーム最弱<ネタ>',15,15))
        team_l.append(Team('チーム最強<ネタ>',200,10))

        #self.__team_list.append(Team(~))とすると、長くなってしまうので、team_lとしました
        self.__team_list = team_l

    def __elo_rating(self, num_1p, num_2p, win):
        #強い相手に勝てば勝つほど、レーティングが多くもらえる(=弱い相手に負ければ負けるほど、レーティングが多く取られる)
        team_l = self.__team_list

        #自由に設定できる係数k レーティングがどれだけ変動するか
        k = 32
        k_2 = 2

        rating_1p = team_l[num_1p].get_rating()
        rating_2p = team_l[num_2p].get_rating()

        #勝率計算(ABの場合、AにBが勝つ確率)
        win_AB = 1 / (10 ** ((rating_2p - rating_1p)/400) + 1)
        win_BA = 1 - win_AB

        if win == 0:
            team_l[num_1p].update_rating(rating_1p + k * win_BA)
            team_l[num_2p].update_rating(rating_2p - k * win_BA)

        elif win == 1:
            team_l[num_1p].update_rating(rating_1p - k * win_AB)
            team_l[num_2p].update_rating(rating_2p + k * win_AB)

        #引き分けの場合、通常はレーティングは変動しないが、
        #強いチームが弱いチームと戦って引き分け = 強いチームの実力が足りない
        #として、少しだけ変動させる
        else:
            if rating_1p < rating_2p:
                team_l[num_1p].update_rating(rating_1p + k_2 * win_BA)
                team_l[num_2p].update_rating(rating_2p - k_2 * win_BA)

            elif rating_1p > rating_2p:
                team_l[num_1p].update_rating(rating_1p - k_2 * win_AB)
                team_l[num_2p].update_rating(rating_2p + k_2 * win_AB)
            else:
                pass

    def __one_game(self, num_1p, num_2p):
        play = Play(self.__team_list,num_1p,num_2p)
        win = play.main()
        self.__elo_rating(num_1p,num_2p,win)
        self.__match_information.append(play)

    def __calculation_WDL(self):
        match_l = self.__match_information
        team_l = self.__team_list
        #対戦成績格納用
        self.__WDL = []
        for i in range(len(team_l)):
            #回数[勝ち,負け,引き分け]
            self.__WDL.append([0,0,0])

        for i in range(len(match_l)):
            num_1p = match_l[i].get_1p_num()
            num_2p = match_l[i].get_2p_num()
            self.__WDL[num_1p][match_l[i].get_WDL_1p()] += 1
            self.__WDL[num_2p][match_l[i].get_WDL_2p()] += 1

    def __sort_rating(self):
        rating = []
        for i in range(len(self.__team_list)):
            team_l = self.__team_list[i]
            rating.append([team_l.get_rating(),i])

        rating.sort(reverse = True)
        sort_number = []
        for i in range(len(rating)):
            sort_number.append(rating[i][1])

        self.__sort_num = sort_number

    def __show_battle_record(self):
        for i in range(len(self.__team_list)):
            num = self.__sort_num[i]
            team_l = self.__team_list[num]
            WDL = self.__WDL[num]
            print(team_l.get_name() + '    戦績:' +
            str(WDL[0]) + '勝' + str(WDL[1]) + '負' + str(WDL[2]) + '引    '
            + 'レーティング:' + str(round(team_l.get_rating(),2))
            )

if __name__ == '__main__':
    main = Main()
    main.main()
