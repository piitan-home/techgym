'''play casino games'''
from player import PlayerBase
from blackjack import BlackJack


class CasinoGames:
    '''casino games'''

    def __init__(self):
        self.players = []

    def create_players(self):
        '''create players'''
        self.players.clear()
        self.players.append(PlayerBase('human', 500, {}))
        self.players.append(PlayerBase('computer', 500, {}))

    def blackjack(self):
        '''play blackjack'''
        blackjack = BlackJack(*self.players)
        blackjack.play()

    def is_gameover(self):
        '''is gameover'''
        return self.players[0].coins < 10


if __name__ == "__main__":
    games = CasinoGames()
    games.create_players()
    while not games.is_gameover():
        games.blackjack()
        if input('ゲームを終了しますかY/n (').lower() in ['y', 'yes']:
            break
        print()
