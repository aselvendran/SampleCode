from api import *
from formatOutput import *
import configparser
import json


def getApiKey():
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        api_key = config['AlphaVantage']['api_key']
        return api_key
    except:
        return ""


def getStockTimeSeries(stock_ticker, api_key=getApiKey()):
    """

    This methods gets the stock data from the api and then formats the data.

    :param stock_ticker: stock ticker of traded stock in the US market
    :param api_key: Optional api key. Best to put it in the config. file
    :return: formatted json containing month-year of max-high/min-low of stock price.
    """
    alpha_vantage = AlphaVantage(api_key)
    get_stock_data = alpha_vantage.getTimeSeries(stock_ticker)
    stock_data = formatStockOutput(get_stock_data)
    print(json.dumps(stock_data, indent=4))
    return stock_data

