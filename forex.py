import requests

urlUSD = 'https://api.exchangerate-api.com/v4/latest/USD'
urlEUR = 'https://api.exchangerate-api.com/v4/latest/EUR'
urlGBP = 'https://api.exchangerate-api.com/v4/latest/GBP'
urlBTC = 'https://blockchain.info/ticker'

# Making our request
response = requests.get(urlUSD)
dataUSD = response.json()['rates']['RUB']

response = requests.get(urlEUR)
dataEUR = response.json()['rates']['RUB']

response = requests.get(urlGBP)
dataGBP = response.json()['rates']['RUB']

response = requests.get(urlBTC)
dataBTC = response.json()['RUB']['last']

data = {'USD': dataUSD, 'EUR': dataEUR, 'GBP':dataGBP, 'BTC': dataBTC}

print(data)