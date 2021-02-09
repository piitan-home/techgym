import pandas as pd
import numpy as np
from numpy import random as rd
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn.datasets import load_breast_cancer


def show_info(data: pd.Series):
    display(f'size: {data.size}')
    display(f'count NaN: {data.isnull().sum()}')
    display(f'mean: {data.mean()}')


cancer = load_breast_cancer()
df = pd.DataFrame(data=cancer['data'], columns=cancer['feature_names'])

mean_radius = df['mean radius']
nan_list = rd.randint(0, len(mean_radius), 30)

for nan in nan_list:
    df.iloc[nan, 0] = np.nan

new_df = mean_radius.dropna()
display('リストワイズ後')
show_info(new_df)
display()

new_df = mean_radius.fillna(0)
display('0に置き換え後')
show_info(new_df)
display()

new_df = mean_radius.fillna(method='ffill')
display('前の値に置き換え後')
show_info(new_df)
display()

new_df = mean_radius.fillna(method='bfill')
display('後の値に置き換え後')
show_info(new_df)
display()

new_df = mean_radius.fillna(mean_radius.mean())
display('平均値に置き換え後')
show_info(new_df)
display()


std = mean_radius.std()
mean = mean_radius.mean()
rand = rd.uniform(mean - std / 2, mean + std / 2, mean_radius.isnull().sum())
new_df = mean_radius.copy()
new_df[np.isnan(new_df)] = rand
display('補完値に置き換え後')
show_info(new_df)
display()

new_df = mean_radius.interpolate()
display('線形補完で置き換え後')
show_info(new_df)
display(limit_direction='forward',)
