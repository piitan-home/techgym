import requests as req
from bs4 import BeautifulSoup as beau
import numpy as np

url = 'https://news.yahoo.co.jp/'

response = req.get(url)
soup = beau(response.text, 'lxml')
titles = soup.find_all('li', class_='topicsListItem')

for title in titles:
    print(title.getText())

#-*------------*-
friends = np.array(['アルファ','ベータ','ガンマ'])
for i,friend in enumerate(friends):
    print(f'{i+1}人目 {friend}')
