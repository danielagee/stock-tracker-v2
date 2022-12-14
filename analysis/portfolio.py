import pandas as pd
import analysis.constants as c
import datetime

# Read the CSV file containing the stock ticker data.
df_portfolio = c.df_portfolio

# Label the date column as date-time format in pandas to manage the merges properly.
df_portfolio['Date'] = pd.to_datetime(c.df_portfolio['Date'])

# Strip the time out of date-time so that only dates remain
df_portfolio['Date'] = df_portfolio['Date'].dt.date

# Cost of the trade
df_portfolio[f'Trade Cost'] = df_portfolio[f'Traded'] * df_portfolio[f'Price Paid']

# Convert the stocks in the portfolio to a list of tickers
tickers = df_portfolio.Ticker.tolist()
# Remove duplicates and sort alphabetically
tickers = sorted([*set(tickers)])
start_date = df_portfolio['Date'].min() - datetime.timedelta(days=c.start_delay)

# print(df_portfolio)
# print(tickers)
