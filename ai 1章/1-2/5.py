from typing import Tuple
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

scaler = StandardScaler()
array = np.loadtxt('5.csv', delimiter=',')

array_std = scaler.fit_transform(array)
pearsonr = sp.stats.pearsonr(array_std[:, 0], array_std[:, 1])[0]
print(f'相関係数:{pearsonr}')

pca = PCA()
pca.fit(array_std)
display(f'主成分の固有ベクトル\n{pca.components_}')
display(f'各主成分の分散:{pca.explained_variance_}')
display(f'各主成分が持つ分散の比率:{pca.explained_variance_ratio_}')


def draw_vector(start, goal) -> None:
    plt.gca().annotate('', goal, start,
                       arrowprops={'arrowstyle': '->', 'linewidth': 2, 'shrinkA': 0, 'shrinkB': 0})


plt.scatter(array_std[:, 0], array_std[:, 1])
for length, vector in zip(pca.explained_variance_, pca.components_):
    v = vector * 3 * np.sqrt(length)
    draw_vector(pca.mean_, pca.mean_ + v)

plt.show()
