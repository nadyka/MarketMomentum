import streamlit as st
from datetime import datetime, date
import quantstats as qs
import streamlit.components.v1 as components
from modules import qs_functions as qsf
import time
from st_aggrid import AgGrid
from datetime import timedelta

# extend pandas functionality with metrics, etc.
qs.extend_pandas()

st.set_page_config(page_title='MarketMomentum', layout='wide', page_icon=':🎰:')

# Initialize session_state if it doesn't exist
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'

if st.session_state['page'] == 'Home':
    st.title("Welcome to MarketMomentum!")
    st.text("To get started, enter a stock symbol and generate your own custom report or see a key metrics snapshot")

elif st.session_state['page'] == 'Snapshot':
    st.title("Snapshot")
    # Rest of the code for Snapshot page

elif st.session_state['page'] == 'Custom Report':
    st.title("Custom Report")
    # Rest of the code for Custom Report page

# create a text input for the stock symbol in the sidebar
symbol = st.sidebar.text_input("Enter a stock symbol", "MSFT")

# Initialize benchmark to None
benchmark = None

# Define benchmark_symbol with a default value
benchmark_symbol = None

# Add a sidebar title
st.sidebar.title('Dates')

# Add a date input widget in the sidebar
current_date = date.today()
default_start_date = current_date - timedelta(days=5*365)  # set default start date to 5 years ago
earliest_date = datetime.strptime('1987-01-01', '%Y-%m-%d').date()  # set selectable date range to start from 1/1/1987
start_date = st.sidebar.date_input('Start date', default_start_date, min_value=earliest_date, max_value=current_date)
end_date = st.sidebar.date_input('End date', current_date, min_value=start_date, max_value=current_date)

# Add a checkbox for including a benchmark
include_benchmark = st.sidebar.checkbox('Include Benchmark')

# If the checkbox is checked, update benchmark_symbol with the user's input
if include_benchmark:
    benchmark_symbol = st.sidebar.text_input("Enter a benchmark symbol", "SPY")

# create a "Snapshot" button in the sidebar
if st.sidebar.button('Snapshot'):
    st.session_state['page'] = 'Snapshot'

# Add a button for custom reports
if st.sidebar.button('Custom Report'):
    st.session_state['page'] = 'Custom Report'

# Define start_str and end_str
start_str = start_date.strftime('%Y-%m-%d')
end_str = end_date.strftime('%Y-%m-%d')

try:
    # fetch the daily returns for a stock
    if 'stock' not in st.session_state or 'symbol' not in st.session_state or st.session_state['symbol'] != symbol:
        st.session_state['stock'] = qs.utils.download_returns(symbol)
        if st.session_state['stock'].empty:
            st.error(f"Ticker {symbol} does not exist.")
            st.stop()
        st.session_state['symbol'] = symbol

    time.sleep(.5)
    # If a benchmark symbol is provided, download the returns for the benchmark
    if benchmark_symbol:
        benchmark = qs.utils.download_returns(benchmark_symbol)
        if benchmark.empty:
            st.error(f"Benchmark ticker {benchmark_symbol} does not exist.")
            st.stop()

        # Filter the benchmark for the selected date range
        benchmark = benchmark.loc[start_str:end_str]

        # Check if the benchmark DataFrame is empty
        if benchmark.empty:
            st.error(f"No data for benchmark {benchmark_symbol} in the specified date range.")
            st.stop()

    stock = st.session_state['stock']
    # Filter the returns for the selected date range
    stock = stock.loc[start_str:end_str]
    # Reconstruct the price data from the returns
    price = (1 + stock).cumprod()

    # Check if the returns DataFrame is empty
    if stock.empty:
        st.error(f"No data for stock {symbol} in the specified date range.")
        st.stop()
except IndexError as e:
    st.error(f"An IndexError occurred: {e}")
    st.stop()
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.stop()

