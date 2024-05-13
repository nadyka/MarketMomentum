import streamlit as st
from datetime import datetime, date
import quantstats as qs
import streamlit.components.v1 as components
from modules import qs_functions as qsf
import time
from st_aggrid import AgGrid
import pandas as pd
import numpy as np
from st_aggrid import AgGrid

def table_daily_returns(stock, spy_data=None):
    """
    Displays daily returns for a given stock and optionally compares it with SPY data as an AgGrid table.

    Parameters:
    - stock: A pandas DataFrame containing the daily returns for the stock.
    - spy_data: A pandas DataFrame containing the daily returns for SPY (optional).
    """
    
    # Convert the stock data to a DataFrame and reset the index
    df = pd.DataFrame(stock).reset_index()

    # Rename the columns
    df.columns = ['Date', 'Daily Returns']

    # If spy_data is provided, add it to the DataFrame
    if spy_data is not None:
        df['SPY'] = spy_data

    # Display the DataFrame as an AgGrid table
    AgGrid(df)


def table_distribution(stock):
    """
    Displays the distribution of daily returns for a given stock as an AgGrid table.

    Parameters:
    - stock: A pandas DataFrame containing the daily returns for the stock.
    """
    
    # Convert returns to percentages
    stock_percentage = stock * 100

    # Convert the data to a DataFrame and reset the index
    df = pd.DataFrame(stock_percentage).reset_index()

    # Rename the columns
    df.columns = ['Date', 'Daily Returns (%)']

    # Display the DataFrame as an AgGrid table
    AgGrid(df)


def table_drawdown(stock):
    """
    Displays the drawdown of returns for a given stock as an AgGrid table.

    Parameters:
    - stock: A pandas DataFrame containing the daily returns for the stock.
    """
    
    # Drop NaN values
    stock = stock.dropna()

    # Convert returns data into prices
    prices = (1 + stock).cumprod()

    # Calculate drawdown series
    drawdown_series = prices / np.maximum.accumulate(prices) - 1.0
    drawdown_series = drawdown_series.replace([np.inf, -np.inf, -0], 0)
    drawdown_series = drawdown_series.rename('drawdown')

    # Convert drawdown series to DataFrame
    drawdown_df = pd.DataFrame(drawdown_series)

    # Reset index to get 'Date' as a column
    drawdown_df = drawdown_df.reset_index()

    # Extract the year from 'Date'
    drawdown_df['year'] = drawdown_df['Date'].dt.year

    # Convert 'drawdown' to percentage
    drawdown_df['drawdown %'] = drawdown_df['drawdown'] * 100

    # Display the DataFrame as an AgGrid table
    AgGrid(drawdown_df)

def table_drawdowns_periods(stock):
# Drop NaN values
    stock = stock.dropna()

    # Convert returns data into prices
    prices = (1 + stock).cumprod()

    # Calculate drawdown series
    drawdown_series = prices / np.maximum.accumulate(prices) - 1.0
    drawdown_series = drawdown_series.replace([np.inf, -np.inf, -0], 0)
    drawdown_series = drawdown_series.rename('drawdown')

    # Convert drawdown series to DataFrame
    drawdown_df = pd.DataFrame(drawdown_series)

    # Reset index to get 'Date' as a column
    drawdown_df = drawdown_df.reset_index()

    # Your provided calculations for drawdowns
    drawdown_df = drawdown_df.copy()  # assuming drawdown_df is already defined

    # Identify the start of drawdown periods
    drawdown_start = (drawdown_df['drawdown'] < 0) & (drawdown_df['drawdown'].shift() >= 0)

    # Identify drawdown periods
    drawdown_df['drawdown_period'] = drawdown_start.cumsum()

    # Calculate min drawdown for each period
    drawdown_periods = drawdown_df.groupby('drawdown_period')['drawdown'].min()

    # Get the 5 worst drawdown periods
    worst_periods = drawdown_periods.nsmallest(5).index

    # Get start and end dates for the worst periods
    worst_periods_df = drawdown_df[drawdown_df['drawdown_period'].isin(worst_periods)]
    start_end_dates = worst_periods_df.groupby('drawdown_period')['Date'].agg(['first', 'last'])

    # Your provided code for earnings graph
    st.subheader('Worst Drawdown Periods')
    AgGrid(start_end_dates)

