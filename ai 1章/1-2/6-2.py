import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
from plot3D import plot3D


iris = load_iris()
plot3D([iris.data[:, 0], iris.data[:, 1],
        iris.data[:, 2]], iris.feature_names)
plt.show()

sc = StandardScaler()
pca = PCA(n_components=2)

sc.fit(iris.data)
X_std = sc.transform(iris.data)

pca.fit(iris.data)
X_pca = pca.transform(iris.data)

X_pca = pd.DataFrame(X_pca, columns=['pc1', 'pc2'])

X_pca['target'] = iris.target
pca_a = X_pca[X_pca['target'] == 0]
pca_b = X_pca[X_pca['target'] == 1]

# 悪性、良性をプロット
ax = pca_a.plot.scatter(
    x='pc1', y='pc2', color='red', label='a')
pca_b.plot.scatter(x='pc1', y='pc2', color='blue', label='b', ax=ax)
plt.show()
