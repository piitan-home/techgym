import numpy as np
from numpy.core.fromnumeric import mean
import pandas as pd
from IPython.display import display
from sklearn.preprocessing import StandardScaler

x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
sc = StandardScaler()
sc.fit(x)
display(sc.transform(x))

df = pd.DataFrame(x)
df_std = (df - df.mean()) / df.std(ddof=False)
