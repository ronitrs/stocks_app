import datetime
import sys


class Stock:
    def __init__(self, stock_id, symbol, quantity, purchase_price, current_value, purchase_date):
        self.stock_id = stock_id
        self.symbol = symbol
        try:
            self.quantity = int(quantity)
        except ValueError:
            print("Unexpected data type for quantity, int expected")
            sys.exit(1)
        try:
            self.purchase_price = float(purchase_price)
        except ValueError:
            print("Unexpected data type for purchase price, float expected")
            sys.exit(1)
        self.purchase_date = purchase_date
        try:
            self.current_value = float(current_value)
        except ValueError:
            print("Unexpected data type for current value, float expected")
            sys.exit(1)
        self.total_profit_loss = None
        self.yearly_earning_loss_rate = None

        # additional properties to store data from json file
        self.open = []
        self.high = []
        self.low = []
        self.low = []
        self.close = []
        self.date = []
        self.volume = []

        # call functions to calculate profit loss and yearly earning loss
        self.calculate_profit_loss()
        self.calculate_yearly_earning_loss_rate()


    # function to calculate yearly earning/loss rate
    def calculate_yearly_earning_loss_rate(self,):

        current_date = datetime.datetime.today()

        # strptime() creates datetime object from date string
        purchase_date = datetime.datetime.strptime(self.purchase_date, "%m/%d/%Y")

        years_past = current_date.year - purchase_date.year

        # formula for calculating yearly earning/loss rate
        try:
            self.yearly_earning_loss_rate = ((((self.current_value - self.purchase_price)/self.purchase_price)/years_past)*100)
        except ZeroDivisionError:
            print("Cannot calculate yearly earning/loss within same year")
            sys.exit(1)
        return self.yearly_earning_loss_rate


    # function to calculate profit/loss
    def calculate_profit_loss(self,):
        profit_loss_per_share = self.current_value - self.purchase_price
        self.total_profit_loss = profit_loss_per_share * self.quantity
        return self.total_profit_loss

    # method to add data to the lists of open, close, high, low, and volume properties
    def update(self, open, high, low, close, date, volume):
        self.open.append(open)
        self.high.append(high)
        self.low.append(low)
        self.close.append(close)
        self.date.append(date)
        self.volume.append(volume)
        return self