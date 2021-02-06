import os
from typing import Tuple
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
import numpy as np
from sklearn.decomposition import PCA
from matplotlib.font_manager import FontProperties
import urllib.request as req
from setup import allow_all_url

allow_all_url()

# モデルの読み込み
model = Word2Vec.load('./words.model')

FONTPATH = './Osaka.ttc'
if not os.path.isfile(FONTPATH):
    url = 'https://github.com/hokuto-HIRANO/Word2Vec/raw/master/font/Osaka.ttc'
    req.urlretrieve(url, FONTPATH)

prop = FontProperties(fname=FONTPATH)

# 対象の単語
words = ['老人', '海', 'ヘミングウェイ', '魚', '彼']

vectors = [model.wv[w] for w in words]

# 単語のベクトル表現を2次元に圧縮する
pca = PCA(n_components=2)
pca.fit(vectors)
vectors_pca = pca.transform(vectors)

for w in vectors_pca:
    # 配列形式に整形
    print(np.array2string(w, separator=', ',
                          formatter={'float_kind': lambda x: '{: .4f}'.format(x)}))

for (i, j, k) in zip(vectors_pca[:, 0], vectors_pca[:, 1], words):
    plt.plot(i, j, 'o')
    plt.annotate(k, xy=(i, j), fontproperties=prop)
plt.show()


def draw_most_similar(vectors: Word2Vec, target: str, color: Tuple[str, str], topn: int = 100):
    similars = [w[0] for w in vectors.wv.most_similar(target, topn=topn)]
    similars.insert(0, target)

    colors = [color[0]] + [color[1]] * topn
    pca = PCA(n_components=2)
    X = pca.fit_transform([vectors.wv[w] for w in similars])
    plt.scatter(X[:, 0], X[:, 1], color=colors, s=10)
    for w, x, X, c in zip(similars[:], X[:, 0], X[:, 1], colors):
        plt.annotate(w, xy=(x, X), xytext=(3, 3),
                     textcoords='offset points', fontsize=6, fontproperties=prop, color=c)


draw_most_similar(model, '老人', ('b', 'g'))
draw_most_similar(model, '海', ('r', 'orange'))
plt.show()
