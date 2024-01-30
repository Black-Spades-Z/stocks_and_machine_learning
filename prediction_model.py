import json
import pandas as pd
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import yfinance as yf



class Stock_performance:
    def __init__(self):
        self.stock_symbols = ['AAPL', 'MSFT']
        self.stocks = {}
        self.model_accuracy = {}
        self.recommended = {}
        self.models = {}

    def get_data(self, stocks="", from_yf=True, source_data=[]):
        if not stocks:
            stocks = self.stock_symbols
        if from_yf:
            stock_symbols = list(stocks)
            for stock_name in stock_symbols:
                data = yf.download(stock_name, period="48mo")
                if len(data):
                    self.stocks[stock_name] = data
        else:
            self.stocks[stock_name] = source_data

    def feed_model(self):
        for stock_name, stock_data in self.stocks.items():
            print(stock_name)
            df = stock_data[['Close']].reset_index()
            df.columns = ['ds', 'y']

            m = Prophet()
            m.fit(df)

            future = m.make_future_dataframe(periods=365)
            future2 = future.copy()
            future2 = future2[future2['ds'].dt.weekday < 6]
            forecast = m.predict(future2)

            # Perform cross-validation
            df_cv = cross_validation(m, initial='365 days', period='180 days', horizon='365 days')

            # Compute performance metrics
            df_p = performance_metrics(df_cv)

            # Calculate Mean Absolute Percentage Error (MAPE)
            mape = (df_p['mae'] / df['y'].mean()) * 100

            self.model_accuracy[stock_name] = 1 - mape.values[0] / 100

            last_closed = df.tail(100)['y'].values.mean()
            min_avg_expected = min(forecast.tail(100)['yhat'].values.mean(), forecast.tail(100)['trend'].values.mean())
            year_difference = min_avg_expected - last_closed

            self.recommended[stock_name] = year_difference / last_closed * (1 - mape.values[0] / 100) ** 2

            self.models[stock_name] = m

    def plot_model(self):
        sorted_recom = dict(sorted(self.recommended.items(), key=lambda item: item[1], reverse=True))
        response = {}
        index = 0
        for num, (stock_name, eval) in enumerate(sorted_recom.items()):
            item = {}
            print("Recommendation status:", num + 1)
            print("Stock:", stock_name)
            print("Accuracy:", self.model_accuracy[stock_name])
            print("Price:", self.stocks[stock_name]['Close'].tail(1)[0])

            future = self.models[stock_name].make_future_dataframe(periods=365)
            future2 = future.copy()
            future2 = future2[future2['ds'].dt.weekday < 6]
            forecast = self.models[stock_name].predict(future2)
            df = pd.DataFrame(forecast)
            item['stock_name'] = stock_name
            item['accuracy'] =  self.model_accuracy[stock_name]
            item['price'] = self.stocks[stock_name]['Close'].tail(1)[0]
            item['df'] = df.to_json(orient='records')
            index = num + 1
            response[index] = item

        response['length'] = index
        json_response = json.dumps(response, indent=2)
        return json_response



