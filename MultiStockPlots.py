import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# portfolio_path = 'C:\\Python\\PythonProjects\\stock-tracker-v2\\cvs files\\Input Files\\'
# portfolio_file = 'Portfolio - FAANG.csv'
portfolio_path = 'C:\\Python\\stocks\\Portfolio Input\\'
portfolio_file = 'Portfolio - DMA.csv'
output_path = 'C:\\Python\\stocks\\Portfolio Output\\'
#output_path = 'C:\\Python\\PythonProjects\\stock-tracker-v2\\cvs files\\Output Files\\'

df_sp500 = pd.read_csv(f'{output_path}^GSPC.csv')

df = pd.read_csv(f'{output_path}merged_value.csv')

# Create sub-plot
fig = make_subplots(rows=2, cols=1, row_heights=[0.8, 0.2], subplot_titles=("Portfolio Value", "Portfolio Returns"))
fig.update_xaxes(title_text="Date", row=1, col=1)
fig.update_xaxes(title_text="Date", row=2, col=1)
fig.update_yaxes(title_text="Portfolio Invested & Value (USD)", row=1, col=1)
fig.update_yaxes(title_text="Return on Investment (%)", row=2, col=1)

# Line plot for total investments.
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Total Invested'],
    line=dict(color='#EE4B2B'),
    name="Total Investments"),
    row=1, col=1)

# Line plot for portfolio value.
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Total Value'],
    line=dict(color='#ADD8E6'),
    name="Total Portfolio Value"),
    row=1, col=1)

"""# Line plot for total dividends.
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Portfolio Div'],
    line=dict(color='#228C22'),
    name="Total Portfolio Dividends"),
    row=1, col=1)"""

# Sub plot for returns

"""# Returns shaded plot
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=np.maximum(0, df['Returns %']*100),
    marker=dict(size=0),
    line=(dict(color='#046307')),
    fill='tozeroy',
    name="Returns %"),
    row=2, col=1)"""

"""# Filter green channel. Accept all values >0, and all <0 become 0.
df[f'Returns %-Gains'] = df[f'Returns %'].where(
    df[f'Returns %'] > 0, 0)
# Filter red channel. Accept all values <0, and all >0 become 0.
df[f'Returns %-Losses'] = df[f'Returns %'].mask(
    df[f'Returns %'] > 0, 0)

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
