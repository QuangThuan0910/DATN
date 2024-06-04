import pandas as pd
import numpy as np
import yfinance as yf
from keras.models import load_model
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from googletrans import Translator


def load_stock_data(stock, start, end):
    """Load historical stock data."""
    return yf.download(stock, start, end)


def prepare_data(data, days=60):
    """Prepare data for prediction."""
    new_df = data.filter(['Adj Close'])
    last_60days = new_df[-days:].values

    scaler = MinMaxScaler(feature_range=(0, 1))
    last_60days_sc = scaler.fit_transform(last_60days)

    return new_df, last_60days_sc, scaler


def predict_future_days(model, scaler, last_60days_sc, days_to_predict=7):
    """Predict future stock prices."""
    future_predictions = []
    current_input = last_60days_sc.copy()  # Copy last 60 days data

    for _ in range(days_to_predict):
        # Prepare data for prediction
        X_test = []
        X_test.append(current_input)
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        # Predict price
        pred_price = model.predict(X_test)
        pred_price_inverse = scaler.inverse_transform(pred_price)  # Inverse transform to original values
        future_predictions.append(pred_price_inverse[0][0])

        # Update input for next prediction
        new_input = np.append(current_input[1:],
                              pred_price)  # Add predicted price to the data sequence, remove the first value
        current_input = new_input.reshape(-1, 1)

    return future_predictions


def plot_predictions(original_data, predicted_data, stock):
    """Plot original and predicted stock prices."""
    last_date = original_data.index[-1]
    predicted_dates = pd.date_range(last_date, periods=len(predicted_data) + 2, inclusive='right')
    predicted_df = pd.DataFrame(predicted_data, index=predicted_dates[1:], columns=['Adj Close'])

    combined_df = pd.concat([original_data, predicted_df])

    plt.figure(figsize=(14, 7))
    plt.plot(combined_df.index, combined_df['Adj Close'], label='Original Adj Close Price', color='blue')
    plt.plot(predicted_df.index, predicted_df['Adj Close'], label='Predicted Adj Close Price', color='red')
    plt.title(f'Historical and Predicted Adj Close Prices for {stock}')
    plt.xlabel('Date')
    plt.ylabel('Adj Close Price (VND)')
    plt.legend()
    plt.show()


def main():
    stock = input("Enter the Stock ID: ")
    end = datetime.now()
    start = datetime(end.year - 20, end.month, end.day)

    # Load stock data
    stock_data = load_stock_data(stock, start, end)

    # Load the model
    model = load_model('Latest_stock_price_model.h5')

    # Prepare the data
    new_df, last_60days_sc, scaler = prepare_data(stock_data)

    # Predict future prices
    predicted_prices = predict_future_days(model, scaler, last_60days_sc, days_to_predict=7)
    print("Predicted Adj Close Prices for the next 7 days: ", predicted_prices)

    # Plot the results
    plot_predictions(new_df, predicted_prices, stock)


if __name__ == "__main__":
    main()
