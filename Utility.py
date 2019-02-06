from bs4 import BeautifulSoup
import requests
import zipfile, io
import pandas as pd
import redis
import os


# Parsing the exact Link from the BSE portal
def parse_url():
    url = 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    link = soup.find('a', id='ContentPlaceHolder1_btnhylZip').get('href')
    return link


# Downloading the zip file from link and extracting it
def download_zip_and_extract():
    link = parse_url()
    r = requests.get(link)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()
    file = link[49:57]
    return file


# Redis database connection
def redis_connection():

    try:
        # making  connection to redis database
        r = redis.StrictRedis(os.environ.get("REDIS_URL", 'None'))

    except Exception as e:
        print(e)

    return r


# Storing data to the redis database
def store_data_to_redis():
    data = pd.read_csv(download_zip_and_extract() + '.CSV')
    r = redis_connection()
    r.flushall()

    for index, row in data.iterrows():
        mapping = {'code': row['SC_CODE'], 'name': row['SC_NAME'].strip(), 'open': row['OPEN'], 'high': row['HIGH'],
                   'low': row['LOW'], 'close': row['CLOSE']}
        r.hmset('stock-' + str(index + 1), mapping)
        r.set(row['SC_NAME'].strip(), index + 1)



# Get top 10 stocks
def get_top_10_stocks():
    top_10_stocks = []

    r = redis_connection()

    # Fetching data from redis database

    for i in range(1, 11):
        dict = r.hgetall('stock-'+str(i))
        top_10_stocks.append(dict)

    return top_10_stocks


# Search keys
def search_stocks(name):
    stocks = []
    r = redis_connection()
    stock_keys = r.keys('*' + name + '*')
    for stock_name in stock_keys:
        value = r.get(stock_name)
        dict = r.hgetall('stock-' + value)
        stocks.append(dict)
    return stocks