from _import_ import pd, display

feature_1 = ['gender', 'age', 'win', 'lose', 'draw']
hand_1 = {'性別': ['男性', '男性', '女性', '男性', '女性', '男性', '女性', '女性', '男性', '男性'],
          '年齢': ['30代', '20代', '10代', '10代', '40代', '50代', '40代', '10代', '20代', '10代'],
          '勝ち': [20, 21, 4, 60, 14, 10, 12, 19, 12, 14],
          '負け': [24, 15, 35, 3, 35, 29, 2, 12, 11, 43],
          'あいこ': [15, 40, 34, 29, 14, 4, 22, 17, 12, 10]}
id_1 = ['100', '101', '102', '103', '104', '105', '106', '107', '108', '109']

feature_2 = ['address', 'hobby', 'job']
hand_2 = {'住所': ['東京', '大阪', '名古屋', '北海道', '東京', '鹿児島', '大阪', '名古屋', '東京', '大阪'],
          '趣味': ['野球', '賭博', 'じゃんけん', '野球', '賭博', '野球', 'じゃんけん', '賭博', '野球', 'じゃんけん'],
          '仕事': ['IT', '医療', '弁護士', '事務', '事務', '弁護士', 'IT', 'IT', 'IT', '事務']}
id_2 = ['100', '101', '102', '103', '110', '111', '106', '113', '108', '114']


hand_df_1 = pd.DataFrame(hand_1)

hand_df_1.columns = feature_1
hand_df_1.columns.names = ['feature']
hand_df_1['id'] = id_1
hand_df_1.set_index('id', inplace=True)

display(hand_df_1)


hand_df_2 = pd.DataFrame(hand_2)

hand_df_2.columns = feature_2
hand_df_2.columns.names = ['feature']
hand_df_2['id'] = id_2
hand_df_2.set_index('id', inplace=True)

display(hand_df_2)
