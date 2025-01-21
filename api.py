import datetime
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
import pandas as pd
import constants

app = Flask(__name__)
engine = create_engine(constants.DATABASE_URL)

def query_db(query: str, params: tuple = ()):
    """
    Executes a query and returns the results as a DataFrame.
    """
    with engine.connect() as connection:
        result = pd.read_sql_query(query, connection, params=params)
    return result

def validate_date(date_str):
    try:
        return datetime.date.fromisoformat(date_str)
    except ValueError:
        return None

@app.route('/tickers', methods=['GET'])
def get_tickers():
    ### 
    # Returns a list of all tickers that the API supports.
    ###
    return jsonify(constants.TICKERS)

@app.route('/returns/<string:ticker>/<string:start_date>/<string:end_date>', methods=['GET'])
def get_ticker_returns_between(ticker, start_date, end_date):
    ### 
    # Returns a time series of the daily returns for the ticker and time horizon.
    ###
    if ticker not in constants.TICKERS:
        return jsonify({"error": f"{ticker} not in valid tickers: {constants.TICKERS}"}), 422
    
    start_date = validate_date(start_date)
    end_date = validate_date(end_date)
    print(f'Getting returns for ticker for {start_date} to {end_date}')

    prev_date = start_date - datetime.timedelta(7)    # query extra rows for return calculation
    next_date = end_date + datetime.timedelta(1)
    df = query_db("SELECT * FROM prices WHERE Date >= ? AND Date < ?", (prev_date, next_date))
    df = df[['Date', ticker]]

    # calculate daily returns
    df['Returns'] = df[ticker].pct_change()

    df = df[['Date', 'Returns']]
    df = df[df['Date'] >= start_date.isoformat()]     # remove extra rows used for return calculation
    print(df)
    return df.to_json()

@app.route('/returns/<string:date>/<string:tickers>', methods=['GET'])
def get_returns_on_date_for(date, tickers):
    ### 
    # Returns a cross-section of daily returns for all requested tickers for a single date.
    ###
    tickers = tickers.split(',')
    for ticker in tickers:
        if ticker not in constants.TICKERS:
            return jsonify({"error": f"{ticker} not in valid tickers: {constants.TICKERS}"}, 422)
    
    date = validate_date(date)
    print(f'Getting returns for {tickers} on {date}')
    
    prev_date = date - datetime.timedelta(7)
    next_date = date + datetime.timedelta(1)
    df = query_db("SELECT * FROM prices WHERE Date < ? AND Date >= ?", (next_date, prev_date))

    prices_df = df[tickers]

    returns_df = prices_df.pct_change()
    returns_df['Date'] = df['Date']
    print(returns_df)

    # return last trading day within a week of date
    return returns_df.iloc[-1].to_json()

if __name__ == '__main__':
    app.run(debug=True)
