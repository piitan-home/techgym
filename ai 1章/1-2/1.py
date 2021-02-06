
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# 資料を読み込み
df = pd.read_csv('1.csv', header=None, names=['x', 'y'])

# KMeansを初期化
kmeans = KMeans(init='random', n_clusters=3)
# 重心を計算
kmeans.fit(df)
# 番号を振る
df['num'] = kmeans.predict(df)

color = ['blue', 'red', 'green']
for i in range(3):
    df_eq = df[df.num == i]
    plt.scatter(df_eq.x, df_eq.y, c=color[i], label=color[i])

plt.legend(loc='upper left')
plt.show()
