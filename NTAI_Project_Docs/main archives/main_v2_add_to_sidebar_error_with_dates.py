import streamlit as st
from datetime import date
from datetime import datetime
import matplotlib.pyplot as plt
import quantstats as qs
import pandas as pd
import yfinance as yf

# extend pandas functionality with metrics, etc.
qs.extend_pandas()

st.set_page_config(page_title='QuantStats',  layout='wide', page_icon=':🎰:')

# Suppose you have a date string
date_str = '2022-01-01'

# Convert it to a datetime object
date_obj = datetime.strptime(date_str, '%Y-%m-%d')

# Now you can use strftime on date_obj
formatted_str = date_obj.strftime('%Y-%m-%d')

# create a "Home" button in the sidebar
if st.sidebar.button('Home'):
    st.sidebar.write('You clicked the home button')

# create a text input for the stock symbol in the sidebar
symbol = st.sidebar.text_input("Enter a stock symbol", "MSFT")

# Add a sidebar title
st.sidebar.title('Select Date Range')

# Add a date input widget in the sidebar
start_date = st.sidebar.date_input('Start date', date(2021, 1, 1))
end_date = st.sidebar.date_input('End date', date(2021, 12, 31))

# Define start_str and end_str
start_str = start_date.strftime('%Y-%m-%d')
end_str = end_date.strftime('%Y-%m-%d')

def fetch_data(start_date, end_date):
    # Assuming 'symbol' is defined elsewhere in your code
    global symbol
    # Convert start_date and end_date to string format expected by yfinance
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    # Fetch the stock price data
    data = yf.download(symbol, start=start_str, end=end_str)
    return data

# Fetch the stock price data between start_date and end_date
# You'll need to implement the fetch_data function
data = fetch_data(start_str, end_str)

# Add a button in the sidebar
if st.sidebar.button('Fetch Data'):
    # create 2 columns
    col1, col2 = st.columns(2)
    
    # plot the stock price performance in the first column
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data['Close'])
    ax.set_title('Stock Price Performance')
    col1.pyplot(fig)
    plt.clf()  # Clear the current figure

    # fetch the daily returns for a stock
    stock = qs.utils.download_returns(symbol)

    # plot the returns in the second column
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(stock)
    ax.set_title('Returns')
    col2.pyplot(fig)
    plt.clf()  # Clear the current figure

    # plot the monthly returns in the third column
    monthly_returns = stock.resample('ME').apply(qs.stats.comp)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_returns)
    ax.set_title('Monthly Returns')
    col1.pyplot(fig)
    plt.clf()  # Clear the current figure
    
