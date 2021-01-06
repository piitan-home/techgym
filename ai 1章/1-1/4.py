
import pandas as pd
from sklearn.cluster import KMeans
from IPython.display import display
import matplotlib.pyplot as plt

from urlallow import allow_all_https

allow_all_https(show_warning=False)

# データ
file_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00468/online_shoppers_intention.csv'
shoppers = pd.read_csv(file_url)

shoppers_sub = shoppers[
    ['Administrative_Duration', 'Informational_Duration', 'ProductRelated_Duration', 'Region', 'SpecialDay']]
bins = [0, 0.2, 0.4, 0.6, 0.8, 1]


kmeans = KMeans(init='random', n_clusters=6, random_state=0)
kmeans.fit(shoppers_sub)
labels = pd.Series(kmeans.labels_, name='cluster_number')

shoppers_with_cluster = pd.concat([shoppers, labels], axis=1)

qcut_sp = pd.cut(shoppers_with_cluster.SpecialDay, bins, right=False)

# クラスタ番号と年齢層を結合
df = pd.concat([shoppers_with_cluster.cluster_number, qcut_sp], axis=1)

# クラスタ番号と年齢層を軸に集計し、年齢層を列に設定
cross_cluster_sp = df.groupby(
    ['cluster_number', 'SpecialDay']).size().unstack().fillna(0)
display(cross_cluster_sp)

# 分割のための区切りを設定
bins_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 上の区切りをもとに金融機関のデータを分割し、qcut_age変数に各データの年齢層を設定
qcut_r = pd.cut(shoppers_with_cluster.Region, bins_2, right=False)

# クラスタ番号と年齢層を結合
df = pd.concat([shoppers_with_cluster.cluster_number, qcut_r], axis=1)

# クラスタ番号と年齢層を軸に集計し、年齢層を列に設定
cross_cluster_r = df.groupby(
    ['cluster_number', 'Region']).size().unstack().fillna(0)
display(cross_cluster_r)
