'''練習用です
handとか個別に変えてなかったw
'''

import numpy as np
import pandas as pd
from IPython.display import display

head_num = 3
tail_num = 6

hand = {'性別': ['男性', '男性', '女性', '男性', '女性', '男性', '女性', '女性', '男性', '男性'],
        '年齢': ['30代', '20代', '10代', '10代', '40代', '50代', '40代', '10代', '20代', '10代'],
        '勝ち': [20, 21, 4, 60, 14, 10, 12, 19, 12, 14],
        '負け': [24, 15, 35, 3, 35, 29, 2, 12, 11, 43],
        'あいこ': [15, 40, 34, 29, 14, 4, 22, 17, 12, 10]}


feature1 = ['gender', 'age', 'win', 'lose', 'draw']
feature2 = ['性別', '年齢', '勝ち', '負け', 'あいこ']
id_ = ['100', '101', '102', '103', '104', '105', '106', '107', '108', '109']
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
hand_df = pd.DataFrame(hand)


def _2():
    # 表示
    display(hand_df)

    # 転置
    display(hand_df.T)

    # indexを変更して先頭三行の表示
    new_index = ['e', 'b', 'a', 'd', 'c', 'f', 'g', 'h', 'i', 'j']
    hand_df2 = pd.DataFrame(hand, index=new_index)

    display(hand_df2.head(head_num))

    # 末尾6行を転置、先頭3行にしてさらに転置する
    display(hand_df2.tail(tail_num).T.head(head_num).T)


def _3():
    display(hand_df['性別'] == '男性')
    display(hand_df[hand_df['性別'] == '男性'])
    new_hand_df = hand_df.drop('年齢', axis=1)
    display(new_hand_df)


def _4():
    display(hand_df.groupby('性別')['勝ち'].mean())
    display(hand_df.groupby('性別')['勝ち'].max())
    display(hand_df.groupby('性別')['勝ち'].min())
    display(hand_df['勝ち'].sort_values())
    hand_df['あいこ'] = np.nan
    display(hand_df)
    display(hand_df.isnull().sum())


def _5():
    display(hand_df)

    # データフレームのコピー
    hand_df2 = hand_df.copy()

    # index,columnsを複数つけ、さらに名前を指定する
    hand_df2.index = [id_, num]
    hand_df2.index.names = ['NUM', '番号']

    hand_df2.columns = [feature1, feature2]
    hand_df2.columns.names = ['feature', '特徴']

    display(hand_df2)

    # index columnsのレベル1を削除する
    hand_df2.columns.droplevel(1)
    hand_df2.index.droplevel(1)

    display(hand_df2['gender'])

    display(hand_df2.drop(['106'], axis=0))

    display(hand_df2.drop(['gender'], axis=1))


def _6():
    hand_df.columns = feature1
    hand_df.columns.names = 'feature'
    hand_df.set_index(id_)
    hand_df2 = hand_df.copy()
    hand_df2.columns = feature2
    hand_df2.columns.names = 'feature'


# _2()
# _3()
# _4()
# _5()
# _6()
