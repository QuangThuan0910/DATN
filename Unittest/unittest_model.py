import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler


# Import the module functions
from pythonProject.testmodel import load_stock_data, prepare_data, predict_future_days, plot_predictions


class TestStockPricePrediction(unittest.TestCase):

    @patch('testmodel.yf.download')
    def test_load_stock_data(self, mock_download):
        # Mock the data returned by yf.download
        data = pd.DataFrame({
            'Adj Close': [100, 101, 102, 103, 104]
        }, index=pd.date_range(start='2020-01-01', periods=5))
        mock_download.return_value = data

        stock = 'AAPL'
        start = datetime(2000, 1, 1)
        end = datetime(2020, 1, 1)
        result = load_stock_data(stock, start, end)

        mock_download.assert_called_once_with(stock, start, end)
        pd.testing.assert_frame_equal(result, data)

    def test_prepare_data(self):
        data = pd.DataFrame({
            'Adj Close': [100, 101, 102, 103, 104, 105]
        }, index=pd.date_range(start='2020-01-01', periods=6))

        new_df, last_60days_sc, scaler = prepare_data(data, days=3)

        expected_last_60days = np.array([[103], [104], [105]])
        np.testing.assert_array_equal(last_60days_sc, scaler.transform(expected_last_60days))
        pd.testing.assert_frame_equal(new_df, data[['Adj Close']])

    @patch('testmodel.load_model')
    def test_predict_future_days(self, mock_load_model):
        # Create a mock model
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([[1.0]])
        mock_load_model.return_value = mock_model

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaler.fit(np.array([[100], [101], [102], [103], [104], [105]]))

        last_60days_sc = scaler.transform(np.array([[103], [104], [105]]))

        predicted_prices = predict_future_days(mock_model, scaler, last_60days_sc, days_to_predict=2)

        expected_predictions = scaler.inverse_transform([[1.0], [1.0]]).flatten().tolist()

        self.assertEqual(predicted_prices, expected_predictions)

    def test_plot_predictions(self):
        data = pd.DataFrame({
            'Adj Close': [100, 101, 102, 103, 104, 105]
        }, index=pd.date_range(start='2020-01-01', periods=6))

        predicted_data = [106, 107]

        try:
            plot_predictions(data, predicted_data, 'AAPL')
        except Exception as e:
            self.fail(f"plot_predictions() raised {type(e).__name__} unexpectedly!")


if __name__ == '__main__':
    unittest.main()
