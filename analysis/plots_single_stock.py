class PortfolioSinglePlots:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import analysis.portfolio as portfolio
    import analysis.constants as c
    import pandas as pd

    df_merged = pd.read_csv(f'{c.root_path}3merged_value.csv')
    df_sp500 = pd.read_csv(f'{c.output_path}sp500.csv')

    def moving_average(df_merged, ticker, window):
        # Calculate the moving average from closing price and a defined duration
        df_merged[f'{window}dma'] = df_merged[f'Close-{ticker}'].rolling(window=window).mean()

    for ticker in portfolio.tickers:
        moving_average(df_merged, ticker, 21)
        moving_average(df_merged, ticker, 200)

        # df_merged['sp500_rel'] = df_merged[f'Close-{ticker}'] / df_sp500['Close']
        df_merged['sp500_rel_%'] = (df_merged[f'Close-{ticker}'] / df_merged[f'Close-{ticker}'].iat[0]) / \
                                   (df_sp500['Close'] / df_sp500['Close'].iat[0])

        # Create dual plot figure with secondary y-axis
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

        # Basic candlestick plot using date, open, high, low, and close.
        fig.add_trace(
            go.Candlestick(x=df_merged['Date'],
                           open=df_merged[f'Open-{ticker}'],
                           high=df_merged[f'High-{ticker}'],
                           low=df_merged[f'Low-{ticker}'],
                           close=df_merged[f'Close-{ticker}'],
                           name=f'{ticker}'),
            secondary_y=False, row=1, col=1)

        # Plot the 21 and 200 day moving averages as new traces on the plotly chart.
        fig.add_trace(
            go.Scatter(x=df_merged['Date'],
                       y=df_merged['21dma'],
                       line=dict(color='#a098ed'),
                       name="21-Day-MA"),
            secondary_y=False, row=1, col=1)
        fig.add_trace(
            go.Scatter(x=df_merged['Date'],
                       y=df_merged['200dma'],
                       line=dict(color='#2c19d4'),
                       name="200-Day-MA"),
            secondary_y=False, row=1, col=1)

        """# Add trace for relative valuation compared to S&P500 index.
        fig.add_trace(
            go.Scatter(x=df_merged['Date'],
                       y=df_merged['sp500_rel'],
                       line=dict(color='#ADD8E6'),
                       name="Rel-Value-SP500"),
            secondary_y=True, row=1, col=1)"""

        # Add trace for relative % valuation compared to S&P500 index.
        fig.add_trace(
            go.Scatter(x=df_merged['Date'],
                       y=df_merged['sp500_rel_%'],
                       line=dict(color='#ADD8E6'),
                       name="Rel-Value-SP500"),
            secondary_y=True, row=1, col=1)

        """
        # Add trace for total returns.
        fig.add_trace(
            go.Scatter(x=df_merged['Date'],
                       y=df_merged[f'Returns-{ticker}'],
                       line=dict(color='#fc0303'),
                       name=f'Returns-{ticker}'),
            secondary_y=False, row=2, col=1)

        # Add trace for total dividends received.
        fig.add_trace(
            go.Scatter(x=df_merged['Date'],
                       y=df_merged[f'Total Div-{ticker}'],
                       line=dict(color='#0da80d'),
                       name=f'Dividends-{ticker}'),
            secondary_y=False, row=2, col=1)

        # Add trace for total returns %.
        fig.add_trace(
            go.Scatter(x=df_merged['Date'],
                       y=df_merged[f'Returns %-{ticker}'],
                       line=dict(color='#b0218f'),
                       name=f'Returns %-{ticker}'),
            secondary_y=True, row=2, col=1)"""

        # Filter green channel. Accept all values >0, and all <0 become 0.
        df_merged[f'Returns %-Gains-{ticker}'] = df_merged[f'Returns %-{ticker}'].where(
            df_merged[f'Returns %-{ticker}'] > 0, 0)
        # Filter red channel. Accept all values <0, and all >0 become 0.
        df_merged[f'Returns %-Losses-{ticker}'] = df_merged[f'Returns %-{ticker}'].mask(
            df_merged[f'Returns %-{ticker}'] > 0, 0)

        fig.add_trace(
            go.Scatter(x=df_merged['Date'],
                       y=df_merged[f'Returns %-Gains-{ticker}'],
                       mode='none',  # Remove line formatting and just show shading.
                       name="Returns %",
                       fill='tozeroy',
                       fillcolor='green'),
            secondary_y=False, row=2, col=1)
        fig.add_trace(
            go.Scatter(x=df_merged['Date'],
                       y=df_merged[f'Returns %-Losses-{ticker}'],
                       mode='none',  # Remove line formatting and just show shading.
                       fill='tozeroy',
                       showlegend=False,  # Remove legend entry for this series so it doesn't duplicate.
                       fillcolor='red'),
            secondary_y=False, row=2, col=1)

        fig.show()
