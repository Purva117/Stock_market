import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from datetime import datetime

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

# Create the target variable (1 for buy, 0 for hold, -1 for sell)
data['Signal'] = 0
data.loc[data['Close'] > data['SMA_20'], 'Signal'] = 1
data.loc[data['Close'] < data['SMA_20'], 'Signal'] = -1

# Drop NaN values
data.dropna(inplace=True)

# Prepare the feature and target variables
features = data[['SMA_20', 'SMA_50', 'RSI']]
target = data['Signal']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Evaluate the model
print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))

# Save predictions to CSV for web visualization
predictions_df = pd.DataFrame({'Date': X_test.index, 'Predicted_Signal': predictions})
predictions_df.to_csv('data/buy_sell_signals.csv', index=False)
