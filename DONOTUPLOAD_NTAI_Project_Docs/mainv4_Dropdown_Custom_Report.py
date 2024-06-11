import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
import quantstats as qs
import pandas as pd
import streamlit as st
import plotly.tools as tls
import numpy as np
import streamlit.components.v1 as components
from datetime import date, timedelta
from NTAI_Project_Docs.modules import qs_functions_old as qsf

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
end_date = date.today()
start_date = end_date - timedelta(days=5*365)  # 5 years ago
start_date = st.sidebar.date_input('Start date', start_date)
end_date = st.sidebar.date_input('End date', end_date)

# create a "Strategy Tearsheet" button in the sidebar
if st.sidebar.button('Strategy Tearsheet'):
    st.session_state['page'] = 'Strategy Tearsheet'

# Add a button for graphs
if st.sidebar.button('Custom Report'):
    st.session_state['page'] = 'Custom Report'

# Define start_str and end_str
start_str = start_date.strftime('%Y-%m-%d')
end_str = end_date.strftime('%Y-%m-%d')

# fetch the daily returns for a stock
stock = qs.utils.download_returns(symbol)

# Filter the returns for the selected date range
stock = stock.loc[start_str:end_str]

# Reconstruct the price data from the returns
price = (1 + stock).cumprod()

if st.session_state['page'] == 'Custom Report':
    # create 2 columns
    col1, col2 = st.columns(2)
    # Define the options for the multi-select dropdown menu
    options = ['Stock Price Performance', 'Returns', 'Monthly Returns', 'Average Monthly Returns', 'Expected Returns' ]
    # Create the multi-select dropdown menu in the sidebar
    selected_options = st.sidebar.multiselect('Select the graphs you want to display:', options)

    # Check if each graph's name is in the selected options before plotting it
    if 'Stock Price Performance' in selected_options:
        qsf.stock_price_performance(price, col1)

    if 'Returns' in selected_options:
        qsf.returns(stock, col2)

    if 'Monthly Returns' in selected_options:
        qsf.monthly_returns(stock, col1)

    if 'Average Monthly Returns' in selected_options:
        qsf.average_monthly_returns(stock, col2)
    
    if 'Expected Returns' in selected_options:
        qsf.expected_returns(stock, col1)

elif st.session_state['page'] == 'Strategy Tearsheet':
    # Save the output of qs.reports.html(stock) to a file
    qs.reports.html(stock, output="NTAI_Project_Docs/quantstats-tearsheet.html")

    # Read the HTML file
    with open("NTAI_Project_Docs/quantstats-tearsheet.html", 'r', encoding='utf-8') as f:
        html_string = f.read()

    # Display the HTML string in the Streamlit app
    components.html(html_string, width=1080, height=4000, scrolling=True)

