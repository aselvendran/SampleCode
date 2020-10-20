import sys
import importlib



if __name__ == "__main__":
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    stock_ticker = argument_list[0]

    module_to_run = importlib.import_module("summarizeOutput")
    method_to_run = getattr(module_to_run, "getStockTimeSeries")

    method_to_run(*[stock_ticker])