def table_earnings(stock):
    # Convert returns to growth of $1 investment over time
    earnings_data = (1 + stock).cumprod()

    # Convert the series to a DataFrame and reset the index to get 'Date' as a column
    earnings_df = earnings_data.reset_index()
    earnings_df.columns = ['Date', 'Value of $1']

    # Display the earnings as an ag-Grid table
    st.subheader('Earnings')
    AgGrid(earnings_df)

def table_monthly_dist(stock):
    # Convert daily returns to monthly returns
    stock_monthly = stock.resample('M').apply(lambda x: (1 + x).prod() - 1)

    # Convert returns to percentages
    stock_percentage = stock_monthly * 100

    # Convert the series to a DataFrame and reset the index to get 'Date' as a column
    monthly_dist_df = stock_percentage.reset_index()
    monthly_dist_df.columns = ['Date', 'Returns (%)']

    # Display the monthly returns distribution as an ag-Grid table
    st.subheader('Monthly Returns Distribution')
    AgGrid(monthly_dist_df)

def table_log_returns(stock):
    returns_data = stock
    cumulative_returns = (1 + returns_data).cumprod() *100
    cumulative_returns_df = cumulative_returns.reset_index()
    cumulative_returns_df.columns = ['Date', 'Cumulative Returns']
    st.subheader('Cumulative Returns (Log Scaled)')
    AgGrid(cumulative_returns_df)

def table_monthly_heatmap(stock):
    monthly_returns = stock.resample('M').apply(lambda x: (1 + x).prod() - 1)
    if not isinstance(monthly_returns.index, pd.DatetimeIndex):
        monthly_returns.index = pd.to_datetime(monthly_returns.index)
    monthly_returns = monthly_returns.to_frame('Returns')
    monthly_returns['Year'] = monthly_returns.index.year
    monthly_returns['Month'] = monthly_returns.index.month_name()
    monthly_returns_pivot = monthly_returns.pivot(index='Year', columns='Month', values='Returns')
    monthly_returns_pivot = monthly_returns_pivot[['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']]
    st.subheader('Monthly Returns Heatmap for MSFT')
    AgGrid(monthly_returns_pivot)

def table_returns(stock):
    stock_monthly = stock.resample('M').apply(lambda x: (1 + x).prod() - 1)
    stock_monthly_df = stock_monthly.reset_index()
    stock_monthly_df.columns = ['Date', 'Monthly Returns']
    st.subheader('Monthly Returns')
    AgGrid(stock_monthly_df)

def table_rolling_sharpe(stock):
    rolling_sharpe = qs.stats.rolling_sharpe(stock)
    rolling_sharpe_df = rolling_sharpe.reset_index()
    rolling_sharpe_df.columns = ['Date', 'Rolling Sharpe Ratio']
    st.subheader('Rolling Sharpe Ratio')
    AgGrid(rolling_sharpe_df)

def table_rolling_sortino(stock):
    rolling_sortino = qs.stats.rolling_sortino(stock)
    rolling_sortino_df = rolling_sortino.reset_index()
    rolling_sortino_df.columns = ['Date', 'Rolling Sortino Ratio']
    st.subheader('Rolling Sortino Ratio')
    AgGrid(rolling_sortino_df)

def table_rolling_volatility(stock):
    rolling_volatility = qs.stats.rolling_volatility(stock)
    rolling_volatility_df = rolling_volatility.reset_index()
    rolling_volatility_df.columns = ['Date', 'Rolling Volatility']
    st.subheader('Rolling Volatility')
    AgGrid(rolling_volatility_df)

def table_yearly_returns(stock):
    stock_yearly = stock.resample('Y').apply(lambda x: (1 + x).prod() - 1)
    stock_yearly_df = stock_yearly.reset_index()
    stock_yearly_df.columns = ['Date', 'Yearly Returns']
    st.subheader('Yearly Returns')
    AgGrid(stock_yearly_df)