import yfinance as yf
import time
import analysis.constants as c
import analysis.portfolio as portfolio

start_date = portfolio.start_date
end_date = c.end_date

if c.refresh_dividends == "Yes":
    for ticker in portfolio.tickers:
        tic = yf.Ticker(ticker)
        div = tic.dividends

        div.to_csv(f'{c.output_path}div-{ticker}.csv')
        print(f'Ticker Dividends: {ticker}')
        time.sleep(1)
