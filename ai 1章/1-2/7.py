# pip install openpyxl
from IPython.display import display
import pandas as pd
import urllib.request as req
import os
from setup import allow_all_url

allow_all_url()

path_1 = 'Online Retail.xlsx'
path_2 = 'Online Retail.csv'
if not os.path.isfile(path_2):
    if not os.path.isfile(path_1):
        url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx'
        req.urlretrieve(url, path_1)

    if not os.path.isfile(path_2):
        trans = pd.read_excel(
            path_1, sheet_name='Online Retail', engine='openpyxl')
        trans.to_csv(path_2)
    os.remove(path_1)

trans = pd.read_csv(path_2)

trans['cancel_flg'] = trans['InvoiceNo'].map(lambda x: len(str(x)) == 6)
trans = trans[(trans['cancel_flg']) & (trans['CustomerID'].notnull())]
trans = trans.drop('cancel_flg', axis=1)
display(trans.groupby('StockCode').size().sort_values(ascending=False)[:5])

set_all = set(trans.InvoiceNo)
set_85123A = set(trans[trans["StockCode"] == "85123A"].InvoiceNo)
set_47566 = set(trans[trans["StockCode"] == '47566'].InvoiceNo)
set_85123A_and_47566 = set_85123A & set_47566

print('バスケット数の一覧')
print(f'全ての購買データ: {len(set_all)}')
print(f'85123Aを購入した: {len(set_85123A)}')
print(f'47566を購入した: {len(set_47566)}')
print(f'85123Aかつ47566を購入した: {len(set_85123A_and_47566)}')
print()

print(f'信頼度: {len(set_85123A_and_47566) / len(set_85123A)}')
print(f'支持度: {len(set_85123A_and_47566) / len(set_all)}')
print(f'リフト値: {len(set_85123A_and_47566) * len(set_all) / len(set_85123A) / len(set_47566)}')
#リフト値 = 信頼度A * 信頼度B / 支持度