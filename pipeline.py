import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import constants

# Function to fetch stock data
def fetch_stock_prices(tickers: list, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches historical stock data for a given tickers and date range.
    """
    print(f"Fetching data for {tickers} from {start_date} to {end_date}...")
    stock_data = yf.download(tickers, start=start_date, end=end_date)
    # stock_data.reset_index(inplace=True)  # Reset index to make 'Date' a column
    # stock_data['Ticker'] = ticker  # Add the ticker symbol as a column
    return stock_data

# Function to store data in the database
def store_data(df: pd.DataFrame, table_name: str = "prices"):
    """
    Stores a DataFrame into the database.
    """
    print(f"Storing data into {table_name}...")
    engine = create_engine(constants.DATABASE_URL)
    with engine.connect() as connection:
        df.to_sql(table_name, connection, if_exists='append', index=False)
    print("Data stored successfully.")

# Main pipeline function
def stock_data_pipeline(tickers: list, start_date: str, end_date: str):
    """
    Pipeline to fetch, transform, and store stock data for a list of tickers.
    """
    # Step 1: Fetch data
    data = fetch_stock_prices(tickers, start_date, end_date)
    print(data)
    print(data.columns)
    
    # Step 2: Transform data. Filter only closing prices
    data = data[['Close']]
    data.columns = data.columns.get_level_values(1)
    data.reset_index(inplace=True)  # Reset index to make 'Date' a column
    
    print(data)
    print(data.columns)

    # Step 3: Store data in database
    store_data(data)


if __name__ == "__main__":
    # Run the pipeline
    stock_data_pipeline(constants.TICKERS, constants.START_DATE, constants.END_DATE)
