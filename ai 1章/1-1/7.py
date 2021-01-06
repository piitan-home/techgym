# pip install openpyxl

import os
import pandas as pd
import urllib.request as req
from urlallow import allow_all_https
from IPython.display import display


allow_all_https(show_warning=False)


def get_csv(file: str = 'Online_Retail.csv'):
    if not os.path.isfile(file):
        print('1分ほどお待ちください')
        url = "http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
        req.urlretrieve(url, "Online_Retail.xlsx")
        trans = pd.read_excel('Online_Retail.xlsx',
                              sheet_name='Online Retail', engine='openpyxl')
        trans.to_csv("./Online_Retail.csv")
    # 購買データの読み込み
    return pd.read_csv('Online_Retail.csv')


trans = get_csv()

trans['cancel_flg'] = trans.InvoiceNo.map(lambda x: str(x)[0])

trans = trans[(trans.cancel_flg == '5') & (trans.CustomerID.notnull())]

# データを表示
print('+++++ 元のデータ +++++')
display(trans)
print()

# StockCodeごとに件数を数え、上位5件を表示
print('+++++ 売れた商品の上位5件 +++++')
display(trans['StockCode'].value_counts().head(5))
print()

print('+++++ 番号`85123A`と`47566`の関係 +++++')
A = set(trans[trans['StockCode'] == '85123A'].InvoiceNo)
B = set(trans[trans['StockCode'] == '47566'].InvoiceNo)
cAll = len(set(trans.InvoiceNo))
cA = len(A)
cB = len(B)
cAB = len(A & B)

print(f'len(85123A):{cA}')
print(f'len(47566):{cB}')
print(f'len(85123A ∩ 47566):{cAB}')
print()

print('+++++ 番号`85123A`と`47566`の信頼度 +++++')
c = cAB / cA
sXY = cAB / cAll
sY = cB / cAll
print(f'C:{c* 100}%')
print(f'S_XY:{sXY *100}%')
print(f'S_Y:{sY *100}%')
print(f'lift:{c / (sY)}')
