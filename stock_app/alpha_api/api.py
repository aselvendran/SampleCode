import requests
from typing import Dict


class AlphaVantage:
    def __init__(self, apiKey):
        self.urlPath = f"https://www.alphavantage.co/query?apikey={apiKey}&function="

    def headers(self):
        header = {}
        header['Content-type'] = 'application/json'
        return header

    def getTimeSeries(self, stock_ticker) -> Dict:
        """

        This method retrieves time series data from AlphaVantage based on the stock ticker provided

        :param stock_ticker: any stock traded in the USA market.
        :return: jsonn output containing the high/low/volume/close of the stock price with the earliest day 11-1999.
        """

        try:
            response = requests.get(url="%sTIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full" % (self.urlPath, stock_ticker),
                                    headers=self.headers())

            # EVERY RESPONSE IS A 200. Therefore a value error is necessary to account for bad requests made to the api
            # (bad ticker symbol)

            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        response_json = response.json()
        try:
            time_series_output = response_json['Time Series (Daily)']
        except:
            raise ValueError(response_json['Error Message'])

        return time_series_output

