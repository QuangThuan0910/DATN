import yfinance as yf
from datetime import datetime
import numpy as np
import pandas as pd
from keras.models import load_model
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


def load_stock_data(stock, start, end):
    df = yf.download(stock, start=start, end=end)
    df = df[['Adj Close']]
    return df

def prepare_data(df):
    last_60_days = df[-60:].values
    scaler = MinMaxScaler(feature_range=(0, 1))
    last_60_days_scaled = scaler.fit_transform(last_60_days)
    return df, last_60_days_scaled, scaler

def predict_future_days(model, scaler, last_60_days_scaled, days_to_predict=7):
    future_predictions = []
    current_input = last_60_days_scaled

    for _ in range(days_to_predict):
        prediction = model.predict(current_input.reshape(1, 60, 1))
        pred_price = scaler.inverse_transform(prediction)
        future_predictions.append(pred_price[0][0])
        new_input = np.append(current_input[1:], prediction)
        current_input = new_input.reshape(-1, 1)

    return future_predictions

def plot_predictions(original_data, predicted_data, stock):
    last_date = original_data.index[-1]
    # Đảm bảo phạm vi ngày bao gồm chính xác một ngày bổ sung hơn cần thiết cho chỉ số
    predicted_dates = pd.date_range(last_date, periods=len(predicted_data) + 3, inclusive='right')
    predicted_df = pd.DataFrame(predicted_data, index=predicted_dates[1:], columns=['Adj Close'])
    combined_df = pd.concat([original_data, predicted_df])

    plt.figure(figsize=(14, 7))
    plt.plot(combined_df.index, combined_df['Adj Close'], label='Giá Đóng Cửa Điều Chỉnh Ban Đầu', color='blue')
    plt.plot(predicted_df.index, predicted_df['Adj Close'], label='Giá Đóng Cửa Dự đoán', color='red')
    plt.title(f'Lịch sử và Dự đoán Giá Đóng Cửa Điều Chỉnh cho {stock}')
    plt.xlabel('Ngày')
    plt.ylabel('Giá Đóng Cửa (VND)')
    plt.legend()
    plt.show()

