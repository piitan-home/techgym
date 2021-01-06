from operator import concat
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from IPython.display import display

from setup import allow_all_url, ignore_warnings


allow_all_url()
ignore_warnings()

file_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00468/online_shoppers_intention.csv'
shoppers = pd.read_csv(file_url)

display(shoppers[:5])
print()
print(f'欠損値の個数:{shoppers.isnull().sum().sum()}')
print()

shoppers.dropna(how='all')


s = shoppers[['Administrative_Duration', 'Informational_Duration',
              'ProductRelated_Duration', 'Region', 'SpecialDay']]
kmeans = KMeans(init='random', n_clusters=6, random_state=0)
kmeans.fit(s)
s['cluster_num'] = kmeans.predict(s)
display(s.groupby('cluster_num').size())


bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
bins_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# クラスター番号と、binsの範囲に収めたSpecialDayを結合
ct_sp = pd.concat([s.cluster_num, pd.cut(
    s.SpecialDay, bins, right=False)], axis=1)
# groupbyで集計し、サイズを計算、見やすく加工する
display(ct_sp.groupby(['cluster_num', 'SpecialDay']
                      ).size().unstack().fillna(0))

ct_re = pd.concat([s.cluster_num, pd.cut(
    s.Region, bins_2, right=False)], axis=1)
# groupbyで集計し、サイズを計算、見やすく加工する
display(ct_re.groupby(['cluster_num', 'Region']
                      ).size().unstack().fillna(0))
