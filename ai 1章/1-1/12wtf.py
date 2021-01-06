from gensim.models import word2vec
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from urlallow import allow_all_https

allow_all_https(show_warning=False)

# モデルの読み込み
model_path = './words.model'
model = word2vec.Word2Vec.load(model_path)

# 対象の単語
words = []
words.append("老人")
words.append("海")
words.append("ヘミングウェイ")
words.append("魚")
words.append("彼")

vectors = []

for w in words:
    vectors.append(model.wv[w])

# 単語のベクトル表現を2次元に圧縮する
pca = PCA(n_components=2)
pca.fit(vectors)
vectors_pca = pca.transform(vectors)

for w in vectors_pca:
    # 配列形式に整形
    print(np.array2string(w, separator=', ', formatter={
          'float_kind': lambda x: '{: .4f}'.format(x)}))


def name2pca(name: str):
    name = [d[0] for d in model.wv.most_similar(name, topn=100)]
    vec = [model.wv[n] for n in name]
    pca.fit(vec)
    vec_pca = pca.transform(vec)
    return (name, [[x for x, _ in vec_pca], [y for _, y in vec_pca]])


_, vec_pca_1 = name2pca('老人')
plt.scatter(vec_pca_1[0], vec_pca_1[1], c='red')
_, vec_pca_2 = name2pca('海')
plt.scatter(vec_pca_2[0], vec_pca_2[1], c='blue')
plt.show()

kmeans = KMeans(init='random', n_clusters=3, random_state=0)
kmeans.fit(vec_pca_1+vec_pca_2)
pre = kmeans.predict(vec_pca_1+vec_pca_2)
# わからない
