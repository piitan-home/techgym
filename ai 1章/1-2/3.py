from typing import Optional
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

kmeans = KMeans(init='random', n_clusters=2)
rand_state = [1, 5, 10, 15, 20, 25]


def get_inertia(rand_state: int) -> int:
    df = DataFrame(make_blobs(random_state=rand_state)[0])
    kmeans.fit(df)
    return kmeans.inertia_


def kmeans_plot(rand_state: int, name: Optional[str] = None):
    df = DataFrame(make_blobs(random_state=rand_state)[0])
    df.columns = ('x', 'y')
    kmeans.fit(df)

    df['num'] = kmeans.predict(df)

    color = ['blue', 'red']
    for i in range(2):
        df_eq = df[df.num == i]
        plt.scatter(df_eq.x, df_eq.y, c=color[i], label=f'duster{i}')

    plt.suptitle(name)
    plt.legend(loc='upper right')
    plt.show()


inertia = [get_inertia(r) for r in rand_state]

sorted_rand_state = [r for i, r in sorted(zip(inertia, rand_state))]

kmeans_plot(sorted_rand_state[0], 'min SSE')

kmeans_plot(sorted_rand_state[-1], 'max SSE')
