# Add baseline of invest and hold
# Add S&P 500 benchmark

import pandas as pd
import datetime
import time
import yfinance as yf
import numpy as np

# portfolio_path = 'C:\\Python\\PythonProjects\\stock-tracker-v2\\cvs files\\Input Files\\'
portfolio_path = 'C:\\Python\\stocks\\Portfolio Input\\'

# portfolio_file = 'Portfolio - FAANG.csv'
# portfolio_file = 'Portfolio - DMA.csv'
# portfolio_file = 'Portfolio - Potential Purchase Evaluation.csv'
portfolio_file = 'Portfolio - Potential Purchase Evaluation - Short.csv'

# output_path = 'C:\\Python\\PythonProjects\\stock-tracker-v2\\cvs files\\Output Files\\'
output_path = 'C:\\Python\\stocks\\Portfolio Output\\'

pre_trade_look = 365*10
backward_look = 0
benchmarks = ['^GSPC', '^DJI', '^IXIC']
rel_benchmark = '^GSPC'
sum_headers = ('Value', 'Invested', 'Div Paid')
ma_list = {21, 50, 200}
starting_cash = 1000
starting_shares = 0


def portfolio_extract(path, file):
    df_pe = pd.read_csv(f'{path}{file}')  # Read the CSV file containing the stock ticker data.
    # df_pe['Date'] = pd.to_datetime(df_pe['Date'])  # Label date column as date-time format in pandas.
    # df_pe['Date'] = df_pe['Date'].dt.date  # Strip the time out of date-time so that only dates remain
    # df_pe[f'Trade Cost'] = df_pe[f'Traded'] * df_pe[f'Price Paid']  # Calculate cost of the trade
    return df_pe


def start_date(offset):  # Get start date of portfolio analysis based on earliest trade date plus an offset.
    return datetime.date.today() - datetime.timedelta(days=offset)


def end_date(offset):  # Get start date of portfolio analysis based on earliest trade date plus an offset.
    return datetime.date.today() - datetime.timedelta(days=offset)


def ticker_list(df_port):  # Convert the stocks in the portfolio to a list of tickers
    return df_port.Ticker.unique()


def refresh_portfolio(stock_ticker, start_a, end_a, path_out):
    print(f'Refreshing {stock_ticker} portfolio')
    tick = yf.Ticker(stock_ticker)
    hist = tick.history(start=start_a, end=end_a)
    hist.reset_index(drop=False, inplace=True)
    hist['Date'] = pd.to_datetime(hist['Date'])  # Convert the date column to date-time format.
    hist['Date'] = hist['Date'].dt.date  # Drop the time component from date column.
    hist.to_csv(f'{path_out}{stock_ticker}.csv')
    time.sleep(1)
    return()


def moving_average(out_path, tick, duration):  # Calculate the moving average from closing price and a defined duration
    print(duration)
    df_ma = pd.read_csv(f'{out_path}{tick}.csv')
    df_ma[f'{duration}-dma'] = df_ma[f'Close'].rolling(window=duration).mean()
    df_ma = df_ma.drop(df_ma.columns[[0]], axis=1)
    df_ma = df_ma.drop(['Unnamed'], axis=1, errors='ignore')
    df_ma.to_csv(f'{out_path}{tick}.csv')
    return ()


