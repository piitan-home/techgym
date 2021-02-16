from IPython.core.display import display
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

sc = MinMaxScaler()

x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
sc.fit(x)
display(sc.transform(x))

df = pd.DataFrame(x)
new_df = (df - df.min()) / (df.max() - df.min())
display(new_df)
