# yfinance-api

# Setup
```python3 -m venv venv/```
```source venv/bin/activate```
```pip3 install -r requirements.txt```


# To run:
```python3 pipeline.py```
```python3 api.py```

# In another terminal, hit the API endpoints.
Examples:

```{{base_url}}/tickers```
```{{base_url}}/returns/AAPL/2024-09-01/2024-09-10```
```{{base_url}}/returns/2024-12-20/AAPL,VTI,VOO```

# Approach
My approach was to run a pipeline that pulls the data from yfinance,
formats it, and loads the pricing data into the database. This database
can be local as in my source code now, or we can easily change it to any
SQL database. I chose sqlalchemy for easy reading/writing from the database. I also chose Pandas to make it easy to manipulate the data.
I also built a Python Flask REST API that serves the endpoints and calculates
the necessary daily returns using Pandas.

# Challenges
How to store data: I decided to make a shared database between the pipeline and the API, as the pipeline cannot persist data in memory after it stops running. This local database can easily be replaced with a production DB url.
It was hard to calculate returns with some days not being trading days, so I ended up using pct_change to calculate it instead by comparing to previous rows.
I ran into a bug with multiple rows for dates due to running pipeline multiple times. To fix this, I changed the DB write to replace existing DB rows with most updated data instead of appending as a new row in order to make the pipeline idempotent without duplicating rows.

# Assumptions
I assumed that the yfinance package would give me dates in the correct format while writing to DB in the pipeline. I could possibly make it more robust by doing checks and filtering out invalid dates or prices in the pipeline. I did however not assume that the user would send valid requests and handled those accordingly.
I also assumed that the yfinance package would give me a price for each ticker on each date, even though some tickers may be suspended. To make the pipeline more robust, I may have to explicitly handle this.


# Assessment
Overall, the code works. However, the system and code are not as clean or robust as I want it to be. I have several ideas on how to improve the 
system if I had more time. I might change the database schema to have a Ticker
column instead of having one column per ticker, which is not very extensible.
Also, I would want to precompute the returns in the pipeline instead of in the REST api, as those returns do not change. I would then store these returns in the database along with the prices.
That would be easier if I change the schema as above. Precomputing in the pipeline would improve the api call time minorly, although most of the api call runtime is from the database access anyways.
