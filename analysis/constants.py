import pandas as pd
import datetime
import analysis.gui

df_inputs = pd.read_csv('c:\\python\\stocks\\Portfolio Input\\Inputs.csv')
df_inputs = df_inputs.drop(df_inputs.columns[[0]], axis=1)

root_path = df_inputs.iloc[0, 1]
portfolio_path = df_inputs.iloc[1, 1]
portfolio_file = df_inputs.iloc[2, 1]
output_path = df_inputs.iloc[3, 1]
# start_date = datetime.datetime.now() - datetime.timedelta(days=365*18)  # Start date is 18 years ago, redefined in Portfolio tab.
start_delay = 30  # Start timeline xx days before earliest portfolio acquisition
end_date = datetime.date.today() - datetime.timedelta(days=0)  # End date is today
refresh_tickers = df_inputs.iloc[4, 1]
refresh_dividends = df_inputs.iloc[5, 1]
portfolio_plot = df_inputs.iloc[6, 1]
individual_plot = df_inputs.iloc[7, 1]
df_portfolio = pd.read_csv(f'{portfolio_path}{portfolio_file}')
