import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from datetime import datetime, timedelta

# Load the data
ticker = 'AAPL'
start_date = '2000-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')
data = yf.download(ticker, start=start_date, end=end_date)

# Calculate technical indicators
data['SMA_20'] = data['Close'].rolling(window=20).mean()
data['SMA_50'] = data['Close'].rolling(window=50).mean()
data['RSI'] = 100 - (100 / (1 + (data['Close'].diff().where(data['Close'].diff() > 0, 0).rolling(window=14).mean() /
                                  data['Close'].diff().where(data['Close'].diff() < 0, 0).abs().rolling(window=14).mean())))

# Drop NaN values
data.dropna(inplace=True)

# Scale the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data[['Close', 'SMA_20', 'SMA_50', 'RSI']])

# Create a separate scaler for the close prices
close_scaler = MinMaxScaler(feature_range=(0, 1))
scaled_close = close_scaler.fit_transform(data[['Close']])

# Prepare the training and testing data
train_data_len = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_data_len]
test_data = scaled_data[train_data_len - 60:]

# Create the datasets for LSTM
def create_dataset(data, time_step=1):
    X, y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step)])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

time_step = 60
X_train, y_train = create_dataset(train_data, time_step)
X_test, y_test = create_dataset(test_data, time_step)

# Reshape the data for LSTM
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2])
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2])

# Build the improved LSTM model
model = Sequential()
model.add(LSTM(100, return_sequences=True, input_shape=(time_step, X_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(100, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(50))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, batch_size=32, epochs=50)

# Predicting the prices
predictions = model.predict(X_test)
predictions = close_scaler.inverse_transform(predictions)

# Prepare the validation data for plotting
valid = data.iloc[train_data_len:]
valid = valid.iloc[:len(predictions)]  # Ensure valid data length matches predictions
valid['Predictions'] = predictions[:, 0]

# Plot the results
plt.figure(figsize=(12, 6))
plt.title('Improved LSTM Model')
plt.xlabel('Date')
plt.ylabel('Close Price USD')
plt.plot(data['Close'], label='Historical Prices')
plt.plot(valid[['Close', 'Predictions']], label='Predicted Prices')
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.show()

# Save predictions to CSV
valid[['Close', 'Predictions']].to_csv('data/predictions.csv')

# Performance metrics
mse = mean_squared_error(valid['Close'], valid['Predictions'])
rmse = np.sqrt(mse)
mae = mean_absolute_error(valid['Close'], valid['Predictions'])
r2 = r2_score(valid['Close'], valid['Predictions'])

print(f'MSE: {mse}')
print(f'RMSE: {rmse}')
print(f'MAE: {mae}')
print(f'R²: {r2}')

# Save performance metrics to CSV
performance_metrics = pd.DataFrame({
    'MSE': [mse],
    'RMSE': [rmse],
    'MAE': [mae],
    'R2': [r2]
})
performance_metrics.to_csv('data/model_performance.csv', index=False)

# Predict future prices for the next month
future_days = 30
last_60_days = scaled_data[-60:]
predicted_prices = []

for _ in range(future_days):
    X_future = last_60_days[-60:].reshape(1, time_step, X_train.shape[2])
    future_price = model.predict(X_future)
    
    # Create a new array with the same shape as the input features
    future_price_full = np.zeros((1, X_train.shape[2]))
    future_price_full[0, 0] = future_price  # Set the predicted 'Close' value
    future_price_full[0, 1:] = last_60_days[-1, 1:]  # Copy other feature values
    
    predicted_prices.append(future_price[0, 0])
    last_60_days = np.append(last_60_days, future_price_full, axis=0)

# Inverse transform the predicted prices
predicted_prices = close_scaler.inverse_transform(np.array(predicted_prices).reshape(-1, 1))

# Create a dataframe for future predictions
future_dates = [data.index[-1] + timedelta(days=i) for i in range(1, future_days + 1)]
future_df = pd.DataFrame(predicted_prices, index=future_dates, columns=['Predicted_Close'])

# Generate buy/sell signals
current_price = data['Close'].iloc[-1]
buy_threshold = 0.02  # Buy if the predicted price is 2% higher than the current price
sell_threshold = 0.02  # Sell if the predicted price is 2% lower than the current price
future_df['Signal'] = 'Hold'
future_df.loc[future_df['Predicted_Close'] > current_price * (1 + buy_threshold), 'Signal'] = 'Buy'
future_df.loc[future_df['Predicted_Close'] < current_price * (1 - sell_threshold), 'Signal'] = 'Sell'

# Save future predictions and signals to CSV
future_df.to_csv('data/future_predictions.csv')
