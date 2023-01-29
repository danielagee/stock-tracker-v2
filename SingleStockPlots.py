import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

#portfolio_path = 'C:\\Python\\PythonProjects\\stock-tracker-v2\\cvs files\\Input Files\\'
#portfolio_file = 'Portfolio - FAANG.csv'
portfolio_path = 'C:\\Python\\stocks\\Portfolio Input\\'
portfolio_file = 'Portfolio - DMA.csv'
output_path = 'C:\\Python\\PythonProjects\\stock-tracker-v2\\cvs files\\Output Files\\'

df_sp500 = pd.read_csv(f'{output_path}^GSPC.csv')


def tickers_list(in_path, file):
    df_pe = pd.read_csv(f'{in_path}{file}')
    df_pe = df_pe.Ticker.unique()  # Convert the stocks in the portfolio to a list of tickers
    return df_pe  # Convert the stocks in the portfolio to a list of tickers


tickers = tickers_list(portfolio_path, portfolio_file)

for ticker in tickers:
    fig = make_subplots(rows=2, cols=1, row_heights=[0.8, 0.2],
                        specs=[[{"secondary_y": True}],
                               [{"secondary_y": True}]],
                        subplot_titles=(f'{ticker} Overview', ''))
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Stock Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text=f'Value Performance of {ticker} vs S&P 500', secondary_y=True, row=1, col=1)
    #fig.update_yaxes(title_text='Dividends Received (USD)', row=2, col=1)
    fig.update_yaxes(title_text=f'Returns %', secondary_y=False, row=2, col=1)
    fig.update_layout(xaxis_rangeslider_visible=False)

    df = pd.read_csv(f'{output_path}{ticker}.csv')

    # Basic candlestick plot using date, open, high, low, and close.
    fig.add_trace(
        go.Candlestick(x=df['Date'],
                       open=df[f'Open'],
                       high=df[f'High'],
                       low=df[f'Low'],
                       close=df[f'Close'],
                       name=f'{ticker}'),
        secondary_y=False, row=1, col=1)

    # Plot the moving averages as new traces on the plotly chart.
    # !!!!!!!!!!!!! Need to update hard coded moving average titles
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['21-dma'],
                   line=dict(color='#a098ed'),
                   name="21-Day-MA"),
        secondary_y=False, row=1, col=1)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['50-dma'],
                   line=dict(color='#2c19d4'),
                   name="50-Day-MA"),
        secondary_y=False, row=1, col=1)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['200-dma'],
                   line=dict(color='#2c1aaa'),
                   name="200-Day-MA"),
        secondary_y=False, row=1, col=1)

    """"# Add trace for relative valuation compared to S&P500 index.
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['^GSPC_rel'],
                   line=dict(color='#ADD8E6'),
                   name="Rel-Value-SP500"),
        secondary_y=True, row=1, col=1)"""

    """# Add trace for relative % valuation compared to S&P500 index.
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['^GSPC_rel_%'],
                   line=dict(color='#ADD8E6'),
                   name="%Rel-Value-SP500"),
        secondary_y=True, row=1, col=1)"""

    """# Add trace for total returns.
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df[f'Returns'],
                   line=dict(color='#fc0303'),
                   name=f'Returns'),
        secondary_y=False, row=2, col=1)"""

    # Add trace for total dividends received.
    """fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df[f'Total Div'],
                   line=dict(color='#0da80d'),
                   name=f'Dividends'),
        secondary_y=False, row=2, col=1)"""

    # Add trace for total returns %.
    """fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df[f'Returns %'],
                   line=dict(color='#b0218f'),
                   name=f'Returns %'),
        secondary_y=True, row=2, col=1)"""

    """ # !!!!!!!!!!!!!! Add calculations for returns
    # Filter green channel. Accept all values >0, and all <0 become 0.
    df[f'Returns %-Gains'] = df[f'Returns %'].where(df[f'Returns %'] > 0, 0)
    # Filter red channel. Accept all values <0, and all >0 become 0.
    df[f'Returns %-Losses'] = df[f'Returns %'].mask(df[f'Returns %'] > 0, 0)

    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df[f'Returns %-Gains'],
                   mode='none',  # Remove line formatting and just show shading.
                   name="Returns %",
                   fill='tozeroy',
                   fillcolor='green'),
        secondary_y=False, row=2, col=1)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df[f'Returns %-Losses'],
                   mode='none',  # Remove line formatting and just show shading.
                   fill='tozeroy',
                   showlegend=False,  # Remove legend entry for this series so it doesn't duplicate.
                   fillcolor='red'),
        secondary_y=False, row=2, col=1)
    """

    fig.show()
