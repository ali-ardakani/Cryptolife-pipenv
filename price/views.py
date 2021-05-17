from django.shortcuts import render
from bs4 import BeautifulSoup
from django.views.generic import DetailView
from bs4 import BeautifulSoup
import re
import json
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from .models import Cryptocurrency
from django.shortcuts import get_object_or_404


def prices_list(request):

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
    }

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'c1f53ff1-4bdc-4db1-993e-1e7e5994a29c',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    data = data['data']
    name_list = []
    for coin in data:
        name_list.append(coin['name'])

    zip_data = zip(name_list, data)
    dict_data = dict(zip_data)


    return render(request, 'price/prices_list.html', {'dict_data' : dict_data})


def price_detail(requset, slug):
    cryptocurrency = Cryptocurrency.objects.get(slug=slug)
    website = requests.get('https://coinmarketcap.com/currencies/%s/' % slug)
    soup = BeautifulSoup(website.text, 'html.parser')
    price_usd = soup.find('div', {"class":"priceValue___11gHJ"})
    price_usd = price_usd.text
    market_cap = soup.find('div', {"class":"statsValue___2iaoZ"})
    market_cap = market_cap.text
    return render(requset, 'price/price_detail.html', {'price_usd' : price_usd, 'market_cap' : market_cap})



