from typing import List
from pprint import pprint

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
from pandas.core.frame import DataFrame
import numpy.random as random
import numpy as np
from IPython.display import display

from read_csv import read


def _1() -> None:
    Sample = np.array(read('1.csv'))

    cluster_df = pd.DataFrame(Sample)

    plt.scatter(cluster_df[0], cluster_df[1], color='blue')
    plt.show()


def _2() -> None:
    Sample = np.array(read('1.csv'))

    cluster_df = pd.DataFrame(Sample)

    # 初期化
    kmeans = KMeans(init='random', n_clusters=3)

    # 重心を計算
    kmeans.fit(cluster_df)

    # 番号を計算
    y_pred = kmeans.predict(cluster_df)

    cluster_df['2'] = y_pred

    cluster_df.columns = ['X', 'Y', 'cluster']


def _3_2(cluster_df: DataFrame, number: int) -> DataFrame:
    return cluster_df[cluster_df.cluster == number]


def _3_3(df: DataFrame, color: str, label: str) -> None:
    plt.scatter(df['X'], df['Y'], color=color, label=label)


def _3() -> None:
    Sample = np.array(read('1.csv'))

    cluster_df = pd.DataFrame(Sample)

    # 初期化
    kmeans = KMeans(init='random', n_clusters=3)

    # 重心を計算
    kmeans.fit(cluster_df)

    # 番号を計算
    y_pred = kmeans.predict(cluster_df)

    cluster_df['2'] = y_pred

    cluster_df.columns = ['X', 'Y', 'cluster']

    df_0, df_1, df_2 = (
        _3_2(cluster_df, 0), _3_2(cluster_df, 1), _3_2(cluster_df, 2))

    _3_3(df_0, 'blue', 'df_0')
    _3_3(df_1, 'red', 'df_1')
    _3_3(df_2, 'green', 'df_2')
    plt.legend(loc='upper left')
    plt.show()


_1()
_2()
_3()
