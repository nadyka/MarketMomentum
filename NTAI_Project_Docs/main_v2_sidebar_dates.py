import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
import quantstats as qs
import pandas as pd
import yfinance as yf

# extend pandas functionality with metrics, etc.
qs.extend_pandas()

st.set_page_config(page_title='QuantStats',  layout='wide', page_icon=':🎰:')

# create a "Home" button in the sidebar
if st.sidebar.button('Home'):
    st.sidebar.write('You clicked the home button')

# create a text input for the stock symbol in the sidebar
symbol = st.sidebar.text_input("Enter a stock symbol", "MSFT")

# Add a sidebar title
st.sidebar.title('Select Date Range')

# Add a date input widget in the sidebar
start_date = st.sidebar.date_input('Start date', date(2020, 1, 1))
end_date = st.sidebar.date_input('End date', date(2022, 12, 31))

# Add a button to confirm the selected dates
if st.sidebar.button('Confirm selected dates'):
    # Define start_str and end_str
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    # fetch the stock price data
    data = yf.download(symbol, start=start_str, end=end_str)

    # create 2 columns
    col1, col2 = st.columns(2)

    # plot the stock price performance in the first column
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data['Close'])
    ax.set_title('Stock Price Performance')
    col1.pyplot(fig)
    plt.clf()  # Clear the current figure

    # fetch the daily returns for a stock
    stock = data['Close'].pct_change().dropna()

    # plot the returns in the second column
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(stock)
    ax.set_title('Returns')
    col2.pyplot(fig)
    plt.clf()  # Clear the current figure

    # plot the monthly returns in the first column
    monthly_returns = stock.resample('M').apply(qs.stats.comp)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_returns)
    ax.set_title('Monthly Returns')
    col1.pyplot(fig)
    plt.clf()  # Clear the current figure