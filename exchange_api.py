"""
Request currency information from multiple APIs
EURO/RON
USD/RON
EURO/USD
"""
from urllib.request import urlopen
import requests

from bs4 import BeautifulSoup
from xml.etree import cElementTree

import json, os
from datetime import datetime
import api_key_list


def get_file():
    # I'm using another module to store my API keys
    url = f'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml?{api_key_list.ecb_key}'

    # If the file does not exist
    if not os.path.isfile('euro_exchange.xml'):
        source = requests.get(url)
        f = open('euro_exchange.xml', 'w')
        f.write(source.text)
        f.close()

    # If the file is older than 1 day will download again and overwrite
    mod_time_stamp = os.stat('euro_exchange.xml').st_mtime
    mod_time = datetime.fromtimestamp(mod_time_stamp)
    if (datetime.now() - mod_time).days >= 1:
        source = requests.get(url)
        f = open('euro_exchange.xml', 'w')
        f.write(source.text)
        f.close()


def euro_ron():
    # Extract info from xml file

    get_file()
    with open('euro_exchange.xml') as f:
        source = f.read()
        soup = BeautifulSoup(source, 'lxml')

        cube = soup.find('cube')
        name = cube.find('cube', currency='RON')
        print(f"EURO/{name['currency']}: {round(float(name['rate']), 5)}")


def usd_ron():
    # Extract info from json (API request)

    url = 'https://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json'
    source = urlopen(url).read()

    data = json.loads(source)

    for res in data['list']['resources']:
        item = res['resource']['fields']
        if 'RON' in item['name']:
            name = item['name']
            value = round(float(item['price']), 4)
            print(f'{name}: {value}')


def euro_usd():
    # Extract info from xml (API request, kind of)

    url = 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    soup = BeautifulSoup(requests.get(url).text, 'lxml')

    item = soup.find('cube', currency='USD')
    name = item['currency']
    rate = round(float(item['rate']), 5)

    print(f'EURO/{name}: {rate}')


if __name__ == '__main__':
    print(f"{datetime.now().date().strftime('%d %B %Y')} @ {datetime.now().time().strftime('%H:%M:%S')}", end='\n\n')
    euro_ron()
    usd_ron()
    print('-'*16)
    euro_usd()