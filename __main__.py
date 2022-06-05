"""
PORTFOLIO PROGRAMMING ASSIGNMENT - IMPROVING THE STOCK PROBLEM WITH ADDITIONAL FUNCTIONALITY
Name: Ronit Sonawane
Course: ICT 4370-1
Date: 06/04/2022
The python code calculates how much the investor has earned or lost.
It also calculates the yearly earning/loss rate for each stock.
Calculations of profit/loss and yearly earning/loss rate each have their own module
If complete portfolio is in profit, the program prints the symbol of highest increased stock.
If complete portfolio is in loss, the program prints the symbol of least decreased stock.
Finally, the program saves a graph in .png format to show the transaction history.
The data is loaded could be loaded from csv, json files.
The input files can be defined in config.ini file.
Prerequisite: Please put Lesson6_Data_Bonds.csv, Lesson6_Data_Stocks.csv and AllStocks.json files in the working directory.
"""

import datetime
import json
import sys
import pandas as pd
from .configurations import values
from .investor import Investor
from .stock import Stock
from .bond import Bond
from .database_helper import build, add_investor, add_stock, add_transaction, add_bond
from .output_helper import create_output
from .visualizer import create_graph

NAME = values.get("INVESTOR", "NAME")
ADDRESS = values.get("INVESTOR", "ADDRESS")
CONTACT = values.get("INVESTOR", "ADDRESS")
STOCK_CSV = values.get("CSV", "STOCK_CSV")
BOND_CSV = values.get("CSV", "BOND_CSV")
STOCK_JSON = values.get("JSON", "STOCK_JSON")
PNG = values.get("GRAPH", "PNG")


def main():
    # build sqlite database
    build()

    # Load data from files
    # Use try except to handle errors, exit program with exit code 1 if try fails
    try:
        stocks_dataframe = pd.read_csv(STOCK_CSV)
    except FileNotFoundError:
        print(STOCK_CSV)
        print("Please make sure stock file is in working directory")
        sys.exit(1)
    except Exception as e:
        print("Unexpected error", e)
        sys.exit(1)


    try:
        bonds_dataframe = pd.read_csv(BOND_CSV)
    except FileNotFoundError:
        print("Please make sure bond file is in working directory")
        sys.exit(1)
    except Exception as e:
        print("Unexpected error", e)
        sys.exit(1)

    try:
        json_file = open(STOCK_JSON)
        json_data = json.load(json_file)
    except FileNotFoundError:
        print("Please make sure AllStocks.json file is in working directory")
        sys.exit(1)
    except Exception as e:
        print("Unexpected error", e)
        sys.exit(1)

    investor = Investor(1, NAME, ADDRESS, CONTACT)
    add_investor(investor)

    stock_dictionary = {}
    # populate stocks and bonds properties of investor from loaded data
    for i in stocks_dataframe.itertuples():
        stock = Stock(i.__getattribute__('Index'), i.__getattribute__('SYMBOL'), int(i.__getattribute__('NO_SHARES')),
                    float(i.__getattribute__('PURCHASE_PRICE')), float(i.__getattribute__('CURRENT_VALUE')), i.__getattribute__('PURCHASE_DATE'))
        investor.stocks.append(stock)

        # add stock object to dictionary for further operations on the object
        stock_dictionary[stock.symbol] = stock
        add_stock(stock, investor)
    

    # iterate over data from json file and updat Stock object
    for transaction in json_data:
        symbol = transaction["Symbol"]
        
        # the google stock symbol does not match with the previous data hence manipulating it to make it consistent
        if symbol == "GOOG":
            symbol += "L"
        open_price = transaction["Open"]
        high = transaction["High"]
        low = transaction["Low"]
        close = transaction["Close"]
        date = datetime.datetime.strptime(transaction["Date"], "%d-%b-%y")
        volume = transaction["Volume"]

        stock =  stock_dictionary.get(symbol)
        add_transaction(stock, investor, open_price, high, low, close, date, volume)
        try:
            # the update() method of dictionary updates the value for given key if the key already exists,
            # if the key does not exist in the dictionary a new key, value pair is added.
            stock_dictionary.update({symbol:stock.update(open_price, high, low, close, date, volume)})
        except Exception as e:
            print(e)


    for i in bonds_dataframe.itertuples():
        bond = Bond(i.__getattribute__('Index'), i.__getattribute__('SYMBOL'), int(i.__getattribute__('NO_SHARES')),
                    float(i.__getattribute__('PURCHASE_PRICE')), float(i.__getattribute__('CURRENT_VALUE')), i.__getattribute__('PURCHASE_DATE'),
                    i.__getattribute__('Coupon'), i.__getattribute__('Yield'))
        investor.bonds.append(bond)
        add_bond(bond, investor)
        
    print("\tStock ownership for {}".format(NAME))

    stocks_output = create_output(investor.stocks)
    bonds_output = create_output(investor.bonds)

    print(stocks_output)

    # max() gets the highest number from the list of profit/loss. That gives us the highest increase if all stocks had profit.
    # since the loss will be returned in negative, we use max() als to get the least loss we have to get the biggest number from all negative numbers.
    # the key parameter for max takes in a lambda function that defines computation (logic) for calculating max value
    # max_profit_loss = max(database, key=lambda x: x['profit_loss']/x['no_of_shares'])['stock_symbol']
    max_profit_loss = max(investor.stocks, key=lambda x: x.total_profit_loss/x.quantity).symbol

    # all() return True for all elements in range evaluate to True, else False.
    # The list comprehenstion passed to all() compares each element in profit_loss with 0 (to identify if its a profit or loss)
    if all(stock.total_profit_loss > 0 for stock in investor.stocks):
        print("The stock with the highest increase in value in your portfolio on a per-share basis is: {}".format(max_profit_loss))
    elif all(stock.total_profit_loss < 0 for stock in investor.stocks):
        print("The stock with least decrease in value in your portfolio on a per-share basis is: {}".format(max_profit_loss))
    else:
        print("Some stocks were profittable, but some were in loss")

    print(bonds_output)
    create_graph(stock_dictionary, PNG)

if __name__ == "__main__":
    main()