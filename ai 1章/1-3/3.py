import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
random_state = [1, 5, 10, 15, 20, 25]
for s in random_state:
    X = make_blobs(random_state=s)[0]
    plt.scatter(X[:, 0], X[:, 1])
    plt.show()
