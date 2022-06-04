from matplotlib import pyplot as plt

# create graph using matplotlib
def create_graph(stock_dictionary, PNG):
    for stock in stock_dictionary.values():
        plt.plot_date(stock.date, stock.close, linestyle = "solid", marker = "None", label = stock.symbol)
    plt.legend()
    plt.savefig(PNG)