import pandas as pd
import analysis.portfolio as portfolio
import analysis.constants as c
import analysis.yfinance_import
import analysis.yfinance_dividends

df_merged_value = pd.DataFrame([[portfolio.start_date, 0, 0, 0, 0, 0]], columns=['Date', 'Total Value', 'Total Invested', 'Returns', 'Returns %', 'Portfolio Div'])

# Label the date column as date-time format in pandas to manage the merges properly.
df_merged_value['Date'] = pd.to_datetime(df_merged_value['Date'])
df_merged_value['Date'] = df_merged_value['Date'].dt.date

for ticker in portfolio.tickers:
    df_ticker = pd.read_csv(f'{c.output_path}{ticker}.csv')

    # Extract only the portfolio rows relevant to the ticker we want to look at.
    df_shares = portfolio.df_portfolio.loc[portfolio.df_portfolio['Ticker'] == ticker]

    # Delete the ticker column from df_shares
    df_shares = df_shares.drop('Ticker', axis=1)

    # Label the date column as date-time format in pandas to manage the merges properly.
    df_ticker['Date'] = pd.to_datetime(df_ticker['Date'])
    df_ticker['Date'] = df_ticker['Date'].dt.date
    df_shares['Date'] = pd.to_datetime(df_shares['Date'])
    df_shares['Date'] = df_shares['Date'].dt.date

    # Merge the shares and ticker data from the portfolio and yfinance data
    df_merged = pd.merge(df_ticker, df_shares, how='outer')

    # Rename columns to differentiate stocks
    df_merged.rename(columns={'Open': f'Open-{ticker}'}, inplace=True)
    df_merged.rename(columns={'High': f'High-{ticker}'}, inplace=True)
    df_merged.rename(columns={'Low': f'Low-{ticker}'}, inplace=True)
    df_merged.rename(columns={'Close': f'Close-{ticker}'}, inplace=True)
    df_merged.rename(columns={'Price Paid': f'Price-{ticker}'}, inplace=True)
    df_merged.rename(columns={'Traded': f'Traded-{ticker}'}, inplace=True)
    df_merged.rename(columns={'Trade Cost': f'Trade Cost-{ticker}'}, inplace=True)

    # Merge in Dividend Data

    # Label the date column as date-time format in pandas to manage the merges properly.
    df_div = pd.read_csv(f'{c.output_path}div-{ticker}.csv')
    df_div['Date'] = df_div['Date'].str[:10]
    df_div['Date'] = pd.to_datetime(df_div['Date'], format='%Y-%m-%d')
    df_div['Date'] = df_div['Date'].dt.date
    # Merge the dividend data from yfinance
    df_merged = pd.merge(df_merged, df_div, how='outer')
    # Rename columns to differentiate stocks
    df_merged.rename(columns={'Dividends': f'Div-{ticker}'}, inplace=True)

    # Process Merged Data

    # Sort the new dataframe by date
    df_merged = df_merged.sort_values(by='Date')

    # Reset the index of the dataframe without adding a column
    df_merged = df_merged.reset_index(drop=True)

    # Sum owned shared from traded shares
    df_merged[f'Shares Owned-{ticker}'] = df_merged[f'Traded-{ticker}'].cumsum()

    # Sum total paid for the shares from paid
    df_merged[f'Total Invested-{ticker}'] = df_merged[f'Trade Cost-{ticker}'].cumsum()

    # convert NaN to value from row above
    df_merged[f'Shares Owned-{ticker}'].fillna(method='pad', inplace=True)
    df_merged[f'Total Invested-{ticker}'].fillna(method='pad', inplace=True)

    # Create a new column and get close price x quantity owned.
    df_merged[f'Value-{ticker}'] = df_merged[f'Close-{ticker}'] * df_merged[f'Shares Owned-{ticker}']

    # Create a new column for returns.
    df_merged[f'Returns-{ticker}'] = df_merged[f'Value-{ticker}'] - df_merged[f'Total Invested-{ticker}']
    df_merged[f'Returns %-{ticker}'] = df_merged[f'Returns-{ticker}'] / df_merged[f'Total Invested-{ticker}'] * 100

    # Calculate value of dividends paid.
    df_merged[f'Div Paid-{ticker}'] = df_merged[f'Div-{ticker}'] * df_merged[f'Shares Owned-{ticker}']

    # Sum total dividends received
    df_merged[f'Total Div-{ticker}'] = df_merged[f'Div Paid-{ticker}'].cumsum()
    df_merged[f'Total Div-{ticker}'].fillna(method='pad', inplace=True)

    # Drop all rows without a stock price to give continuous data
    df_merged.dropna(axis=0, subset=[f'Close-{ticker}'], inplace=True)

    # Reset the index of the dataframe without adding a column
    df_merged = df_merged.reset_index(drop=True)

    df_merged = df_merged.drop(df_merged.columns[[5, 6, 7, 8, 9]], axis=1)

    df_merged_value = pd.merge(df_merged_value, df_merged, how='outer')
    df_merged_value.drop_duplicates(inplace=True)

# Sort the new dataframe by date
# df_merged_value.sort_values(by='Date', inplace=True)
# Reset the index of the dataframe without adding a column
# df_merged_value.reset_index(drop=True, inplace=True)


value_tickers = ['Value-' + sub for sub in portfolio.tickers]
invested_tickers = ['Total Invested-' + sub for sub in portfolio.tickers]
df_merged_value['Total Value'] = df_merged_value[value_tickers].sum(axis=1)
df_merged_value['Total Invested'] = df_merged_value[invested_tickers].sum(axis=1)
df_merged_value['Returns'] = df_merged_value['Total Value'] - df_merged_value['Total Invested']
df_merged_value['Returns %'] = df_merged_value['Returns'] / df_merged_value['Total Invested']*100
div_tickers = ['Total Div-' + sub for sub in portfolio.tickers]
df_merged_value['Portfolio Div'] = df_merged_value[div_tickers].sum(axis=1)

df_merged_value.to_csv(f'{c.root_path}3merged_value.csv')
