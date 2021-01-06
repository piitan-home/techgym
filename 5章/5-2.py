import requests as req
from bs4 import BeautifulSoup as beau

def nikkei_225():
    url = 'https://stocks.finance.yahoo.co.jp/stocks/history/?code=998407.O'

    res = req.get(url)
    soup = beau(res.text,'lxml')
    data = soup.find_all('table',class_ = 'boardFin yjSt marB6')[0]

    name_plate = data.find_all('th')
    name_plate = [i.string for i in name_plate]

    data_all = data.find_all('td')
    data_all = [i.string for i in data_all]

    text = '直近1ヶ月の日経平均株価一覧\n    '
    for name in name_plate:
        text += name + '      '
    text += '\n'
    for i in range(len(data_all)):
        text += f'{data_all[i]}  '
        if (i+1) % len(name_plate) == 0:
            text += '\n'

    print(text.strip())

def yahoo_news():
    url = 'https://news.yahoo.co.jp/topics'

    res = req.get(url)
    soup = beau(res.text,'lxml')
    data = soup.find_all('li',class_ = 'topicsListItem')
    data_all = []
    _ = [data_all.extend(i.find_all('a')) for i in data] #ちょっと、わかりにくい書き方？
    data_all = [i.string for i in data_all if i.string != None] #NoneTypeを除外する
    text = '本日のニュース'
    for data in data_all:
        text += f'\n・{data}'
    print(text)

if __name__ == "__main__":
    nikkei_225()
    print()
    yahoo_news()