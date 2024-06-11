import streamlit as st
from datetime import datetime, date
import quantstats as qs
import streamlit.components.v1 as components
from modules import qs_functions_v5 as qsf
import time


# extend pandas functionality with metrics, etc.
qs.extend_pandas()

st.set_page_config(page_title='QuantStats', layout='wide', page_icon=':🎰:')

# Initialize session_state if it doesn't exist
if 'page' not in st.session_state:
    st.session_state['page'] = ''

# create a text input for the stock symbol in the sidebar
symbol = st.sidebar.text_input("Enter a stock symbol", "MSFT")

# Add a sidebar title
st.sidebar.title('Dates')

# Add a date input widget in the sidebar
end_date = date.today()
start_date = datetime.strptime('1985-01-01', '%Y-%m-%d').date() # set to 1/1/1985
start_date = st.sidebar.date_input('Start date', start_date, min_value=start_date, max_value=end_date)
end_date = st.sidebar.date_input('End date', end_date, min_value=start_date, max_value=end_date)

# create a "Strategy Tearsheet" button in the sidebar
if st.sidebar.button('Snapshot'):
    st.session_state['page'] = 'Snapshot'

# Add a button for graphs
if st.sidebar.button('Custom Report'):
    st.session_state['page'] = 'Custom Report'

# Define start_str and end_str
start_str = start_date.strftime('%Y-%m-%d')
end_str = end_date.strftime('%Y-%m-%d')

time.sleep(.5)
# fetch the daily returns for a stock
stock = qs.utils.download_returns(symbol)

spy_data = spy_data = qs.utils.download_returns('SPY')

# Filter the returns for the selected date range
stock = stock.loc[start_str:end_str]

# Reconstruct the price data from the returns
price = (1 + stock).cumprod()


if st.session_state['page'] == 'Custom Report':
    # Define the options for the multi-select dropdown menu
    options = ['Daily Returns', 'Daily Returns Distribution', 'Drawdown', 'Drawdowns Periods', 'Earnings', 'Monthly Distribution', 'Log Returns', 'Monthly Heatmap', 'Monthly Returns', 'Rolling Sharpe', 'Rolling Sortino', 'Rolling Volatility', 'Yearly Returns']

    selected_options = st.sidebar.multiselect('Select the graphs you want to display:', options)

    # Initialize a list to keep track of which column is free
    columns = []
    free_column_index = 0

    for option in selected_options:
        fig = None
        if option == 'Monthly Heatmap':
            fig = qsf.plot_monthly_heatmap(stock)
            # Display the chart in the main column
            st.plotly_chart(fig)
            continue

        # create 2 columns
        if free_column_index == 0:
            columns = st.columns(2)

        if option == 'Daily Returns':
            fig = qsf.plot_daily_returns(stock)
        elif option == 'Daily Returns Distribution':
            fig = qsf.plot_distribution(stock)
        elif option == 'Drawdown':
            fig = qsf.plot_drawdown(stock)
        elif option == 'Drawdowns Periods':
            fig = qsf.plot_drawdowns_periods(stock)
        elif option == 'Earnings':
            fig = qsf.plot_earnings(stock)
        elif option == 'Monthly Distribution':
            fig = qsf.plot_monthly_dist(stock)
        elif option == 'Log Returns':
            fig = qsf.plot_log_returns(stock)
        elif option == 'Monthly Returns':
            fig = qsf.plot_returns(stock)
        elif option == 'Rolling Sharpe':
            fig = qsf.plot_rolling_sharpe(stock)
        elif option == 'Rolling Sortino':
            fig = qsf.plot_rolling_sortino(stock)
        elif option == 'Rolling Volatility':
            fig = qsf.plot_rolling_volatility(stock)
        elif option == 'Yearly Returns':
            fig = qsf.plot_yearly_returns(stock)

        if fig is not None:
            # Display the figure in the first free column
            columns[free_column_index].plotly_chart(fig)
            # Switch to the next column for the next figure
            free_column_index = (free_column_index + 1) % 2
            if free_column_index == 0:
                columns = []

elif st.session_state['page'] == 'Snapshot':
    # Save the output of qs.reports.html(stock) to a file
    qs.reports.html(stock, output="NTAI_Project_Docs/quantstats-tearsheet.html")

    # Read the HTML file
    with open("NTAI_Project_Docs/quantstats-tearsheet.html", 'r', encoding='utf-8') as f:
        html_string = f.read()

    # Display the HTML string in the Streamlit app
    components.html(html_string, width=1080, height=4000, scrolling=True)