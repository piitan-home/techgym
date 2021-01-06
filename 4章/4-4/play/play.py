import random

class Player:
    def __init__(self, name, coin):
        self.__name = str(name)
        self.__coin = int(coin)
        self.__bet_coin = None
    
    def get_max_bet_coin(self):
        return min(99,self.__coin)
    
    def set_bet_coin(self, bet_coin):
        self.__bet_coin = bet_coin
        self.__coin -= bet_coin

    def get_info(self):
        return {'name':self.__name, 'coin':self.__coin, 'bet_coin':self.__bet_coin}

class Human(Player):
    def __init__(self, name, coin):
        super().__init__(name, coin)
    
    def bet(self):
        max_bet_coin = super().get_max_bet_coin()
        while True:
            name = super().get_info()['name']
            print('{}さんは 何枚BETしますか? (1-{}) :'.format(name,str(max_bet_coin)),end='')
            bet_coin = input()
            if bet_coin in [str(i+1) for i in range(max_bet_coin)]:
                break
        super().set_bet_coin(int(bet_coin))

class Computer(Player):
    def __init__(self, name, coin):
        super().__init__(name, coin)
    
    def bet(self):
        max_bet_coin = super().get_max_bet_coin()
        super().set_bet_coin(random.randint(1,max_bet_coin))

class Cell:
    def __init__(self, name, table_length):
        self.name = str(name)
        if name in ['R','B']:
            self.color = {'R':'red','B':'black'}[name]
            self.rate = 2 * 0.8
        else:
            self.color = ['B','R'][int(name)%2]
            self.rate = table_length * 0.8

class OneGame:
    def __init__(self, player_status, table_length, initial_money):
        self.__players = self.__create_players(player_status, initial_money)
        self.__tables = self.__create_tables(int(table_length))

    def __create_players(self, player_status, initial_money):
        players = []
        for player in player_status:
            if player[1] in ['com','computer','bot']:
                temp = Computer(player[0], initial_money)
            elif player[1] in ['human','player']:
                temp = Human(player[0], initial_money)
            players.append(temp)
        return players
    
    def __create_tables(self, length):
        tables = [Cell(i,length) for i in range(length)]
        tables.insert(0,Cell('R',length))
        tables.insert(1,Cell('B',length))
        return tables
    
    def __show_bet_coin(self):
        for player in self.__players:
            info = player.get_info()
            print('{}は {}コイン BETしました'.format(info['name'],str(info['bet_coin'])))

    def __show_players(self):
        for player in self.__players:
            info = player.get_info()
            print(info['name'] + ' : ' + str(info['coin']))
        
    def __show_tables(self):
        pass #ここから <----
    
    def __bet(self):
        for player in self.__players:
            player.bet()

    def play(self):
        self.__show_players()
        self.__bet()
        self.__show_bet_coin()
        self.__show_players()