import streamlit as st
from datetime import datetime, date
import quantstats as qs
import streamlit.components.v1 as components
from modules import qs_functions as qsf
import time
from st_aggrid import AgGrid

# extend pandas functionality with metrics, etc.
qs.extend_pandas()

st.set_page_config(page_title='MarketMomentum', layout='wide', page_icon=':🎰:')

# Initialize session_state if it doesn't exist
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'

if st.session_state['page'] == 'Home':
    st.title("Welcome to MarketMomentum!")
    st.text("To get started, enter a stock symbol and generate your own custom report or see a key metrics snapshot")

# create a text input for the stock symbol in the sidebar
symbol = st.sidebar.text_input("Enter a stock symbol", "MSFT")

# Initialize benchmark to None
benchmark = None

# Define benchmark_symbol with a default value
benchmark_symbol = None

# Add a sidebar title
st.sidebar.title('Dates')

# Add a date input widget in the sidebar
end_date = date.today()
start_date = datetime.strptime('1985-01-01', '%Y-%m-%d').date() # set to 1/1/1985
start_date = st.sidebar.date_input('Start date', start_date, min_value=start_date, max_value=end_date)
end_date = st.sidebar.date_input('End date', end_date, min_value=start_date, max_value=end_date)

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

time.sleep(.5)

# fetch the daily returns for a stock
if 'stock' not in st.session_state or 'symbol' not in st.session_state or st.session_state['symbol'] != symbol:
    st.session_state['stock'] = qs.utils.download_returns(symbol)
    st.session_state['symbol'] = symbol

time.sleep(.5)
    # If a benchmark symbol is provided, download the returns for the benchmark
if benchmark_symbol:
        benchmark = qs.utils.download_returns(benchmark_symbol)
        # Filter the benchmark for the selected date range
        benchmark = benchmark.loc[start_str:end_str]

stock = st.session_state['stock']

# Filter the returns for the selected date range
stock = stock.loc[start_str:end_str]

# Reconstruct the price data from the returns
price = (1 + stock).cumprod()

if st.session_state['page'] == 'Custom Report':
    # Define the options for the multi-select dropdown menu
    options = ['Metrics Table', 'Daily Returns Graph', 'Daily Returns Table', 'Daily Returns Distribution Graph', 'Drawdown Graph', 'Drawdowns Periods Graph', 'Drawdowns Periods Table', 'Earnings Graph', 'Earnings Table', 'Monthly Distribution Graph',  'Log Returns Graph', 'Monthly Heatmap Graph', 'Monthly Returns Graph', 'Monthly Returns Table', 'Rolling Sharpe Graph', 'Rolling Sharpe Table', 'Rolling Sortino Graph', 'Rolling Sortino Table', 'Rolling Volatility Graph', 'Rolling Volatility Table', 'Yearly Returns Graph', 'Yearly Returns Table']
    selected_options = st.sidebar.multiselect('Select the graphs and tables you want to display:', options)

    generate_report_button = st.sidebar.button('Generate Report')

    if generate_report_button:
    # Modify the function mappings to pass the benchmark to the functions
        graph_functions = {
                'Daily Returns Graph': lambda stock: qsf.plot_daily_returns(stock, benchmark),
                'Daily Returns Distribution Graph': lambda stock: qsf.plot_distribution(stock, benchmark, benchmark_symbol),
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
                'Daily Returns Table': lambda stock: qsf.table_daily_returns(stock, benchmark),
                'Drawdowns Periods Table': qsf.table_drawdowns_periods,
                'Earnings Table': qsf.table_earnings,
                'Monthly Returns Table': qsf.table_returns,
                'Rolling Sharpe Table': qsf.table_rolling_sharpe,
                'Rolling Sortino Table': qsf.table_rolling_sortino,
                'Rolling Volatility Table': qsf.table_rolling_volatility,
                'Yearly Returns Table': qsf.table_yearly_returns,
                'Metrics Table': lambda stock: qsf.key_metrics(stock, benchmark)
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
                        'defaultColDef': {'flex': 1},
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
            # Convert all tables and graphs to HTML and join them
            graphs_html = ''.join([f'<div class="graph">{graph}</div>' for graph in graphs.values()])
            tables_html = ''.join([f'<div class="table"><h2>{name}</h2>{df.to_html(border=0, index=False)}</div>' for name, df in tables.items()])
            html = f'<h1>{symbol} Custom Report</h1><div class="container"><div class="graphs">{graphs_html}</div><div class="tables">{tables_html}</div></div>'

            # Add CSS to style the tables and graphs
            css = """
            <style>
            .container {
                display: flex;
                align-items: flex-start;
            }
            .graphs {
                width: 66.66%;
            }
            .tables {
                width: 33.33%;
            }
            .table table {
                border-collapse: collapse;
                width: 100%;
            }
            .table table td, .table table th {
                border: none;
                padding: 10px;
                text-align: left;
            }
            .table table th {
                white-space: nowrap;
            }
            </style>
            """

            # Add the CSS to the HTML
            html = css + html

            # Create a download button for the HTML file
            st.sidebar.download_button(
                "Export all to HTML",
                data=html,
                file_name='tables_and_graphs.html',
                mime='text/html'
            )
            
            # Convert all tables to CSV and join them
            csv = '\n\n'.join([df.to_csv() for df in tables.values()])

            # Create a download button for the CSV file
            st.sidebar.download_button(
                "Export tables to CSV",
                data=csv,
                file_name='tables.csv',
                mime='text/csv'
            )
        
elif st.session_state['page'] == 'Snapshot':
    # Save the output of qs.reports.html(stock) to a file
    qs.reports.html(stock, benchmark=benchmark, output="NTAI_Project_Docs/quantstats-tearsheet.html")

    # Read the HTML file
    with open("NTAI_Project_Docs/quantstats-tearsheet.html", 'r', encoding='utf-8') as f:
        html_string = f.read()

    # Display the HTML string in the Streamlit app
    components.html(html_string, width=1080, height=4000, scrolling=True)