import pandas as pd
from IPython.display import display

# スクレイピングのために読み込み
import urllib
import seaborn as sns
import matplotlib.pyplot as plt

# データをCSVファイルから読み込む
data = "http://archive.ics.uci.edu/ml/machine-learning-databases/balloons/adult+stretch.data"
# urllib.request.urlretrieve(data, './adult+stretch.data')
balloons = pd.read_csv(data)

# データの説明文をダウンロードする
txt = "http://archive.ics.uci.edu/ml/machine-learning-databases/balloons/balloons.names"
# urllib.request.urlretrieve(txt, './balloons.names')

# 説明文の表示(必要であれば表示)
#f = open("./balloons.names","r")
# for line in f:
#    print(line)
# f.close()

# データの個数や型を確認
display(balloons.info())

# 説明文からindexをつける
columns_name = ['color', 'size', 'act', 'age', 'inflated']
balloons.columns = columns_name

# 表示
display(balloons)

display(pd.crosstab(balloons['color'], balloons['size']))


plt.figure(figsize=(10, 10))

# colorのヒストグラムを表示
plt.subplot(2, 2, 1)
sns.countplot(x='color', data=balloons)

# colorカテゴリごとのage件数
plt.subplot(2, 2, 2)
sns.countplot(x='color', hue='age', hue_order=[
              'CHILD', 'ADULT'], data=balloons)

# colorカテゴリごとのsize件数
plt.subplot(2, 2, 3)
sns.countplot(x='color', hue='size', hue_order=[
              'SMALL', 'LARGE'], data=balloons)
plt.show()
