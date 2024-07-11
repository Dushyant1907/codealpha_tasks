import pandas as pd # type: ignore
import yfinance as yf # type: ignore
import matplotlib.pyplot as plt # type: ignore
from datetime import datetime
import json

portfolio = []

def add_stock(symbol, shares, purchase_price, purchase_date):
    stock = {
        'symbol': symbol,
        'shares': shares,
        'purchase_price': purchase_price,
        'purchase_date': purchase_date
    }
    portfolio.append(stock)

def remove_stock(symbol):
    global portfolio
    portfolio = [stock for stock in portfolio if stock['symbol'] != symbol]


def get_stock_data(symbol, start_date):
    stock = yf.Ticker(symbol)
    hist = stock.history(start=start_date)
    return hist

def update_portfolio(symbol, shares=None, purchase_price=None, purchase_date=None):
    for stock in portfolio:
        if stock['symbol'] == symbol:
            if shares is not None:
                stock['shares'] = shares
            if purchase_price is not None:
                stock['purchase_price'] = purchase_price
            if purchase_date is not None:
                stock['purchase_date'] = purchase_date
            break

def calculate_portfolio_value():
    total_value = 0
    for stock in portfolio:
        current_price = yf.Ticker(stock['symbol']).history(period='1d')['Close'].iloc[-1]
        total_value += current_price * stock['shares']
    return total_value

def calculate_gains():
    gains = {}
    for stock in portfolio:
        current_price = yf.Ticker(stock['symbol']).history(period='1d')['Close'].iloc[-1]
        gain = (current_price - stock['purchase_price']) * stock['shares']
        gains[stock['symbol']] = gain
    return gains


def plot_portfolio():
    symbols = [stock['symbol'] for stock in portfolio]
    values = [yf.Ticker(stock['symbol']).history(period='1d')['Close'].iloc[-1] * stock['shares'] for stock in portfolio]
    plt.figure(figsize=(10, 6))
    plt.bar(symbols, values)
    plt.xlabel('Stock Symbol')
    plt.ylabel('Value ($)')
    plt.title('Portfolio Value by Stock')
    plt.show()

def save_portfolio(filename='portfolio.json'):
    with open(filename, 'w') as f:
        json.dump(portfolio, f)

def load_portfolio(filename='portfolio.json'):
    global portfolio
    with open(filename, 'r') as f:
        portfolio = json.load(f)
        
def view_portfolio():
    for stock in portfolio:
        print(f"Symbol: {stock['symbol']}, Shares: {stock['shares']}, Purchase Price: ${stock['purchase_price']}, Purchase Date: {stock['purchase_date']}")

        
# to dd stocks to the portfolio
add_stock('AAPL', 10, 150.0, '2022-01-01')
add_stock('MSFT', 5, 250.0, '2022-01-01')
add_stock('GOOGL', 8, 1800.0, '2021-06-15')
add_stock('TSLA', 3, 700.0, '2021-03-20')
add_stock('MS',4, 900.0, '2022-01-01')

# View portfolio
print("Current Portfolio:")
view_portfolio()

# Remove a stock from the portfolio
remove_stock('TSLA')

# Update stock information
update_portfolio('AAPL', shares=15)

# Calculate portfolio value
print(f"Total Portfolio Value: ${calculate_portfolio_value():.2f}")

# Calculate gains
gains = calculate_gains()
for symbol, gain in gains.items():
    print(f"{symbol}: ${gain:.2f}")

# Plot portfolio
plot_portfolio()

# Save and load portfolio
save_portfolio()
load_portfolio()

