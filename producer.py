import alpha_vantage.timeseries as ts
import pandas as pd
import numpy as np
from datetime import datetime
from keys import alpha_vantage_api_key

class StockProducer:
    def __init__(self, alpha_vantage_api_key):
        self.api_key = alpha_vantage_api_key
        self.ts = ts.TimeSeries(key=self.api_key, output_format='pandas')

    def get_stock_data(self, symbol, interval='1min'):
        data, meta_data = self.ts.get_intraday(symbol=symbol, outputsize='full')
        return data    

    def get_latest_price(self, symbol):
        data = self.get_stock_data(symbol)
        if not data.empty:
            latest_price = data['1. open'].iloc[0]
            return float(latest_price)
        else:
            raise ValueError("No data available for the given symbol.")
    
    import numpy as np

    def get_historical_volatility(data, window=30):
        data = data['4. close'].astype(float)
        returns = np.log(data / data.shift(1)).dropna()
        volatility = returns.rolling(window=window).std().iloc[-1] * np.sqrt(252)  # annualize
        return volatility

    def calculate_time_to_maturity(maturity_date_str):
        today = datetime.today()
        maturity_date = datetime.strptime(maturity_date_str, '%Y-%m-%d')
        delta = maturity_date - today
        days = delta.total_seconds() / (24 * 60 * 60)  # floating point days
        return days / 365.0


        


apple = StockProducer(alpha_vantage_api_key)
print(apple.get_stock_data('AAPL'))
print(apple.get_latest_price('AAPL'))
print(apple.calculate_time_to_maturity('2025-06-16'))