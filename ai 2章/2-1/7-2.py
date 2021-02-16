import pandas as pd
from pandas.core.frame import DataFrame
import requests
import io
from IPython.display import display


# 自動車価格データの取得
url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data'
res = requests.get(url).content
auto: DataFrame = pd.read_csv(io.StringIO(res.decode('utf-8')), header=None)
auto.columns = ['symboling', 'normalized-losses', 'make', 'fuel-type', 'aspiration', 'num-of-doors',
                'body-style', 'drive-wheels', 'engine-location', 'wheel-base', 'length', 'width', 'height',
                'curb-weight', 'engine-type', 'num-of-cylinders', 'engine-size', 'fuel-system', 'bore',
                'stroke', 'compression-ratio', 'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg', 'price']

label_make = pd.get_dummies(auto[['body-style', 'engine-type']])
display(label_make)
