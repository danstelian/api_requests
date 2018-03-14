"""
Requests two ways:
1. requests + BeautifulSoup
2. urllib + cElementTree

Request weather information from an API, for the city of Brasov
(in this case just the temperature)

Parse the xml file by using either xml.etree.cElementTree.parse() or BeautifulSoup + lxml module
"""
import datetime
import api_key_list
# first way
import requests
from bs4 import BeautifulSoup
# second way
from urllib import request
from xml.etree import cElementTree


def re_plus_soup():
    city = 'Brasov'
    country = 'ro'

    # I'm using another module to store my API keys
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&mode=xml&appid={api_key_list.owm_key}'
    resp = requests.get(url)

    soup = BeautifulSoup(resp.text, 'lxml')

    temp_k = float(soup.temperature['value'])
    temp_c = round(temp_k - 272.15, 1)

    time = datetime.datetime.now().time().strftime('%H:%M:%S')
    print(f'The temperature in Brasov @ {time} is {temp_c} C')


def urllib_plus_etree():
    city = 'Brasov'
    country = 'ro'

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&mode=xml&appid={api_key_list.owm_key}'
    resp = request.urlopen(url)

    tree = cElementTree.parse(resp)

    temp_k = float(tree.find('temperature').attrib['value'])
    temp_c = round(temp_k - 272.15, 1)

    time = datetime.datetime.now().time().strftime('%H:%M:%S')
    print(f'The temperature in Brasov @ {time} is {temp_c} C')


if __name__ == '__main__':
    re_plus_soup()