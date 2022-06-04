import pandas as pd
from .database_helper import update_table, get_stock_bond
# functions to create pandas dataframe for output
def create_output(database):
    # output = []
    columns=["Stock", "Quantity", "Earnings/Loss", "Yearly Earning/Loss"]
    for stock_bond in database:
        # round() rounds the numbers after decimal, format() adds zeros after decimal if necessary to match expected output format.
        formatted_profit_loss = format(round(stock_bond.total_profit_loss, 2), '.2f')

        # split() and join() used to insert $ sign after - sign (as shown in assignment requirements)
        formatted_profit_loss = "$" + formatted_profit_loss if float(formatted_profit_loss) > 0 else "-$".join(formatted_profit_loss.split("-"))
        formatted_yearly_earning_loss = format(round(stock_bond.yearly_earning_loss_rate, 2), '.2f') + "%"

        update_table(stock_bond, formatted_profit_loss, formatted_yearly_earning_loss)
        c = get_stock_bond(stock_bond, columns)
        df = pd.DataFrame(c.fetchall(), columns=columns+["Total Closing Price"])
        c.close()
    return df