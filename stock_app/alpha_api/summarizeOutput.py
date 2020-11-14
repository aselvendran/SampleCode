from alpha_api.api import *
from alpha_api.formatApiOutput  import *
import configparser
import time

def getApiKey():
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        api_key = config['AlphaVantage']['api_key']
        return api_key
    except:
        return ""


def getStockTimeSeries(stock_ticker, api_key='A3U8E3F7N3A85K86'):
    """

    This methods gets the stock data from the api and then formats the data.

    :param stock_ticker: stock ticker of traded stock in the US market
    :param api_key: Optional api key. Best to put it in the config. file
    :return: formatted json containing month-year of max-high/min-low of stock price.
    """
    alpha_vantage = AlphaVantage(api_key)
    get_stock_data = alpha_vantage.getTimeSeries(stock_ticker)
    stock_data = formatStockOutput(get_stock_data)
    return stock_data


def calculateDividend(stock_data, month_year, amount_to_buy, stock_price_limit):
    stock_info = stock_data[month_year]

    if stock_price_limit == "average":
        stock_price = (stock_info['maximum high'] + stock_info['minimum low']) / 2
    else:
        stock_price = stock_info[stock_price_limit]

    amount_of_stocks = amount_to_buy / stock_price

    days_list = [stock_date for stock_date in stock_data.keys() if
                 datetime.strptime(month_year, "%m-%Y") < datetime.strptime(stock_date, "%m-%Y")]

    stocks_val = {}

    print("stock_data",stock_data)

    for day in days_list:
        stocks_val[day] = {"dividends_total": stock_data[day]['dividend amount'] * amount_of_stocks,
                           "value_of_stock": ((stock_data[day]['maximum high'] + stock_data[day][
                               'minimum low']) / 2) * amount_of_stocks
                           }

    return stocks_val


def stockListDividendOutput(stock_dic, amount_of_portfolio, month_of_buy, stock_price_limit):
    dividend_dic = {}

    for stock_ticker in stock_dic.keys():
        amount_to_buy = amount_of_portfolio * (float(stock_dic[stock_ticker].replace("%", ""))) / 100

        stock_data = getStockTimeSeries(stock_ticker)
        time.sleep(11)
        div = calculateDividend(stock_data, month_of_buy, amount_to_buy, stock_price_limit)

        for div_month in div.keys():
            if div_month in dividend_dic:
                dividend_dic[div_month].append(div[div_month])
            else:
                dividend_dic[div_month] = [div[div_month]]

    max_date_of_stocks = max([datetime.strptime(month_year, "%m-%Y") for month_year in dividend_dic]).strftime("%m-%Y")
    portfolio_value = sum([stock_breakout['value_of_stock'] for stock_breakout in dividend_dic[max_date_of_stocks]])

    dividends_received = sum(
        [sum([(stock['dividends_total']) for stock in dividend_dic[month_of_stock]]) for month_of_stock in
         dividend_dic.keys()])

    dates_of_stock = [date.strftime("%m-%Y") for date in
                      sorted([datetime.strptime(month, "%m-%Y") for month in dividend_dic.keys()], reverse=False)]
    dividends_monthly = [sum([(stock['dividends_total']) for stock in dividend_dic[month_of_stock]]) for month_of_stock
                         in dates_of_stock]
    value_monthly = [sum([(stock['value_of_stock']) for stock in dividend_dic[month_of_stock]]) for month_of_stock in
                     dates_of_stock]

    return {"month_year_stock":dates_of_stock,"dividends_monthly": dividends_monthly, "value_monthly": value_monthly,
            "dividends_received": dividends_received, "portfolio_value": portfolio_value}
