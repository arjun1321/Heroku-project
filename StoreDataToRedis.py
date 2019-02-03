from bs4 import BeautifulSoup
import requests
import zipfile, io
import pandas as pd
import redis

# Parsing the exact Link from the BSE portal

page = requests.get('https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx')
soup = BeautifulSoup(page.content, 'html.parser')
link = soup.find('a', id='ContentPlaceHolder1_btnhylZip').get('href')

# downloading the zip file from link and extracting it

r = requests.get(link)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()

# Redis database credentials

redis_host = "ec2-23-22-9-220.compute-1.amazonaws.com"
redis_port = 7949
redis_password = "p2a3244f8451b8e4c92461fdbc825853de3355dfd0ebdd643a91f443bea0a7fe7"

try:

    # making connection to redis database

    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    # Storing data to the redis database

    for index, row in data.iterrows():
        mapping = {'code': row['SC_CODE'], 'name': row['SC_NAME'], 'open': row['OPEN'], 'high': row['HIGH'],
                   'low': row['LOW'], 'close': row['CLOSE']}
        r.hmset('stock-' + str(index + 1), mapping)
        r.sadd(row['SC_NAME'], index + 1)


except Exception as e:
    print(e)