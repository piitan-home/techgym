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

# 説明変数
X = wine.loc[:, ['Alcohol']].values

# 目的変数
Y = wine['Color_intensity'].values

# 予測モデルを計算、ここでa,bを算出
REG.fit(X, Y)

# 回帰係数
display('回帰係数:', REG.coef_)
# 切片
display('切片:', REG.intercept_)

# 先ほどと同じ散布図
plt.scatter(X, Y)
plt.xlabel('Alcohol')
plt.ylabel('Color_intensity')

# その上に線形回帰直線を引く
plt.plot(X, REG.predict(X))
plt.grid(True)

# 決定係数
print('決定係数:', REG.score(X, Y))

plt.show()