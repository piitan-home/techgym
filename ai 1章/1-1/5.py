import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn.preprocessing import StandardScaler

from read_csv import read

X = np.array(read('5.csv'))

scaler = StandardScaler()
X_std = scaler.fit_transform(X)

p = sp.stats.pearsonr(X_std[:, 0], X_std[:, 1])[0]
print(f'相関係数{p}:')

plt.scatter(X_std[:, 0], X_std[:, 1], color='blue')
plt.show()
