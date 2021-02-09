from IPython.core.display import display
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
sc = MinMaxScaler()
sc.fit(x)
display(sc.transform(x))

df = pd.DataFrame(x)
new_df = (df - df.min()) / (df.max() - df.min())
