
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv('1.csv')
kmeans = KMeans(init='random', n_clusters=3)
kmeans.fit(df)
df['num'] = kmeans.predict(df)
for i, c in enumerate(['red', 'blue', 'green']):
    tmp = df[df['num'] == i]
    plt.scatter(tmp.x, tmp.y, color=c)
plt.show()
