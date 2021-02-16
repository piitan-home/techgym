import pandas as pd
from IPython.display import display
from sklearn.preprocessing import OneHotEncoder

columns = ['Java', 'JavaScript', 'PHP', 'Python', 'Ruby']
df = pd.DataFrame({'row': columns})

enc = OneHotEncoder()
array_enc = enc.fit_transform(df).toarray()

df_1 = pd.DataFrame(data=array_enc, columns=columns, dtype=int)
display(df_1)
