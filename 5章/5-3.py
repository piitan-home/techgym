import requests
from bs4 import BeautifulSoup
import numpy as np


class Weather():
    def __init__(self):
        self.url = 'https://weather.yahoo.co.jp/weather/'
        self.url_2 = 'https://weather.yahoo.co.jp/weather/week/'
        self.__today = self.__get_response(self.url)
        self.__week = self.__get_response(self.url_2).find_all('tbody')
        self.__week = BeautifulSoup(
            f'{self.__week[0]}{self.__week[1]}', 'lxml')

    def __get_response(self, url):
        return BeautifulSoup(requests.get(url).text, 'lxml')

    def __get_text(self, inf, tag, name):
        data = inf.find_all(tag, class_=name)
        return [i.text for i in data]

    def __get_alt(self, inf, tag, name):
        data = inf.find_all(tag, class_=name)
        data = [i.find('img') for i in data if i.find('img') != None]
        return [i.get('alt') for i in data if i.get('alt') != None]

    def __todays_weather(self):
        name = self.__get_text(self.__today, '', 'name')
        weather = self.__get_alt(self.__today, '', 'icon')
        high = self.__get_text(self.__today, '', 'high')
        low = self.__get_text(self.__today, '', 'low')
        precip = self.__get_text(self.__today, '', 'precip')
        return {'name': name, 'weather': weather, 'high': high, 'low': low, 'precip': precip}

    def __weekly_weather(self):
        name = self.__get_text(self.__week, 'a', '')
        weather = self.__get_alt(self.__week, 'td', '')
        return {'name': name, 'weather': weather}

    def show_todays_weather(self):
        data = self.__todays_weather()

    def show_weekly_weather(self):
        data = self.__weekly_weather()


if __name__ == "__main__":
    w = Weather()
    w.show_todays_weather()
    print()
    w.show_weekly_weather()
