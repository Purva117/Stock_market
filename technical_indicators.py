import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# Function to calculate moving averages
def calculate_moving_averages(data, short_window, long_window):
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    return data

# Function to calculate RSI
def calculate_rsi(data, window):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

# Example usage
ticker = 'AAPL'
start_date = '2000-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')
data = yf.download(ticker, start=start_date, end=end_date)

data = calculate_moving_averages(data, short_window=20, long_window=50)
data = calculate_rsi(data, window=14)

# Plot the indicators
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['Short_MA'], label='20-Day MA')
plt.plot(data['Long_MA'], label='50-Day MA')
plt.title(f'{ticker} Technical Indicators')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Save data to CSV for web visualization
data[['Close', 'Short_MA', 'Long_MA', 'RSI']].to_csv('data/technical_indicators.csv')
