import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X = make_blobs(random_state=5)[0]
plt.scatter(X[:, 0], X[:, 1])
plt.show()

kmeans = KMeans(n_clusters=2)
kmeans.fit(X)
num = kmeans.predict(X)
for i, c in enumerate(['red', 'blue']):
    tmp = X[num == i]
    plt.scatter(tmp[:, 0], tmp[:, 1], color=c)
plt.show()