def performance_model_test(out_path, tick):  # Calculate the performance of a trade model
    df_test = pd.read_csv(f'{out_path}{tick}.csv')
    short_interval = list(ma_list)[2]  # Reads first duration in ma list
    mid_interval = list(ma_list)[1]  # Reads second duration in ma list
    long_interval = list(ma_list)[0]  # Reads third duration in ma list
    df_test.loc[0, "cash"] = starting_cash
    df_test.loc[0, "owned_shares"] = starting_shares

    # If statement to check for short interval moving average > mid-interval moving average. If yes, own, if no, sell.
    df_test.loc[df_test[f'{short_interval}-dma'] > df_test[f'{mid_interval}-dma'], f'rating'] = "Buy"  # Buy when 21 day MA is > 50 day MA
    # df_test.loc[df_test[f'{short_interval}-dma'] > df_test[f'{mid_interval}-dma'], f'rating'] = "Hold"  # Buy when 21 day MA is < 50 day MA
    df_test.loc[df_test[f'Close'] <= df_test[f'{short_interval}-dma'], f'rating'] = "Sell"  # Sell when close is < 21 day MA

    # Check if the rating is the same as the previous day
    df_test['rating_stable'] = df_test.rating.eq(df_test.rating.shift(periods=1))
    df_test.loc[(df_test['rating_stable'] == False) & (df_test['rating'] == 'Sell'), 'action'] = 'Sold'
    df_test.loc[(df_test['rating_stable'] == False) & (df_test['rating'] == 'Buy'), 'action'] = 'Bought'

    for i in range(1, len(df_test)):
        if df_test.loc[i, "action"] == "Bought" and df_test.loc[i-1, "owned_shares"] == 0:
            bought_shares = np.floor(df_test.loc[i-1, "cash"] / df_test.loc[i, "Close"])
            df_test.loc[i, "owned_shares"] = bought_shares
            df_test.loc[i, "cash"] = df_test.loc[i-1, "cash"] - bought_shares * df_test.loc[i, "Close"]
        elif df_test.loc[i, "action"] == "Sold":
            sold_shares = df_test.loc[i-1, "owned_shares"]
            df_test.loc[i, "cash"] = df_test.loc[i-1, "cash"] + sold_shares * df_test.loc[i, "Close"]
            df_test.loc[i, "owned_shares"] = 0
        else:
            df_test.loc[i, "cash"] = df_test.loc[i-1, "cash"]
            df_test.loc[i, "owned_shares"] = df_test.loc[i-1, "owned_shares"]

    df_test = df_test.drop(df_test.columns[[0]], axis=1)
    df_test = df_test.drop(['Unnamed'], axis=1, errors='ignore')
    df_test.to_csv(f'{out_path}{tick}.csv')

    print('Model test completed.')
    return ()


def returns_analysis(out_path, tick):  # Checks returns of the model.
    df_test = pd.read_csv(f'{out_path}{tick}.csv')

    df_test['portfolio_value'] = df_test['cash'] + df_test.owned_shares * df_test.Close

    df_test = df_test.drop(df_test.columns[[0]], axis=1)
    df_test.to_csv(f'{out_path}{tick}.csv')

    print('Returns analysis completed.')
    return ()


def buy_hold_returns(out_path, tick):  # Checks returns of the model.
    df_test = pd.read_csv(f'{out_path}{tick}.csv')

    df_test['portfolio_value'] = df_test['cash'] + df_test.owned_shares * df_test.Close

    df_test = df_test.drop(df_test.columns[[0]], axis=1)
    df_test.to_csv(f'{out_path}{tick}.csv')

    print('Returns analysis completed.')
    return ()


def create_merged(start_merge):
    df_merged_v = pd.DataFrame(
        [[start_merge, 0, 0, 0, 0, 0]],
        columns=['Date', 'Total Invested', 'Total Value', 'Returns', 'Returns %', 'Total Div Paid'])
    return df_merged_v


df_portfolio = portfolio_extract(portfolio_path, portfolio_file)
# start_analysis = start_date(pre_trade_look)
start_analysis = datetime.datetime(1960, 1, 1) # start_date(df_portfolio, pre_trade_look)
end_analysis = end_date(backward_look)
tickers = ticker_list(df_portfolio)

for bm in benchmarks:  # Refresh benchmark data from yfinance
    refresh_portfolio(bm, start_analysis, end_analysis, output_path)

for ticker in tickers:
    refresh_portfolio(ticker, start_analysis, end_analysis, output_path)  # Refresh stock data from yfinance & do calcs
    for days in ma_list:  # Calculate moving average
        moving_average(output_path, ticker, int(days))
    performance_model_test(output_path, ticker)
    returns_analysis(output_path, ticker)
    buy_hold_returns()

df_merged_value = create_merged(start_analysis)
