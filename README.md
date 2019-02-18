
# Zerodha python test

This application does following task

- Downloads the Equity bhavcopy zip file from below link <br>
https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx
- Extract the csv file and then write the records into Redis Database
- Shows first 10 stock entries from redis database
- Search stocks by their name field
- Click <a href="https://myapparjun1321.herokuapp.com/"> Here </a> for demo


<h6> Not complete yet Following works need to be done </h6>
- Need to optimize search functionality
- Need to handle errors- zip, redis, http get
- Need to simplify redis implementation

