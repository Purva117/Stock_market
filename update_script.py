import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
import io
from base64 import b64encode

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the list of stock options
stock_options = [
    {'label': 'Apple Inc. (AAPL)', 'value': 'AAPL'},
    {'label': 'Microsoft Corporation (MSFT)', 'value': 'MSFT'},
    {'label': 'Tesla Inc. (TSLA)', 'value': 'TSLA'},
    {'label': 'Alphabet Inc. (GOOGL)', 'value': 'GOOGL'},
    {'label': 'Meta Platforms Inc. (META)', 'value': 'META'},
    # Add more stock options here
]

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Financial Market Analysis Dashboard"),
    
    dcc.Dropdown(
        id='stock-dropdown',
        options=stock_options,
        value=stock_options[0]['value'],
        multi=False
    ),
    
    dcc.Graph(id='price-chart'),
    dcc.Graph(id='returns-chart'),
    
    html.Div([
        html.H3("Summary Statistics"),
        html.P(id='avg-price'),
        html.P(id='price-std'),
        html.P(id='avg-returns'),
        html.P(id='returns-std')
    ])
])

# Define callback functions
@app.callback(
    [Output('price-chart', 'figure'),
     Output('returns-chart', 'figure'),
     Output('avg-price', 'children'),
     Output('price-std', 'children'),
     Output('avg-returns', 'children'),
     Output('returns-std', 'children')],
    [Input('stock-dropdown', 'value')]
)
def update_charts(selected_stock):
    # Calculate start and end dates for data fetching
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # Fetch data for the past year

    # Fetch latest stock data
    stock_data = yf.download(selected_stock, start=start_date, end=end_date)

    # Calculate summary statistics
    avg_price = stock_data['Adj Close'].mean()
    price_std = stock_data['Adj Close'].std()
    stock_data['Daily_Return'] = stock_data['Adj Close'].pct_change()
    avg_returns = stock_data['Daily_Return'].mean()
    returns_std = stock_data['Daily_Return'].std()

    # Create price chart
    price_chart = go.Figure()
    price_chart.add_trace(go.Candlestick(
        x=stock_data.index,
        open=stock_data['Open'],
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close'],
        name=f'{selected_stock} Price'
    ))
    price_chart.update_layout(title=f'{selected_stock} Price Chart')

    # Create returns chart
    returns_chart = go.Figure()
    returns_chart.add_trace(go.Scatter(
        x=stock_data.index,
        y=stock_data['Daily_Return'],
        mode='lines',
        name=f'{selected_stock} Daily Returns',
        line=dict(color='blue')
    ))

    # Calculate 50-day and 200-day moving averages
    stock_data['50_MA'] = stock_data['Adj Close'].rolling(window=50).mean()
    stock_data['200_MA'] = stock_data['Adj Close'].rolling(window=200).mean()
    
    # Create buy and sell signals based on moving average crossover
    stock_data['Buy_Signal'] = 0
    stock_data['Sell_Signal'] = 0
    stock_data.loc[stock_data['50_MA'] > stock_data['200_MA'], 'Buy_Signal'] = 1
    stock_data.loc[stock_data['50_MA'] < stock_data['200_MA'], 'Sell_Signal'] = -1
    
    # Generate updated HTML chart
    updated_chart = go.Figure()
    updated_chart.add_trace(go.Candlestick(
        x=stock_data.index,
        open=stock_data['Open'],
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close'],
        name=f'{selected_stock} Price'
    ))
    updated_chart.add_trace(go.Scatter(
        x=stock_data.index,
        y=stock_data['50_MA'],
        mode='lines',
        name='50-day MA',
        line=dict(color='orange')
    ))
    updated_chart.add_trace(go.Scatter(
        x=stock_data.index,
        y=stock_data['200_MA'],
        mode='lines',
        name='200-day MA',
        line=dict(color='purple')
    ))
    updated_chart.add_trace(go.Scatter(
        x=stock_data[stock_data['Buy_Signal'] == 1].index,
        y=stock_data[stock_data['Buy_Signal'] == 1]['50_MA'],
        mode='markers',
        name='Buy Signal',
        marker=dict(color='green', size=8, symbol='triangle-up')
    ))
    updated_chart.add_trace(go.Scatter(
        x=stock_data[stock_data['Sell_Signal'] == -1].index,
        y=stock_data[stock_data['Sell_Signal'] == -1]['50_MA'],
        mode='markers',
        name='Sell Signal',
        marker=dict(color='red', size=8, symbol='triangle-down')
    ))
    updated_chart.update_layout(title=f'{selected_stock} Price Chart with Buy/Sell Signals')

    # Encode and save the updated HTML
    buffer = io.StringIO()
    updated_chart.write_html(buffer)
    encoded_html_bytes = buffer.getvalue().encode()

    with open('index.html', 'wb') as f:
        f.write(encoded_html_bytes)

    avg_price_text = f"Average Price: {avg_price:.2f}"
    price_std_text = f"Price Standard Deviation: {price_std:.2f}"
    avg_returns_text = f"Average Returns: {avg_returns:.4f}"
    returns_std_text = f"Returns Standard Deviation: {returns_std:.4f}"

    return updated_chart, returns_chart, avg_price_text, price_std_text, avg_returns_text, returns_std_text

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)