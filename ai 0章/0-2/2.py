from _import_ import pd, display

# 操作する数
head_num = 3
tail_num = 6

hand = {'性別': ['男性', '男性', '女性', '男性', '女性', '男性', '女性', '女性', '男性', '男性'],
        '年齢': ['30代', '20代', '10代', '10代', '40代', '50代', '40代', '10代', '20代', '10代'],
        '勝ち': [20, 21, 4, 60, 14, 10, 12, 19, 12, 14],
        '負け': [24, 15, 35, 3, 35, 29, 2, 12, 11, 43],
        'あいこ': [15, 40, 34, 29, 14, 4, 22, 17, 12, 10]}

alpha_bet = list('ebadcfghij')

# データフレームの生成
hand_df = pd.DataFrame(hand)

display(hand_df.T)

hand_df.index = alpha_bet

display(hand_df.head(3))

display(hand_df.tail(6).T.head(3).T)
