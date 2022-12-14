# import datetime
from tkinter import *
from tkinter.ttk import Combobox
import pandas as pd

# Read defaults from existing file.
df_inputs = pd.read_csv('c:\\python\\stocks\\Portfolio Input\\Inputs.csv')
# Delete the old index column
df_inputs = df_inputs.drop(df_inputs.columns[[0]], axis=1)

# Extract default values from csv file
root_path_default = df_inputs.iat[0, 1]
portfolio_path_default = df_inputs.iat[1, 1]
portfolio_file_default = df_inputs.iat[2, 1]
output_path_default = df_inputs.iat[3, 1]
refresh_tickers_default = df_inputs.iat[4, 1]
refresh_dividends_default = df_inputs.iat[5, 1]
portfolio_plot_default = df_inputs.iat[6, 1]
individual_plot_default = df_inputs.iat[7, 1]

"""input_data = [['root_path', 'c:\\python\\stocks\\'],
              ['portfolio_path', 'c:\\python\\stocks\\PortfolioInput\\'],
              ['portfolio_file', 'portfolio - Dividend.csv'],
              ['output_path', 'c:\\python\\stocks\\PortfolioOutput\\'],
              ['refresh_tickers', 'Yes'],
              ['refresh_dividends', 'Yes'],
              ['portfolio_plot', 'Yes'],
              ['individual_plot', 'Yes']
              ]"""

background_color = '#eae6ff'
text_color = '#000000'

root = Tk()
root.title('Data Entry')
root.geometry('950x450+300+200')
root.resizable(False, False)
root.configure(bg=background_color)


def execute():
    root_path = root_path_entry.get()
    portfolio_path = portfolio_path_entry.get()
    portfolio_file = portfolio_file_entry.get()
    output_path = output_path_entry.get()
    refresh_tickers = refresh_tickers_entry.get()
    refresh_dividends = refresh_dividends_entry.get()
    portfolio_plot = portfolio_plot_entry.get()
    individual_plot = individual_plot_entry.get()

    df_inputs.iat[0, 1] = root_path
    df_inputs.iat[1, 1] = portfolio_path
    df_inputs.iat[2, 1] = portfolio_file
    df_inputs.iat[3, 1] = output_path
    df_inputs.iat[4, 1] = refresh_tickers
    df_inputs.iat[5, 1] = refresh_dividends
    df_inputs.iat[6, 1] = portfolio_plot
    df_inputs.iat[7, 1] = individual_plot

    df_inputs.to_csv(f'C:\\Python\\stocks\\Portfolio Input\\Inputs.csv')
    root.destroy()
    return


# Labels
x_align_label = 20
Label(root, text='Stocks Project Folder Path (root):', font=23, bg=background_color, fg=text_color).place(x=x_align_label, y=20)
Label(root, text='Portfolio Folder Name:', font=23, bg=background_color, fg=text_color).place(x=x_align_label, y=70)
Label(root, text='Portfolio File Name:', font=23, bg=background_color, fg=text_color).place(x=x_align_label, y=120)
Label(root, text='Output Folder Name:', font=23, bg=background_color, fg=text_color).place(x=x_align_label, y=170)
Label(root, text='Refresh Tickers?', font=23, bg=background_color, fg=text_color).place(x=x_align_label, y=220)
Label(root, text='Refresh Dividends?', font=23, bg=background_color, fg=text_color).place(x=x_align_label, y=270)
Label(root, text='Generate portfolio plot?', font=23, bg=background_color, fg=text_color).place(x=x_align_label, y=320)
Label(root, text='Generate individual stock plots?', font=23, bg=background_color, fg=text_color).place(x=x_align_label, y=370)

# Entry
root_path = StringVar()
portfolio_path = StringVar()
portfolio_file = StringVar()
output_path = StringVar()

root_path_entry = Entry(root, textvariable=root_path, width=45, bd=2, font=20)
portfolio_path_entry = Entry(root, textvariable=portfolio_path, width=45, bd=2, font=20)
portfolio_file_entry = Entry(root, textvariable=portfolio_file, width=45, bd=2, font=20)
output_path_entry = Entry(root, textvariable=output_path, width=45, bd=2, font=20)
refresh_tickers_entry = Combobox(root, values=['Yes', 'No'], width=45, state='r', font='arial 14')
refresh_dividends_entry = Combobox(root, values=['Yes', 'No'], width=45, state='r', font='arial 14')
portfolio_plot_entry = Combobox(root, values=['Yes', 'No'], width=45, state='r', font='arial 14')
individual_plot_entry = Combobox(root, values=['Yes', 'No'], width=45, state='r', font='arial 14')

# Default values read from .csv file
root_path_entry.insert(0, root_path_default)
portfolio_path_entry.insert(0, portfolio_path_default)
portfolio_file_entry.insert(0, portfolio_file_default)
output_path_entry.insert(0, output_path_default)
refresh_tickers_entry.set(refresh_tickers_default)
refresh_dividends_entry.set(refresh_dividends_default)
portfolio_plot_entry.set(portfolio_plot_default)
individual_plot_entry.set(individual_plot_default)

x_align_entry = 350
root_path_entry.place(x=x_align_entry, y=20)
portfolio_path_entry.place(x=x_align_entry, y=70)
portfolio_file_entry.place(x=x_align_entry, y=120)
output_path_entry.place(x=x_align_entry, y=170)
refresh_tickers_entry.place(x=x_align_entry, y=220)
refresh_dividends_entry.place(x=x_align_entry, y=270)
portfolio_plot_entry.place(x=x_align_entry, y=320)
individual_plot_entry.place(x=x_align_entry, y=370)

Button(root, text='Run', bg='#326273', fg='white', width=15, height=2, command=execute).place(x=20, y=400)

# start_delay = 30  # Start timeline xx days before earliest portfolio acquisition
# end_date = datetime.date.today() - datetime.timedelta(days=0)  # End date is today

root.mainloop()


# Add an icon to data entry form
#icon_image=PhotoImage(file='logo.png')
#root.iconphoto(False, icon_image)
