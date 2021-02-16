import pandas as pd
from sklearn.feature_extraction import FeatureHasher
from IPython.display import display


h = FeatureHasher(n_features=5)

# 読み込みデータ
columns = ['Python', 'Ruby', 'PHP', 'Java', 'JavaScript']
D = [{"Label": "Python"}, {"Label": "Ruby"}, {"Label": "PHP"},
     {"Label": "Java"}, {"Label": "JavaScript"}]
df_D = pd.DataFrame({'Label': columns})

f_array = h.transform(D).toarray()
df_a = pd.DataFrame(f_array, dtype=int, index=columns)
display(df_a)
