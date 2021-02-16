import pandas as pd
from IPython.display import display

# 読み込みデータ
pg_data = {'row': ['Python', 'Ruby', 'PHP', 'Java', 'JavaScript']}
df = pd.DataFrame(pg_data)
display(df)

dummies = pd.get_dummies(df)
display(dummies)

df['vector'] = [dummies.iloc[:,i].values for i in range(len(dummies))]
display(df)
