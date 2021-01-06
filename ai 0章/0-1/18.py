import os
import pandas as pd
import urllib
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display

# 線形単回帰
from sklearn import linear_model

os.chdir(os.path.abspath(__file__ + '/../'))

# データの取得
data = "wine.data"
wine = pd.read_csv(data)


# indexを説明からつける
# アルコール,リンゴ酸,灰,灰分のアルカリ度,マグネシウム,総フェノール,フラバノイド
# 非フラバノイドフェノール,プロアントシアニン,色の濃さ,色相,希釈ワインのOD 280 / OD 315,プロリン
columns_name = ['class', 'Alcohol', 'Malic_acid', 'Ash',
                'Alcalinity_of_ash', 'Magnesium', 'Total_phenols',
                'Flavanoids', 'Nonflavanoid_phenols', 'Proanthocyanins',
                'Color_intensity', 'Hue', 'OD280_OD315', 'Proline']
wine.columns = columns_name

# 線形回帰インスタンス
REG = linear_model.LinearRegression()

# すべての相関係数の表示
display(wine.corr())

# 相関係数のヒートマップを表示
plt.figure(figsize=(8, 8))
sns.heatmap(wine.corr(), vmax=1, vmin=-1, center=0)
plt.savefig('wine_data_heatmap.png')
plt.show()

# 相関係数の並び替え
wine_corr = wine.corr().abs().unstack()
wine_corr_sort = wine_corr.sort_values(ascending=False)
wine_corr_list = pd.DataFrame(wine_corr_sort)

# 総関係数上位を表示　13成分の同一ペアの相関係数が1.0になることに注意
ra_low, ra_hi = 14, 25

display(wine_corr_list.iloc[ra_low:ra_hi])
