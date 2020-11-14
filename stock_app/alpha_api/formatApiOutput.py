from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class PricingRange:
    open: str
    high: str
    low: str
    close: str
    dividend: str

    def __post_init__(self):
        self.open = float(self.open)
        self.high = float(self.high)
        self.low = float(self.low)
        self.close = float(self.close)
        self.dividend = float(self.dividend)


@dataclass
class StockHistory:
    date: datetime
    pricing: PricingRange

    def __post_init__(self):
        self.date = datetime.strptime(self.date, "%Y-%m-%d")




def formatStockOutput(jsonOutput: Dict) -> Dict:
    """
    This method takes the output from the api and then stores the response into a different dictionary which is formatted
    by year/month.

    The premise behind this method is to find the max-high/min-low by grouping the stock price by month-year and then sort
    the data to find the corresponding results. The final data output will be stored into the max_low_dic.

    :param jsonOutput: stock output from api
    :return: dictionary containing month-year and the max-high/min-low price of the stock.
    """
    breakout_year_month_dic = {}
    max_low_dic = {}



    for key, value in jsonOutput.items():
        stock_price = PricingRange(open=value['1. open'],
                                   high=value['2. high'],
                                   low=value['3. low'],
                                   close=value['4. close'],
                                   dividend=value['7. dividend amount'])

        stockHistoryDC = StockHistory(date=key, pricing=stock_price)

        day, month, year = stockHistoryDC.date.day, stockHistoryDC.date.month, stockHistoryDC.date.year

        if year in breakout_year_month_dic:
            if month in breakout_year_month_dic[year]:
                breakout_year_month_dic[year][month].append(stockHistoryDC)
            else:
                breakout_year_month_dic[year][month] = [stockHistoryDC]
        else:
            breakout_year_month_dic[year] = {month: [stockHistoryDC]}

    for year in breakout_year_month_dic.values():
        for month in year.values():
            high = sorted(month, key=lambda x: x.pricing.high, reverse=True)[0]
            low = sorted(month, key=lambda x: x.pricing.low, reverse=False)[0]
            dividend = sorted(month, key=lambda x: x.pricing.dividend, reverse=True)[0]
            max_low_dic[high.date.strftime("%m-%Y")] = {"maximum high": high.pricing.high,
                                                        "minimum low": low.pricing.low,
                                                        'dividend amount':dividend.pricing.dividend}

    return max_low_dic
