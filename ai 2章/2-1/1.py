import sys
from IPython.display import display
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_breast_cancer

cancer = load_breast_cancer()
df = pd.DataFrame(data=cancer.data, columns=cancer.feature_names)

display(df)
plt.hist(df['mean radius'], bins=16, label='mean radius')  # bins: ヒストグラムの分割数
plt.show()

sns.set_style('whitegrid')
sns.histplot(df['mean radius'], kde=True, bins=16, label='mean radius')
plt.show()

sns.set(style='dark', palette='colorblind', color_codes=True)
sns.histplot(df['mean radius'], kde=True, bins=58, label='mean radius')
plt.show()

plt.rcParams["figure.figsize"] = [16, 16]
df.hist()
plt.show()
