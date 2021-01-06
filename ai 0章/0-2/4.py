from IPython.core.display import display
from numpy.core.defchararray import index
from _import_ import pd, np

hand = {'性別': ['男性', '男性', '女性', '男性', '女性', '男性', '女性', '女性', '男性', '男性'],
        '年齢': ['30代', '20代', '10代', '10代', '40代', '50代', '40代', '10代', '20代', '10代'],
        '勝ち': [20, 21, 4, 60, 14, 10, 12, 19, 12, 14],
        '負け': [24, 15, 35, 3, 35, 29, 2, 12, 11, 43],
        'あいこ': [15, 40, 34, 29, 14, 4, 22, 17, 12, 10]}
hand_df = pd.DataFrame(hand)

group_gender = hand_df.groupby('性別')
display('average\n', group_gender['勝ち'].mean())
display('min\n', group_gender['勝ち'].min())
display('max\n', group_gender['勝ち'].max())
display(hand_df['勝ち'].sort_values())
hand_df['あいこ'] = np.nan
display(hand_df.isnull().sum())
