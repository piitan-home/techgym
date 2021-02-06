import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.datasets import load_breast_cancer
from plot3D import plot3D

# 乳がんデータの取得
cancer = load_breast_cancer()


plot3D([cancer.data[:, 0], cancer.data[:, 1],
        cancer.data[:, 2]], cancer.feature_names)
plt.show()

# 標準化
sc = StandardScaler()
sc.fit(cancer.data)
X_std = sc.transform(cancer.data)

# 主成分分析
pca = PCA(n_components=2)
pca.fit(X_std)
X_pca = pca.transform(X_std)

# 列にラベルをつける、1つ目が第1主成分、2つ目が第2主成分
X_pca = pd.DataFrame(X_pca, columns=['pc1', 'pc2'])

# 上のデータに、目的変数（cancer.target）を紐づける、横に結合
X_pca['target'] = cancer.target

# 悪性、良性を分ける
pca_malignant = X_pca[X_pca['target'] == 0]
pca_benign = X_pca[X_pca['target'] == 1]

# 悪性、良性をプロット
ax = pca_malignant.plot.scatter(
    x='pc1', y='pc2', color='red', label='malignant')
pca_benign.plot.scatter(x='pc1', y='pc2', color='blue', label='benign', ax=ax)
plt.show()
