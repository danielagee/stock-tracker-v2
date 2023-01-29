# Enable switch on/off for single and multi-plot
# Fix value of 100% loss on sell
# Fix relative S&P500 performance calculation.
# Add dividends and sales as returns rather than invested. Invested dividends are not double counted.
# Clean up constants.py code
# Stop running on import. Make each file a def main() with if __name__ == "__main__": n\ main()
# Learn Lambda
# Plot of stock value (owned * price) on lower graph in individual plot window

import pandas as pd
import datetime
import time
import yfinance as yf
import numpy as np

# portfolio_path = 'C:\\Python\\PythonProjects\\stock-tracker-v2\\cvs files\\Input Files\\'
# portfolio_file = 'Portfolio - FAANG.csv'
portfolio_path = 'C:\\Python\\stocks\\Portfolio Input\\'
portfolio_file = 'Portfolio - DMA.csv'
output_path = 'C:\\Python\\PythonProjects\\stock-tracker-v2\\cvs files\\Output Files\\'
pre_trade_look = 30
backward_look = 0
benchmarks = ['^GSPC', '^DJI', '^IXIC']
rel_benchmark = '^GSPC'
sum_headers = ('Value', 'Invested', 'Div Paid')
ma_list = {'21', '50', '200'}


def portfolio_extract(path, file):
    df_pe = pd.read_csv(f'{path}{file}')  # Read the CSV file containing the stock ticker data.
    df_pe['Date'] = pd.to_datetime(df_pe['Date'])  # Label date column as date-time format in pandas.
    df_pe['Date'] = df_pe['Date'].dt.date  # Strip the time out of date-time so that only dates remain
    df_pe[f'Trade Cost'] = df_pe[f'Traded'] * df_pe[f'Price Paid']  # Calculate cost of the trade
    return df_pe


def start_date(df_trades, offset):  # Get start date of portfolio analysis based on earliest trade date plus an offset.
    return df_trades['Date'].min() - datetime.timedelta(days=offset)


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


def relative_performance(out_path, tick, bm):  # Calculate performance vs benchmark
    print('Calculating Relative Performance')
    df_rp = pd.read_csv(f'{out_path}{tick}.csv')
    df_bm = pd.read_csv(f'{out_path}{bm}.csv')
    df_rp[f'{bm}_rel'] = (df_rp[f'Close'] / df_bm['Close'])
    df_rp[f'{bm}_rel_%'] = (df_rp[f'Close'] / df_rp['Close'].iat[0]) / (df_bm['Close'] / df_bm['Close'].iat[0])
    df_rp = df_rp.drop(df_rp.columns[[0]], axis=1)
    df_rp.to_csv(f'{out_path}{tick}.csv')
    return ()


def create_merged(start_merge):
    df_merged_v = pd.DataFrame(
        [[start_merge, 0, 0, 0, 0, 0]],
        columns=['Date', 'Total Invested', 'Total Value', 'Returns', 'Returns %', 'Total Div Paid'])
    return df_merged_v


