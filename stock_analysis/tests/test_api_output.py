import unittest
from formatOutput import formatStockOutput
from api import AlphaVantage
from datetime import datetime


class TestTermNodeMatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_key = "BAD_API_KEY"
        cls.stock_ticker = "TTD"
        cls.alpha_vantage = AlphaVantage(cls.api_key)
        cls.get_stock_data = cls.alpha_vantage.getTimeSeries(cls.stock_ticker)
        cls.get_stock_format = formatStockOutput(cls.get_stock_data)

    def testAnyApiKey(self):
        """

        This method is to test the api key used to retrieve data from AlphaVantage. ANY API Key can be used!!


        """
        self.assertEquals(dict, type(self.alpha_vantage.getTimeSeries(self.stock_ticker)))

    def testBadStockTicker(self):
        """


        This test is to check whether a ValueError will be returned when a bad stock ticker is submitted to the API.

        """
        self.assertRaises(ValueError, self.alpha_vantage.getTimeSeries, "THIS_IS_BAD_STOCK_TICKER")

    def testMonthHighestStockPrice(self):
        """

        This is the link to the TTD stock in yahoo finance https://finance.yahoo.com/quote/TTD/history?period1=1596240000&period2=1598832000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true

        The max. high for ttd in August 2020 was 510 and the test checks the formatted data to check whether the data matches.

        """
        maximum_high_price_august = self.get_stock_format['08-2020']['maximum high']
        self.assertEquals(510.0, maximum_high_price_august)

    def testMonthLowestStockPrice(self):
        """

        The min. low for ttd in August 2020 was 444.54 and the test checks the formatted data to check whether the data matches.


        """
        minimum_low_price_august = self.get_stock_format['08-2020']['minimum low']
        self.assertEquals(444.54, minimum_low_price_august)

    def testFirstMonthOfStock(self):
        """


        The first month of trade for TTD was 09-2016 and the test checks the formatted data to check whether the data matches.

        """
        monthyear_of_stock_list = self.get_stock_format.keys()
        format_str = "%m-%Y"
        dates_arranged = sorted([(datetime.strptime(date_, format_str)) for date_ in monthyear_of_stock_list])
        first_date = min(dates_arranged).strftime('%m-%Y')
        self.assertEquals("09-2016", first_date)

    def testLatestMonthOfStock(self):
        """

        The latest month of trade for TTD was 10-2020 and the test checks the formatted data to check whether the data matches.

        """
        monthyear_of_stock_list = self.get_stock_format.keys()
        format_str = "%m-%Y"
        dates_arranged = sorted([(datetime.strptime(date_, format_str)) for date_ in monthyear_of_stock_list])
        latest_date = max(dates_arranged).strftime('%m-%Y')
        self.assertEquals("10-2020", latest_date)

    def testAllMonthsOf2020(self):
        """

        The TTD stock was traded every month this year and the test checks the formatted data to has 10 months of results.

        """
        monthyear_of_stock_list = self.get_stock_format.keys()
        format_str = "%m-%Y"
        dates_arranged = sorted([(datetime.strptime(date_, format_str)) for date_ in monthyear_of_stock_list])
        dates_arranged_2020 = [date_ for date_ in dates_arranged if date_.year == 2020]
        self.assertEquals(10, len(dates_arranged_2020))


if __name__ == '__main__':
    unittest.main()
