# create database
import sqlite3
from .configurations import values

STOCK_DB = values.get("DATABASE", "STOCK_DB")

def connect():
    try:
        conn = sqlite3.connect(STOCK_DB) 
        c = conn.cursor()
        return (c, conn)
    except Exception as e:
        print("Failed to load database:", e)

def build():
    c, conn = connect()
    c.execute('''
            CREATE TABLE IF NOT EXISTS investor
            ([investor_id] INTEGER PRIMARY KEY, [name] TEXT, [address] TEXT,
            [phone_number] TEXT)
            ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS stock
            ([id] INTEGER PRIMARY KEY, [investor_id] INTEGER,
            [symbol] TEXT, [quantity] INTEGER, [purchase_price] REAL,
            [current_value] REAL, [purchase_date] TEXT, [profit_loss] TEXT,
            [yearly_earning_loss] TEXT)
            ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS bond
            ([id] INTEGER PRIMARY KEY, [investor_id] INTEGER,
            [symbol] TEXT, [quantity] INTEGER, [purchase_price] REAL,
            [current_value] REAL, [purchase_date] TEXT, [coupon] REAL,
            [yield] REAL, [profit_loss] TEXT, [yearly_earning_loss] TEXT)
            ''')

    # adding another table for data from json file
    c.execute('''
            CREATE TABLE IF NOT EXISTS transactions
            ([id] INTEGER PRIMARY KEY, [investor_id] INTEGER,
            [symbol] TEXT, [open] TEXT, [high] TEXT, [low] TEXT,
            [close] REAL, [date] TEXT, [volume] INTEGER)
            ''')
    conn.commit()
    c.close()


def add_investor(investor):
    c, conn = connect()
    c.execute(f'''
          INSERT OR IGNORE INTO investor (name, address, phone_number)
                VALUES('{investor.name}', '{investor.address}', '{investor.phone_number}')
          ''')
    conn.commit()
    c.close()


def add_stock(stock, investor):
    c, conn = connect()
    c.execute(f'''
          INSERT OR IGNORE INTO stock (id, investor_id, symbol, quantity, purchase_price, current_value, purchase_date)
                VALUES({stock.stock_id}, {investor.investor_id}, '{stock.symbol}', {stock.quantity}, {stock.purchase_price},
                       {stock.current_value}, '{stock.purchase_date}')
          ''')
    conn.commit()
    c.close()


def update_table(stock_bond, formatted_profit_loss, formatted_yearly_earning_loss):
    c, conn = connect()
    # Using string formatting to match the column width with the headers
    c.execute(f'''
                UPDATE {type(stock_bond).__name__.lower()} 
                SET profit_loss = '{formatted_profit_loss}',
                    yearly_earning_loss = '{formatted_yearly_earning_loss}'
                WHERE id = {stock_bond.stock_id}
                ''')
    conn.commit()
    c.close()


def get_stock_bond(stock_bond, columns):
    c, _ = connect()
    if hasattr(stock_bond, 'coupon') and hasattr(stock_bond, '_yield'):
        c.execute('''
            SELECT
            symbol, quantity, profit_loss, yearly_earning_loss, coupon, yield, quantity * purchase_price as total_closing_price
            FROM bond
            ''')
        columns.extend(["Coupon", "Yield"])
        columns[0] = "Bond"
    else:
        c.execute('''
            SELECT
            symbol, quantity, profit_loss, yearly_earning_loss, quantity * purchase_price as total_closing_price
            FROM stock
            ''')
    return c


def add_transaction(stock, investor, open_price, high, low, close, date, volume):
    c, conn = connect()
    c.execute(f'''
        INSERT OR IGNORE INTO transactions (investor_id, symbol, open, high, low, close, date, volume)
                VALUES({investor.investor_id}, '{stock.symbol}', '{open_price}', '{high}', '{low}', {close}, '{date}', {volume})
        ''')
    conn.commit()
    conn.close()


def add_bond(bond, investor):
    c, conn = connect()
    c.execute(f'''
        INSERT OR IGNORE INTO bond (id, investor_id, symbol, quantity, purchase_price, current_value, purchase_date, coupon, yield)
                VALUES({bond.stock_id}, {investor.investor_id}, '{bond.symbol}', {bond.quantity}, {bond.purchase_price},
                    {bond.current_value}, '{bond.purchase_date}', {bond.coupon}, {bond._yield})
        ''')
    conn.commit()
    conn.close()