def merge_additional_ticker(out_path, tick, df_merged_val):
    df_ticker = pd.read_csv(f'{out_path}{tick}.csv')
    df_ticker = df_ticker.drop(df_ticker.columns[[0]], axis=1)  # Drop old index column

    # Label the date column as date-time format in pandas to manage the merges properly.
    df_ticker['Date'] = pd.to_datetime(df_ticker['Date'])
    df_ticker['Date'] = df_ticker['Date'].dt.date

    # Extract only the portfolio rows with an active trade.
    df_shares = df_portfolio.loc[df_portfolio['Ticker'] == tick]

    # Delete the ticker column from df_shares
    df_shares = df_shares.drop('Ticker', axis=1)

    # Merge the shares bought/sold and ticker price data from the portfolio and yfinance data
    df_merged = pd.merge(df_ticker, df_shares, on='Date', how='outer')

    # Rename columns to differentiate stocks
    df_merged.rename(columns={'Open': f'Open-{tick}'}, inplace=True)
    df_merged.rename(columns={'High': f'High-{tick}'}, inplace=True)
    df_merged.rename(columns={'Low': f'Low-{tick}'}, inplace=True)
    df_merged.rename(columns={'Close': f'Close-{tick}'}, inplace=True)
    df_merged.rename(columns={'Volume': f'Vol-{tick}'}, inplace=True)
    df_merged.rename(columns={'Dividends': f'Div-{tick}'}, inplace=True)
    df_merged.rename(columns={'Price Paid': f'Price-{tick}'}, inplace=True)
    df_merged.rename(columns={'^GSPC_rel': f'GSPC_rel-{tick}'}, inplace=True)
    df_merged.rename(columns={'^GSPC_rel_%': f'GSPC_rel_%-{tick}'}, inplace=True)
    df_merged.rename(columns={'Traded': f'Traded-{tick}'}, inplace=True)
    df_merged.rename(columns={'Price Paid': f'Price Paid-{tick}'}, inplace=True)
    df_merged.rename(columns={'Trade Cost': f'Trade Cost-{tick}'}, inplace=True)

    # Process Merged Data
    df_merged = df_merged.sort_values(by='Date')  # Sort the new dataframe by date
    df_merged = df_merged.reset_index(drop=True)  # Reset the index of the dataframe without adding a column
    df_merged[f'Shares Owned-{tick}'] = df_merged[f'Traded-{tick}'].cumsum()  # Sum owned shared from traded shares
    df_merged[f'Invested-{tick}'] = df_merged[f'Trade Cost-{tick}'].cumsum()  # Sum total paid for the shares from paid
    df_merged[f'Shares Owned-{tick}'].fillna(method='pad', inplace=True)  # convert NaN to value from row above
    df_merged[f'Invested-{tick}'].fillna(method='pad', inplace=True)  # convert NaN to value from row above

    # Create a new column and get close price x quantity owned.
    df_merged[f'Value-{tick}'] = df_merged[f'Close-{tick}'] * df_merged[f'Shares Owned-{tick}']

    # Create new columns for returns and returns % based on stock value appreciation/depreciation.
    df_merged[f'Returns-{tick}'] = df_merged[f'Value-{tick}'] - df_merged[f'Invested-{tick}']
    df_merged[f'Returns %-{tick}'] = df_merged[f'Returns-{tick}'] / df_merged[f'Invested-{tick}'] * 100

    # Calculate value of dividends paid.
    df_merged[f'Div Paid-{tick}'] = df_merged[f'Div-{tick}'] * df_merged[f'Shares Owned-{tick}']

    df_merged[f'Div-{tick}'] = df_merged[f'Div Paid-{tick}'].cumsum()  # Sum total dividends received on date
    df_merged[f'Div-{tick}'].fillna(method='pad', inplace=True)  # Fill all rows between dividend pay days
    df_merged.dropna(axis=0, subset=[f'Close-{tick}'], inplace=True)  # Drop rows without price to give continuous data
    df_merged = df_merged.reset_index(drop=True)  # Reset the index of the dataframe without adding a column
    df_merged = df_merged.drop(df_merged.columns[[7, 8, 9, 10]], axis=1)  # Drop unnecessary columns
    df_merged_val = pd.merge(df_merged_val, df_merged, how='outer')  # Merge new df with existing df
    df_merged_val.drop_duplicates(inplace=True)
    return df_merged_val


def sum_columns(header_prefix, out_path):  # Create list of eaders to sum. format 'header-xxx' where xxx = ticker.
    sum_col = list(set([f'{header_prefix}-' + sub for sub in df_portfolio.Ticker]))  # Eliminate duplicate entries.
    # Sum the values of all headers in the correct format (ticker and data type)
    df_merged_value[f'Total {header_prefix}'] = df_merged_value[sum_col].sum(axis=1)
    df_merged_value.to_csv(f'{out_path}merged_value.csv')  # Write values to the CSV file
    return()


df_portfolio = portfolio_extract(portfolio_path, portfolio_file)
start_analysis = start_date(df_portfolio, pre_trade_look)
end_analysis = end_date(backward_look)
tickers = ticker_list(df_portfolio)

for bm in benchmarks:  # Refresh benchmark data from yfinance
    refresh_portfolio(bm, start_analysis, end_analysis, output_path)
for ticker in tickers:
    refresh_portfolio(ticker, start_analysis, end_analysis, output_path)  # Refresh stock data from yfinance & do calcs
    for days in ma_list:  # Calculate moving average
        moving_average(output_path, ticker, int(days))
    relative_performance(output_path, ticker, rel_benchmark)  # Calculate relative performance vs benchmark

df_merged_value = create_merged(start_analysis)
for ticker in tickers:
    df_merged_value = merge_additional_ticker(output_path, ticker, df_merged_value)
for header in sum_headers:
    sum_columns(header, output_path)

df_merged_value.replace(0, np.nan, inplace=True)  # Convert zero values in dividends paid column to NaN.
df_merged_value[f'Total Div Paid'].fillna(method='pad', inplace=True)  # Fill dividends paid NaN from above
df_merged_value['Returns'] = df_merged_value['Total Value'] - df_merged_value['Total Invested']
df_merged_value['Returns %'] = df_merged_value['Returns'] / df_merged_value['Total Invested']*100
df_merged_value.to_csv(f'{output_path}merged_value.csv')
