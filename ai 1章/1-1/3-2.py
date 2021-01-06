from typing import Any, Tuple
from math import sqrt, ceil
from numpy.core.fromnumeric import sort

# from IPython.display import display
# import numpy as np
# import numpy.random as random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


class PltBase:
    def __init__(self, size: int) -> None:
        self.size = size
        self.fig: Figure = plt.figure()
        self.num = 1

    @property
    def sqrt_size(self):
        return ceil(sqrt(self.size))

    def ax(self):
        d = self.fig.add_subplot(self.sqrt_size, self.sqrt_size, self.num)
        self.num += 1
        return d


class Analysis:
    def __init__(self) -> None:
        self.draw_size = 2
        self.plt = PltBase(self.draw_size)

    @staticmethod
    def mkKMeans(fit_data: Any, init: str = 'random', n_clusters: int = 2) -> KMeans:
        return KMeans(init=init, n_clusters=n_clusters).fit(fit_data)

    def get_score(self, data: Any, n_trials: int = 10) -> Tuple[int, int]:
        score = []
        number = list(range(2, 2+n_trials))
        for i in number:
            score.append(self.mkKMeans(data, n_clusters=i).inertia_)
        sort = sorted(zip(score, number))
        return (sort[0][0], sort[0][1])

    def draw(self, title: str, data: Any, n_clusters: int) -> None:
        ax = self.plt.ax()
        y_pred = self.mkKMeans(data, n_clusters=n_clusters).predict(data)

        # x,y座標を結合
        merge_data = pd.concat(
            [pd.DataFrame(data[:, 0]), pd.DataFrame(data[:, 1]), pd.DataFrame(y_pred)], axis=1)
        merge_data.columns = ['X', 'Y', 'cluster']

        df0 = merge_data[merge_data.cluster == 0]
        df1 = merge_data[merge_data.cluster == 1]
        ax.scatter(df0['X'], df0['Y'], color='blue', label='cluster0')
        ax.scatter(df1['X'], df1['Y'], color='red', label='cluster1')
        # ax.legend(loc='upper right')

    def analysis(self):
        data = []
        number = (1, 5, 10, 15, 20, 25)
        for num in number:
            data.append(self.get_score(make_blobs(random_state=num)[0], 10))
        score, cluster = zip(*data)
        sort = sorted(zip(score, number, cluster))

        for i in range(self.draw_size):
            self.draw(str(sort[i][1]), make_blobs(
                random_state=sort[i][1])[0], sort[i][2])


if __name__ == "__main__":
    a = Analysis()
    a.analysis()
    plt.tight_layout()
    plt.show()
