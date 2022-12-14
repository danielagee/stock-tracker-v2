class PortfolioStackedPlot:
    import plotly.graph_objects as go
    import analysis.portfolio as portfolio
    import analysis.constants as c
    import pandas as pd

    df_merged = pd.read_csv(f'{c.root_path}3merged_value.csv')

    # Create Plot
    fig = go.Figure()

    for ticker in portfolio.tickers:
        fig.add_trace(go.Scatter(
            name=f'{ticker}',
            x=df_merged['Date'],
            y=df_merged[f'Value-{ticker}'],
            stackgroup='one'
        ))

    fig.show()




