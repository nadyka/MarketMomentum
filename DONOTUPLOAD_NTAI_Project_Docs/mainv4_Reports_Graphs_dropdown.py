import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
import quantstats as qs
import pandas as pd
import streamlit as st
import plotly.tools as tls
import numpy as np
import streamlit.components.v1 as components

# extend pandas functionality with metrics, etc.
qs.extend_pandas()

st.set_page_config(page_title='QuantStats',  layout='wide', page_icon=':🎰:')

# Initialize session_state if it doesn't exist
if 'page' not in st.session_state:
    st.session_state['page'] = ''

# create a text input for the stock symbol in the sidebar
symbol = st.sidebar.text_input("Enter a stock symbol", "MSFT")

# Add a sidebar title
st.sidebar.title('Dates')

# Add a date input widget in the sidebar
start_date = st.sidebar.date_input('Start date', date(2020, 1, 1))
end_date = st.sidebar.date_input('End date', date(2023, 12, 31))

# create a "Strategy Tearsheet" button in the sidebar
if st.sidebar.button('Strategy Tearsheet'):
    st.session_state['page'] = 'Strategy Tearsheet'

# Add a button for graphs
if st.sidebar.button('Graphs'):
    st.session_state['page'] = 'Graphs'

# Define start_str and end_str
start_str = start_date.strftime('%Y-%m-%d')
end_str = end_date.strftime('%Y-%m-%d')

# fetch the daily returns for a stock
stock = qs.utils.download_returns(symbol)

# Filter the returns for the selected date range
stock = stock.loc[start_str:end_str]

# Reconstruct the price data from the returns
price = (1 + stock).cumprod()

if st.session_state['page'] == 'Graphs':
    # create 2 columns
    col1, col2 = st.columns(2)

    # plot the stock price performance in the first column
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(price)
    ax.set_title('Stock Price Performance')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    col1.pyplot(fig)
    plt.clf()  # Clear the current figure

    # plot the returns in the second column
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(stock)
    ax.set_title('Returns')
    ax.set_xlabel('Date')
    ax.set_ylabel('Returns')
    col2.pyplot(fig)
    plt.clf()  # Clear the current figure

    # plot the monthly returns in the first column
    monthly_returns = stock.resample('ME').apply(qs.stats.comp)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_returns)
    ax.set_title('Monthly Returns')
    ax.set_xlabel('Date')
    ax.set_ylabel('Monthly Returns')
    col1.pyplot(fig)
    plt.clf()  # Clear the current figure

    # Calculate the average monthly returns
    avg_monthly_returns = stock.resample('ME').apply(np.mean)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(avg_monthly_returns)
    ax.set_title('Average Monthly Returns')
    ax.set_xlabel('Date')
    ax.set_ylabel('Average Monthly Returns')
    col2.pyplot(fig)
    plt.clf()  # Clear the current figure

elif st.session_state['page'] == 'Strategy Tearsheet':
    # Save the output of qs.reports.html(stock) to a file
    qs.reports.html(stock, output="NTAI_Project_Docs/quantstats-tearsheet.html")

    # Read the HTML file
    with open("NTAI_Project_Docs/quantstats-tearsheet.html", 'r') as f:
        html_string = f.read()

    # Display the HTML string in the Streamlit app
    components.html(html_string, width=1080, height=4000, scrolling=False)

