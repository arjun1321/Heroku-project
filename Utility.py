from bs4 import BeautifulSoup
import requests
import zipfile, io
import pandas as pd
import redis


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
    # Redis credential
    redis_host = "ec2-23-22-9-220.compute-1.amazonaws.com"
    redis_port = 7949
    redis_password = "p2a3244f8451b8e4c92461fdbc825853de3355dfd0ebdd643a91f443bea0a7fe7"

    try:
        # making  connection to redis database
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    except Exception as e:
        print(e)

    return r


# Storing data to the redis database
def store_data_to_redis():
    data = pd.read_csv(download_zip_and_extract() + '.CSV')
    r = redis_connection()

    for index, row in data.iterrows():
        mapping = {'code': row['SC_CODE'], 'name': row['SC_NAME'].strip(), 'open': row['OPEN'], 'high': row['HIGH'],
                   'low': row['LOW'], 'close': row['CLOSE']}
        r.hmset('stock-' + str(index + 1), mapping)
        r.sadd(row['SC_NAME'].strip(), index + 1)



# Get top 10 stocks
def get_top_10_stocks():
    top_10_stocks = []

    r = redis_connection()

    # Fetching data from redis database

    for i in range(1, 11):
        dict = r.hgetall('stock-'+str(i))
        top_10_stocks.append(dict)

    return top_10_stocks

