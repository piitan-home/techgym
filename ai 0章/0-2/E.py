from _import_ import np, plt, random

init_seed = 0
hist_bin = 40
N = 100000

random.seed(init_seed)

plt.figure(figsize=(20, 6))

rand_data = np.random.randn(N)
data = rand_data * 10 + 50

plt.hist(data, bins=hist_bin, range=(0, 90))

plt.show()