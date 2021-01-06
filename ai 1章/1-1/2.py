from IPython.display import display
import numpy as np
import numpy.random as random
import pandas as pd
import matplotlib.pyplot as plt

# k-means法を使うためのインポート
from sklearn.cluster import KMeans
# 分類データセット生成
from sklearn.datasets import make_blobs

X, Y = make_blobs(random_state=5)

kmeans = KMeans(init='random', n_clusters=2)
kmeans.fit(X)

y_pred = kmeans.predict(X)

merge_data = pd.concat(
    [pd.DataFrame(X[:, 0]), pd.DataFrame(X[:, 1]), pd.DataFrame(y_pred)], axis=1)
merge_data.columns = ['X', 'Y', 'cluster']

# クラスタリング結果のグラフ化
df0 = merge_data[merge_data.cluster == 0]
df1 = merge_data[merge_data.cluster == 1]

# グラフのプロット
plt.scatter(df0['X'], df0['Y'], color='blue', label='cluster0')
plt.scatter(df1['X'], df1['Y'], color='red', label='cluster1')

# 凡例
plt.legend(loc='upper right')
plt.show()
