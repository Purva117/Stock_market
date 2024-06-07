import yfinance as yf

# Function to get financial ratios
def get_financial_ratios(ticker):
    stock = yf.Ticker(ticker)
    financials = stock.financials
    balance_sheet = stock.balance_sheet

    ratios = {
        'P/E': stock.info['trailingPE'],
        'P/B': stock.info['priceToBook'],
        'ROE': stock.info['returnOnEquity'],
        'Dividend Yield': stock.info['dividendYield']
    }
    return ratios

# Example usage
ticker = 'AAPL'
ratios = get_financial_ratios(ticker)
print(ratios)

# Save data to CSV for web visualization
import csv

with open('data/financial_ratios.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['Ratio', 'Value'])
    for key, value in ratios.items():
        writer.writerow([key, value])
