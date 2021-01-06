'''class combinations'''


class ListCombinations:
    """listでの組み合わせを計算します\n
    (a,b),(c,d) = (a,c),(a,d),(b,c),(b,d)
    (1,2),3 = (1,3),(2,3)\n
    (3,1),(4,1,5) = (3,4),(3,1),(3,5),(1,4),(1,1),(1,5)
    """

    @classmethod
    def to_list(cls, data) -> list:
        '''int, float, str, tuple -> list'''
        if isinstance(data, (int, float, str)):
            return (data,)
        if isinstance(data, tuple):
            return data
        if isinstance(data, list):
            return tuple(data)
        raise TypeError(f'{type(data)} not in (int, float, str, list, tuple)')

    @classmethod
    def combinations(cls, data: tuple) -> tuple:
        '''combinations'''
        combinations = [[]]
        for d in data:
            d_1 = cls.to_list(d)
            new_combinations = []
            for d_2 in d_1:
                new_combinations += [c+[d_2] for c in combinations]
            combinations = new_combinations
        return tuple(combinations)
