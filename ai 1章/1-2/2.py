from pandas import DataFrame
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

df = DataFrame(make_blobs(random_state=5)[0])
df.columns = ['x', 'y']

kmeans = KMeans(init='random', n_clusters=2)
kmeans.fit(df)
df['num'] = kmeans.predict(df)

color = ['blue', 'red']
for i in range(2):
    df_eq = df[df.num == i]
    plt.scatter(df_eq.x, df_eq.y, c=color[i], label=f'duster{i}')

plt.legend(loc='upper right')
plt.show()
