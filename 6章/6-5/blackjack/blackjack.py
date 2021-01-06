'''black_jack.py'''
import random

from .cards import CardSet, PlayerCard, CardInfo


class Player:
    '''player'''

    def __init__(self, player, choice_pattern):
        self.player = player
        self.cards = PlayerCard()

        self.__choice_pattern = choice_pattern

    @property
    def is_stand(self):
        '''is stand'''
        return self.cards.is_stand

    @property
    def is_bust(self):
        '''is bust'''
        return self.cards.is_bust

    @property
    def is_surrender(self):
        '''is surrender'''
        return self.cards.is_surrender

    def choice_pattern(self, moves):
        '''get choice pattern'''
        choice = list(self.__choice_pattern)
        if moves != 1:
            if 'doubleDown' in choice:
                choice.remove('doubleDown')
        return tuple(choice)

    @property
    def max_betcoins(self):
        '''get max betcoins'''
        return min(self.player.max_betcoins, self.player.coins)

    def cards_info(self):
        '''get cards info'''
        return f'{self.cards.text()}(計:{",".join(map(str, self.cards.total))})'


class Human(Player):
    '''human'''

    @staticmethod
    def get_input_number(text, max_=1, min_=1, error_text='整数を入力してください'):
        '''get number'''
        while True:
            number = input(text)
            try:
                number = int(number)
            except ValueError:
                pass
            else:
                if min_ <= number <= max_:
                    return number
            print(error_text)

    def choice(self, moves):
        '''choice'''
        self.cards.show()
        txt = f'カードは{self.cards_info()}です'
        txt += '\n'
        txt += 'あなたの行動を選択してください'
        print(txt)
        choice_pattern = self.choice_pattern(moves)
        choice_text = ' '.join(
            [f'{choice}:{i+1}' for i, choice in enumerate(choice_pattern)])
        num = self.get_input_number(
            f'{choice_text} (', max_=len(choice_pattern), min_=1)
        return choice_pattern[num-1]

    def bet(self):
        '''bet'''
        num = self.get_input_number(
            f'何枚Betしますか? 10~{self.max_betcoins} (', max_=self.max_betcoins, min_=10)
        self.player.set_betcoins(num)


class Computer(Player):
    '''computer'''

    def choice(self, moves):
        '''choice'''
        number = random.randrange(1)
        return self.choice_pattern(moves)[number]

    def bet(self):
        '''bet'''
        # betしなくていい


class BlackJackRules:
    '''black_jack rules'''
    @classmethod
    def show_rules(cls):
        '''ルール説明'''
        print()
        print('ブラックジャック(テックジムバージョン)の説明を行います')
        print(f'得点を{CardInfo.BLACKJACK_SCORE}(ブラックジャック)にできるだけ近づけるゲームです')
        print('2人プレイで遊びます(自分とコンピューター)')
        number = [f"{CardInfo.NAME[i]}:{num}" for i,
                  num in enumerate(CardInfo.NUMBER)]
        print(f'得点は{" ".join(number)} です(Aは好きな方を選択できる)')
        print('カードの得点の合計が最終得点となります')
        print(f'カードの得点が{CardInfo.BLACKJACK_SCORE}を超えた時点で負けとなります(バスト)')
        print()
        print('まず、自分、コンピューター双方に2枚ずつカードが配られます')
        print('次に自分、相手ともにヒット、スタンドなどの選択を')
        print('(誰か一人が)ブラックジャック、バスト、(または全員が)スタンドするまで行い続けます')
        print()
        print('選択の内容(wikipediaから引用)')
        print('  ヒット:カードをもう一枚引く')
        print('  スタンド:カードを引かずにその時点の点数で勝負する')
        print('  ダブルダウン:プレイヤーは最初の2枚のカードを見てから')
        print('      ベットを2倍にしてもう1枚だけカードを引く')
        print('  サレンダー:プレイヤーの手が悪く、勝ち目がないと判断した場合に')
        print('      賭け金の半額を放棄してプレイを降りる')
        print('')
        print('2人とも同じ点数、同じ状態（バストなど）なら引き分けとなります')
        print('2人が同じ点数ではない場合、カードの得点が高い方が勝ちとなります')
        print()
        input('以上で説明は終了となります エンターを押してゲームを開始してください')
        print()


class BlackJack:
    '''black_jack'''

    CHOICE_PATTERN = ('hit', 'stand', 'doubleDown', 'surrender')

    def __init__(self, *players: Player):
        self.card_set = CardSet()
        self.human = Human(players[0], self.CHOICE_PATTERN)
        self.computer = Computer(players[1], self.CHOICE_PATTERN)
        self.moves = 0

    def deal_cards(self, player: Player, card_num=1):
        '''deal cards'''
        cards = []
        for _ in range(card_num):
            cards.append(self.card_set.deal())
        player.cards.add(*cards)

    @property
    def is_gameover(self) -> bool:
        '''return is_gameover'''
        if self.human.is_bust or self.computer.is_bust:
            return True
        if self.human.is_surrender or self.computer.is_surrender:
            return True
        return self.human.is_stand and self.computer.is_stand

    def choice(self, player: Player):
        '''choice'''
        if not player.cards.is_stand:
            pattern = player.choice(self.moves)
            if pattern == 'hit':
                self.deal_cards(player)
            elif pattern == 'stand':
                player.cards.set_stand()
            elif pattern == 'doubleDown':
                player.player.set_betcoins(2, mode='mag')
                self.deal_cards(player)
                player.cards.set_stand()
            elif pattern == 'surrender':
                player.cards.set_surrender()

    @staticmethod
    def bet(player: Player):
        '''bet'''
        player.bet()

    def refund(self):
        '''勝者にコインを払い戻します'''
        human, computer = (self.human.cards.score, self.computer.cards.score)
        if human > computer:
            self.human.player.refund(2)
        elif human == computer:
            self.human.player.refund(1)
        elif human < computer:
            self.human.player.refund(0)

    def show_win_player(self):
        '''show win player'''
        human, computer = (self.human.cards.score, self.computer.cards.score)
        if human > computer:
            print('あなたの勝ちです')
        elif human == computer:
            print('引き分けです')
        elif human < computer:
            print('あなたの負けです')
        self.human.cards.show()
        print(f'あなたのカードは{self.human.cards_info()}です')
        self.computer.cards.show()
        print(f'コンピューターのカードは{self.computer.cards_info()}です')

    def play(self):
        '''play'''
        if input('説明を聞きますか? Y/n :').lower() in ['y', 'yes']:
            BlackJackRules.show_rules()
        print('ブラックジャックスタート！\n')
        print(f'現在の持ちコインは{self.human.player.coins}Coinです')
        self.card_set.reset()
        self.moves = 0

        self.deal_cards(self.human, 2)
        self.deal_cards(self.computer, 2)

        self.bet(self.human)
        self.bet(self.computer)
        while True:
            self.moves += 1
            self.choice(self.human)
            self.choice(self.computer)
            print()
            if self.is_gameover:
                break

        self.refund()
        self.show_win_player()
