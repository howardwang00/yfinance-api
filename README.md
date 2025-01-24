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

