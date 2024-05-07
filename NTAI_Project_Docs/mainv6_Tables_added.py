import streamlit as st
from datetime import datetime, date
import quantstats as qs
import streamlit.components.v1 as components
from modules import qs_functions as qsf
import time
from st_aggrid import AgGrid


# extend pandas functionality with metrics, etc.
qs.extend_pandas()

st.set_page_config(page_title='QuantStats', layout='wide', page_icon=':🎰:')

# Initialize session_state if it doesn't exist
if 'page' not in st.session_state:
    st.session_state['page'] = 'Snapshot'

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
if 'stock' not in st.session_state or 'symbol' not in st.session_state or st.session_state['symbol'] != symbol:
    st.session_state['stock'] = qs.utils.download_returns(symbol)
    st.session_state['symbol'] = symbol

stock = st.session_state['stock']

spy_data = spy_data = qs.utils.download_returns('SPY')

# Filter the returns for the selected date range
stock = stock.loc[start_str:end_str]

# Reconstruct the price data from the returns
price = (1 + stock).cumprod()


if st.session_state['page'] == 'Custom Report':
    # Define the options for the multi-select dropdown menu
    options = ['Daily Returns Graph', 'Daily Returns Table', 'Daily Returns Distribution Graph', 'Drawdown Graph', 'Drawdown Table', 'Drawdowns Periods Graph', 'Drawdowns Periods Table', 'Earnings Graph', 'Earnings Table', 'Monthly Distribution Graph',  'Log Returns Graph', 'Monthly Heatmap Graph', 'Monthly Returns Graph', 'Monthly Returns Table', 'Rolling Sharpe Graph', 'Rolling Sharpe Table', 'Rolling Sortino Graph', 'Rolling Sortino Table', 'Rolling Volatility Graph', 'Rolling Volatility Table', 'Yearly Returns Graph', 'Yearly Returns Table']
    selected_options = st.sidebar.multiselect('Select the graphs and tables you want to display:', options)

    # Map option names to their corresponding functions
    graph_functions = {
        'Daily Returns Graph': qsf.plot_daily_returns,
        'Daily Returns Distribution Graph': qsf.plot_distribution,
        'Drawdown Graph': qsf.plot_drawdown,
        'Drawdowns Periods Graph': qsf.plot_drawdowns_periods,
        'Earnings Graph': qsf.plot_earnings,
        'Monthly Distribution Graph': qsf.plot_monthly_dist,
        'Log Returns Graph': qsf.plot_log_returns,
        'Monthly Heatmap Graph': qsf.plot_monthly_heatmap,
        'Monthly Returns Graph': qsf.plot_returns,
        'Rolling Sharpe Graph': qsf.plot_rolling_sharpe,
        'Rolling Sortino Graph': qsf.plot_rolling_sortino,
        'Rolling Volatility Graph': qsf.plot_rolling_volatility,
        'Yearly Returns Graph': qsf.plot_yearly_returns
    }

    table_functions = {
        'Daily Returns Table': qsf.table_daily_returns,
        'Drawdown Table': qsf.table_drawdown,
        'Drawdowns Periods Table': qsf.table_drawdowns_periods,
        'Earnings Table': qsf.table_earnings,
        'Monthly Returns Table': qsf.table_returns,
        'Rolling Sharpe Table': qsf.table_rolling_sharpe,
        'Rolling Sortino Table': qsf.table_rolling_sortino,
        'Rolling Volatility Table': qsf.table_rolling_volatility,
        'Yearly Returns Table': qsf.table_yearly_returns
    }

    # Initialize a list to keep track of which column is free
    columns = []
    free_column_index = 0

    for option in selected_options:
        # If the option is 'Monthly Heatmap Graph', display it in a full-width container
        if option == 'Monthly Heatmap Graph':
            fig = graph_functions[option](stock)
            if fig is not None:
                st.plotly_chart(fig)
            continue  # Skip the rest of the loop

        # Always create 2 columns
        if free_column_index == 0:
            columns = st.columns(2)

        # Generate and display the graph or table
        if option in graph_functions:
            fig = graph_functions[option](stock)
            if fig is not None:
                columns[free_column_index].plotly_chart(fig)
        elif option in table_functions:
            df = table_functions[option](stock)
            if df is not None:
                # Generate column definitions based on DataFrame columns
                column_defs = [{'headerName': col, 'field': col, 'filter': True} for col in df.columns]

                gridOptions={
                    'columnDefs': column_defs,
                    'defaultColDef': {'flex': 1},
                    'fit_columns_on_grid_load': True,
                }
                with columns[free_column_index].container():
                    st.markdown(f"###### **{option}**")  # Add a title to the table
                    AgGrid(df, gridOptions=gridOptions)

        # Switch to the next column for the next figure or table
        free_column_index = (free_column_index + 1) % 2

elif st.session_state['page'] == 'Snapshot':
        # Save the output of qs.reports.html(stock) to a file
    qs.reports.html(stock, output="NTAI_Project_Docs/quantstats-tearsheet.html")

        # Read the HTML file
    with open("NTAI_Project_Docs/quantstats-tearsheet.html", 'r', encoding='utf-8') as f:
            html_string = f.read()

    # Display the HTML string in the Streamlit app
    components.html(html_string, width=1080, height=4000, scrolling=True)