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
    return jsonify(constants.TICKERS)

@app.route('/returns/<string:ticker>/<string:start_date>/<string:end_date>', methods=['GET'])
def get_ticker(ticker, start_date, end_date):
    start_date = validate_date(start_date)
    end_date = validate_date(end_date)
    print(f'Getting returns for ticker for {start_date} to {end_date}')

    df = query_db("SELECT * FROM prices WHERE Date >= ? AND Date <= ?", (start_date, end_date))
    df = df[['Date', ticker]]
    print(df)
    return df.to_json()
    # return jsonify({"error": "Item not found"}), 404



if __name__ == '__main__':
    app.run(debug=True)
