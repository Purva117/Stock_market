import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# Download historical price data
def download_historical_data(ticker, start, end):
    stock_data = yf.download(ticker, start=start, end=end)
    return stock_data

# Plot historical prices
def plot_historical_prices(stock_data, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['Close'], label='Close Price')
    plt.title(f'{ticker} Historical Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

# Example usage
ticker = 'AAPL'
start_date = '2000-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')

data = download_historical_data(ticker, start_date, end_date)
plot_historical_prices(data, ticker)

# Save data to CSV for web visualization
data.to_csv('data/historical_prices.csv')