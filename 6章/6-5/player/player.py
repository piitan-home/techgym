'''プレイヤーの元となるクラスです'''


class PlayerBase:
    '''プレイヤーのベースとなるクラスです(将来の拡張用)\n
    '''

    def __init__(self, name: str, coins: int, settings: tuple):
        self.name = name
        self.coins = coins
        self.settings = settings
        self.betcoins = None
        self.max_betcoins = 100

    def set_betcoins(self, coins: int, mode='num'):
        '''set betcoins'''
        if not isinstance(coins, int):
            raise TypeError()
        if mode == 'num':
            self.coins -= coins
            self.betcoins = coins
        elif mode == 'mag':
            self.coins -= self.betcoins * (coins-1)
            self.betcoins *= coins

    def refund(self, mag):
        '''refund'''
        if self.betcoins is None:
            raise TypeError()
        self.coins += self.betcoins * mag
        self.betcoins = None
