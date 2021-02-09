from IPython.display import display
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer


def get_info(data: pd.Series) -> pd.Series:
    info = pd.Series(dtype=object)
    info.name = f'{data.name} infomation'
    info['name'] = data.name
    info['size'] = data.size
    info['max'] = data.max()
    info['min'] = data.min()
    info['mean'] = data.mean()
    info['median'] = data.median()
    info['mode'] = data.mode()[0]
    info['variance'] = data.var()
    info['standard'] = data.std()
    info['describe'] = data.describe()[0]
    return info


cancer = load_breast_cancer()
df = pd.DataFrame(data=cancer['data'], columns=cancer['feature_names'])
display(get_info(df['mean radius']))
display(df['mean radius'].describe())

plt.figure(figsize=(5, 8))
plt.boxplot(df['mean radius'])
plt.grid(True)
plt.show()