if st.session_state['page'] == 'Custom Report':
    # Define the options for the multi-select dropdown menu
    options = ['Metrics Table', 'Daily Returns Graph', 'Daily Returns Table (%)', 'Daily Returns Distribution Graph', 'Drawdown Graph', 'Drawdowns Periods Graph', 'Drawdowns Periods Table', 'Earnings Graph', 'Daily Earnings Table (%)', 'Monthly Earnings Table (%)','Yearly Earnings Table (%)','Monthly Distribution Graph',  'Log Returns Graph', 'Monthly Heatmap Graph', 'Monthly Returns Graph', 'Monthly Returns Table (%)', 'Rolling Sharpe Graph', 'Rolling Sharpe Table', 'Rolling Sortino Graph', 'Rolling Sortino Table', 'Rolling Volatility Graph', 'Rolling Volatility Table', 'Yearly Returns Graph', 'Yearly Returns Table (%)']
    selected_options = st.sidebar.multiselect('Select the graphs and tables you want to display:', options)
    # Modify the function mappings to pass the benchmark to the functions
    graph_functions = {
                'Daily Returns Graph': lambda stock: qsf.plot_daily_returns(stock, symbol, benchmark, benchmark_symbol),
                'Daily Returns Distribution Graph': lambda stock: qsf.plot_distribution(stock, symbol, benchmark, benchmark_symbol),
                'Drawdown Graph': qsf.plot_drawdown,
                'Drawdowns Periods Graph': qsf.plot_drawdowns_periods,
                'Earnings Graph': lambda stock: qsf.plot_earnings(stock, symbol, benchmark, benchmark_symbol),
                'Monthly Distribution Graph': qsf.plot_monthly_dist,
                'Log Returns Graph': lambda stock: qsf.plot_log_returns(stock, symbol, benchmark, benchmark_symbol),
                'Monthly Heatmap Graph': qsf.plot_monthly_heatmap,
                'Monthly Returns Graph': lambda stock: qsf.plot_returns(stock, symbol, benchmark, benchmark_symbol),
                'Rolling Sharpe Graph': lambda stock: qsf.plot_rolling_sharpe(stock, symbol, benchmark, benchmark_symbol),
                'Rolling Sortino Graph': lambda stock: qsf.plot_rolling_sortino(stock, symbol, benchmark, benchmark_symbol),
                'Rolling Volatility Graph': lambda stock: qsf.plot_rolling_volatility(stock, symbol, benchmark, benchmark_symbol),
                'Yearly Returns Graph': lambda stock: qsf.plot_yearly_returns(stock, symbol, benchmark, benchmark_symbol)
            }

    table_functions = {
                'Daily Returns Table (%)': lambda stock: qsf.table_daily_returns(stock, symbol, benchmark_symbol, benchmark),
                'Drawdowns Periods Table': qsf.table_drawdowns_periods,
                'Daily Earnings Table (%)': lambda stock: qsf.table_earnings(stock, symbol, benchmark_symbol, benchmark),
                'Monthly Earnings Table (%)': lambda stock: qsf.table_monthly_earnings(stock, symbol, benchmark_symbol, benchmark),
                'Yearly Earnings Table (%)': lambda stock: qsf.table_yearly_earnings(stock, symbol, benchmark_symbol, benchmark),
                'Monthly Returns Table (%)': lambda stock: qsf.table_returns(stock, symbol, benchmark_symbol, benchmark),
                'Rolling Sharpe Table': lambda stock: qsf.table_rolling_sharpe(stock, symbol, benchmark_symbol, benchmark),
                'Rolling Sortino Table': lambda stock: qsf.table_rolling_sortino(stock, symbol, benchmark_symbol, benchmark),
                'Rolling Volatility Table': lambda stock: qsf.table_rolling_volatility(stock, symbol, benchmark_symbol, benchmark),
                'Yearly Returns Table (%)': lambda stock: qsf.table_yearly_returns(stock, symbol, benchmark_symbol, benchmark),
                'Metrics Table': lambda stock: qsf.key_metrics(stock, symbol, benchmark_symbol, benchmark)
            }

        # Initialize a list to keep track of which column is free
    columns = []
    free_column_index = 0
        # Initialize a dictionary to store tables
    tables = {}
        # Initialize a dictionary to store graphs
    graphs = {}

    for option in selected_options:
            # If the option is 'Monthly Heatmap Graph', display it in a full-width container
            if option == 'Monthly Heatmap Graph':
                fig = graph_functions[option](stock)
                if fig is not None:
                    st.plotly_chart(fig)
                    # Convert the figure to HTML and store it in the dictionary
                    graph_html = fig.to_html(full_html=False)
                    graphs[option] = graph_html
                continue  # Skip the rest of the loop

            # Always create 2 columns
            if free_column_index == 0:
                columns = st.columns(2)

            # Generate and display the graph or table
            if option in graph_functions:
                fig = graph_functions[option](stock)
                if fig is not None:
                    columns[free_column_index].plotly_chart(fig)
                    # Convert the figure to HTML and store it in the dictionary
                    graph_html = fig.to_html(full_html=False)
                    graphs[option] = graph_html
            elif option in table_functions:
                df = table_functions[option](stock)
                if df is not None:
                    # Generate column definitions based on DataFrame columns
                    column_defs = [{'headerName': col, 'field': col, 'filter': True} for col in df.columns]

                    gridOptions={
                        'columnDefs': column_defs,
                        'defaultColDef': {'flex': 1, 'editable': False},
                        'fit_columns_on_grid_load': True,
                    }
                    with columns[free_column_index].container():
                        st.markdown(f"###### **{option}**")  # Add a title to the table
                        AgGrid(df, gridOptions=gridOptions)

                    # Store the table in the dictionary
                    tables[option] = df

            # Switch to the next column for the next figure or table
            free_column_index = (free_column_index + 1) % 2

        # Add the export button
    if len(tables) > 0 or len(graphs) > 0:
            qsf.export_data(graphs, tables, symbol)
        
elif st.session_state['page'] == 'Snapshot':
    # Save the output of qs.reports.html(stock) to a file
    qs.reports.html(stock, benchmark=benchmark, output="snapshot.html")

    # Read the HTML file
    with open("snapshot.html", 'r', encoding='utf-8') as f:
        html_string = f.read()

    # Display the HTML string in the Streamlit app
    components.html(html_string, width=1080, height=4000, scrolling=True)

        # Add an export button for the snapshot
    st.sidebar.download_button(
        label="Export Snapshot",
        data=html_string,
        file_name="snapshot.html",
        mime="text/html"
    )
