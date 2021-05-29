# import json
# from requests import Request, Session
# from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
# from news.models import Category
# from config import settings

# url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# parameters = {
# 'start':'1',
# 'limit':'5000',
# 'convert':'USD'
# }

# headers = {
# 'Accepts': 'application/json',
# 'X-CMC_PRO_API_KEY': 'c1f53ff1-4bdc-4db1-993e-1e7e5994a29c',
# }

# session = Session()
# session.headers.update(headers)

# try:
#     response = session.get(url, params=parameters)
#     data = json.loads(response.text)
# except (ConnectionError, Timeout, TooManyRedirects) as e:
#     print(e)

# data = data['data']

# slugs = []
# for i in data:
#     slugs.append(i['slug'])

# for slug in slugs:
#     queryset = Category(slug=slug)
#     queryset.save()





import requests
from news.models import Category

categories = []
        
url = 'https://api.coingecko.com/api/v3/coins/list'

data = requests.get(url).json()
for coin in data:
    categories.append(coin['name'].lower())

for category in categories:
    queryset = Category(slug=category)
    queryset.save()