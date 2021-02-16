import pandas as pd
from pandas.core.frame import DataFrame
import requests
import io
from sklearn.preprocessing import LabelEncoder
from IPython.display import display


def counter(num: int) -> int:
    return count[num]


# 自動車価格データの取得
url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data'
res = requests.get(url).content
auto: DataFrame = pd.read_csv(io.StringIO(res.decode('utf-8')), header=None)
auto.columns = ['symboling', 'normalized-losses', 'make', 'fuel-type', 'aspiration', 'num-of-doors',
                'body-style', 'drive-wheels', 'engine-location', 'wheel-base', 'length', 'width', 'height',
                'curb-weight', 'engine-type', 'num-of-cylinders', 'engine-size', 'fuel-system', 'bore',
                'stroke', 'compression-ratio', 'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg', 'price']

enc = LabelEncoder()
label_make = enc.fit_transform(auto['make'])
auto['label_make'] = label_make

count = auto.groupby('make')['label_make'].count()
auto['count_make'] = auto['label_make'].map(counter)

display(auto)
