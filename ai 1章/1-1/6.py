from typing import Iterable
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 乳がんデータを読み込むためのインポート
from sklearn.datasets import load_breast_cancer

# 乳がんデータの取得
cancer = load_breast_cancer()

# data = pd.DataFrame(cancer.data[:, 0:3])
# data.columns = cancer.feature_names[0:3]
# display(data)


def plot3D(data: Iterable, label: Iterable = ('x', 'y', 'z')):
    fig = plt.figure()
    ax_3d = Axes3D(fig)
    ax_3d.set_xlabel(label[0])
    ax_3d.set_ylabel(label[1])
    ax_3d.set_zlabel(label[2])
    ax_3d.view_init(elev=10., azim=-15)
    ax_3d.plot(
        data[0], data[1], data[2], marker="o", linestyle='None', color='blue')


def std_all(data: Iterable):
    sc = StandardScaler()
    sc.fit(data)
    return (sc, sc.transform(data))


def pca_all(std: StandardScaler, n_components=2):

    pca = PCA(n_components=n_components)
    pca.fit(std)
    return (pca, pca.transform(std))


plot3D([cancer.data[:, 0], cancer.data[:, 1],
        cancer.data[:, 2]], cancer.feature_names)
plt.show()

pca, X_pca = pca_all(std_all(cancer.data)[1])

print(f'X_pca shape:{X_pca.shape}')
print(f'Explained variance ratio:{pca.explained_variance_ratio_}')

# 上のデータに、目的変数（cancer.target）を紐づける、横に結合
new_X_pca = pd.concat(
    [pd.DataFrame(X_pca, columns=['pc1', 'pc2']),
     pd.DataFrame(cancer.target, columns=['target'])], axis=1)

# 悪性、良性を分ける
pca_malignant = new_X_pca[new_X_pca['target'] == 0]
pca_benign = new_X_pca[new_X_pca['target'] == 1]

# 悪性、良性をプロット
ax = pca_malignant.plot.scatter(
    x='pc1', y='pc2', color='red', label='malignant')
pca_benign.plot.scatter(x='pc1', y='pc2', color='blue', label='benign', ax=ax)
plt.show()
