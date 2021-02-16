import pandas as pd
from IPython.display import display
from sklearn.preprocessing import LabelEncoder

columns = ['Java', 'JavaScript', 'PHP', 'Python', 'Ruby']
df = pd.DataFrame({'row': columns})

enc = LabelEncoder()
array_enc = enc.fit_transform(columns)

df['Label'] = array_enc

display(df)
