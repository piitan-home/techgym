import random
import math

teams = []

class Team():
    def __init__(self,name,attack,defence):
        self.name = name
        self.attack = attack
        self.defence = defence

    def info(self):
        print(str(self.name) + ' ( 攻撃力:' + str(self.attack) + ' / 守備力:' + str(self.defence) + ' )')

    def get_hit_rate(self):
        return random.randint(10,self.attack)

    def get_out_rate(self):
        return random.randint(10,self.defence)

def get_play_inning(attacker,defender):
    score = teams[attacker].get_hit_rate() - teams[defender].get_out_rate()
    one_inning_score = math.floor(score/10)
    if one_inning_score < 0:
        one_inning_score = 0
    return one_inning_score

def create_teams():
    global teams
    teams.append(Team('アタッカーズ',80,20))
    teams.append(Team('ディフェンダーズ',30,70))
    teams.append(Team('アベレージーズ',50,50))

def show_teams():
    print('全チームの情報')
    for i in range(len(teams)):
        print('No.' + str(i+1) + ' ', end="")
        teams[i].info()

def choice_team(player):
    #team個数分の数字を生成(0~team-1)
    valid_value = list(range(len(teams)))
    text = ''
    if player == 'myself':
        text = '自分のチームを選択してください'
    elif player == 'enemy':
        text = '相手のチームを選択してください'

    is_valid = False
    while not is_valid:
        # 自分のチームを選択してください(1~3)のように表示し、1を引いて、listの番号と同じにする
        team_num = int(input(text + '(1~' + str(len(teams)) + ') :'))-1
        if team_num in valid_value:
            is_valid = True
        else:
            print('正しい値を入力してください')

    if player == 'myself':
        print('自分のチームは「' + teams[team_num].name + '」です')
    elif player == 'enemy':
        print('相手のチームは「' + teams[team_num].name + '」です')
    return team_num

def play_2(my_team,enemy_team):
    my_score = []
    enemy_score = []
    for i in range(9):
        score = get_play_inning(my_team,enemy_team)
        my_score.append(score)

        score = get_play_inning(enemy_team,my_team)
        #9回裏なら
        if i == 8:
            #9回裏までに決着がついていたら
            if sum(my_score) < sum(enemy_score):
                score = 'X'
            else:
                #9回裏までに決着がついていない状態での最大のスコアの差は4点(引き分けの状態から満塁本塁打)
                if sum(my_score) + 4 < sum(enemy_score) + score:
                    score = 4
        else:
            pass
        enemy_score.append(score)

    return [my_score,enemy_score]

def draw_score(score_borads):
    times = list('123456789R')
    print('＿＿ | ' + ' | '.join(times) + ' |')

    score = score_borads[0]
    #合計をlistに追加
    score.append(sum(score))
    #全てstring型に変換
    score = [str(i) for i in score]
    print('自分 | ' + ' | '.join(score) + ' |')

    score = score_borads[1]
    #9回裏の時点で勝ちが確定していたら
    if score[8] == 'X':
        score[8] = 0
        #合計をlistに追加
        score.append(sum(score))
        score[8] = 'X'
    else:
        #合計をlistに追加
        score.append(sum(score))
    #全てstring型に変換
    score = [str(i) for i in score]
    print('相手 | ' + ' | '.join(score) + ' |')

def play():
    create_teams()
    show_teams()

    my_team = choice_team('myself')
    enemy_team = choice_team('enemy')

    score_borads = play_2(my_team,enemy_team)

    draw_score(score_borads)

if __name__ == '__main__':
    play()
