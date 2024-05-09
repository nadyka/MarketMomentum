import numpy as np
import quantstats as qs
import plotly.graph_objects as go
from scipy.stats import norm
import pandas as pd

def max_consecutive(returns, win=True):
    # Convert returns to binary win/loss
    binary = returns > 0 if win else returns < 0

    # Find where the streaks of wins/losses start
    streak_starts = (~binary).shift(-1).fillna(False) & binary

    # Find where the streaks of wins/losses end
    streak_ends = binary.shift(-1).fillna(False) & (~binary)

    # Calculate the length of each streak
    streak_lengths = (streak_ends.cumsum() - streak_starts.cumsum()).max()

    return streak_lengths


############GRAPHS################

def plot_daily_returns(stock, symbol, benchmark=None, benchmark_symbol='Benchmark'):
    """
    Plots daily returns for a given stock and optionally compares it with a benchmark data.

    Parameters:
    - stock: A pandas DataFrame containing the daily returns for the stock.
    - benchmark: A pandas DataFrame containing the daily returns for the benchmark (optional).
    - benchmark_symbol: A string representing the ticker symbol of the benchmark (default is 'SPY').

    Returns:
    - A Plotly figure displaying the daily returns.
    """
    
    fig = go.Figure()

    # Add the daily returns plot for the stock
    fig.add_trace(go.Scatter(x=stock.index, y=stock, mode='lines', name=symbol, line=dict(color='blue')))

    # Add the benchmark data plot if benchmark is provided
    if benchmark is not None:
        fig.add_trace(go.Scatter(x=benchmark.index, y=benchmark, mode='lines', name=benchmark_symbol, line=dict(color='red')))

    # Customize the layout
    fig.update_layout(title='Daily Returns', xaxis_title='Date', yaxis_title='Returns')

    return fig

def plot_distribution(stock, symbol, benchmark=None, benchmark_symbol='Benchmark'):
    # Convert returns to percentages
    stock_percentage = stock * 100
    benchmark_percentage = None

    if benchmark is not None:
        benchmark_percentage = benchmark * 100

    # Calculate the average
    stock_average = np.mean(stock_percentage)
    benchmark_average = None

    if benchmark is not None:
        benchmark_average = np.mean(benchmark_percentage)

    fig = go.Figure(data=go.Histogram(x=stock_percentage, nbinsx=50, histnorm='probability density', name=f'{symbol} Daily Returns'))

    # Add a histogram for the benchmark if provided
    if benchmark is not None:
        fig.add_trace(go.Histogram(x=benchmark_percentage, nbinsx=50, histnorm='probability density', name=f'{benchmark_symbol} Daily Returns'))

    # Add a vertical line at the average
    fig.add_shape(
        type="line",
        x0=stock_average, y0=0, x1=stock_average, y1=1,
        line=dict(color="Red",width=2, dash="dot"),
        yref="paper"
    )

    # Add a vertical line at the benchmark average if provided
    if benchmark is not None:
        fig.add_shape(
            type="line",
            x0=benchmark_average, y0=0, x1=benchmark_average, y1=1,
            line=dict(color="Blue",width=2, dash="dot"),
            yref="paper"
        )

    # Update layout
    fig.update_layout(
        title='Daily Returns Distribution',
        xaxis_title='Returns (%)',
        yaxis_title='Density',
        bargap=0.1,
        barmode='overlay'
    )
    fig.update_traces(opacity=0.75)

    # Calculate the KDE
    x = np.linspace(stock_percentage.min(), stock_percentage.max(), 100)
    stock_pdf = norm.pdf(x, stock_average, stock_percentage.std())

    # Add the KDE line to the figure
    fig.add_trace(go.Scatter(x=x, y=stock_pdf, mode='lines', name=f'{symbol} Distribution'))

    # Calculate and add the benchmark KDE if provided
    if benchmark is not None:
        benchmark_pdf = norm.pdf(x, benchmark_average, benchmark_percentage.std())
        fig.add_trace(go.Scatter(x=x, y=benchmark_pdf, mode='lines', name=f'{benchmark_symbol} Distribution'))

    return fig

def plot_drawdown(stock):
    
    """
    Plots the drawdown of returns for a given stock.
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

    # Print drawdown_df
    print(drawdown_df)

    # Extract the year from 'Date'
    drawdown_df['year'] = drawdown_df['Date'].dt.year

    # Convert 'drawdown' to percentage
    drawdown_df['drawdown %'] = drawdown_df['drawdown'] * 100

    # Create a new figure
    fig = go.Figure()

    # Group the data by year
    grouped = drawdown_df.groupby('year')

    # Add a scatter trace for the drawdown of each year
    for name, group in grouped:
        fig.add_trace(go.Scatter(x=group['Date'], y=group['drawdown %'],
                            mode='lines',
                            name=name))

    # Calculate the overall average drawdown
    average_drawdown = drawdown_df['drawdown %'].mean()

    # Add a red dotted line for the average drawdown
    fig.add_shape(
        type="line",
        x0=drawdown_df['Date'].min(),
        y0=average_drawdown,
        x1=drawdown_df['Date'].max(),
        y1=average_drawdown,
        line=dict(
            color="red",
            width=2,
            dash="dot",
        ),
    )

    # Update the layout to add title and labels, and hide the legend
    fig.update_layout(title='Underwater Plot',
                    xaxis_title='Year',
                    yaxis_title='Drawdown (%)',
                    showlegend=False)
    return fig

def plot_drawdowns_periods(stock):
    """
    Plots the drawdowns periods of returns for a given stock.
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
    
    earnings_data = (1 + stock).cumprod()
    # Your provided code for earnings graph
    fig = go.Figure(data=go.Scatter(x=earnings_data.index, y=earnings_data, mode='lines'))

    # Add rectangles for the 5 worst drawdown periods
    for _, row in start_end_dates.iterrows():
        fig.add_shape(
            type="rect",
            xref="x", yref="paper",
            x0=row['first'], y0=0, x1=row['last'], y1=1,
            fillcolor="red", opacity=0.5, layer="below", line_width=0
        )

    fig.update_layout(title='Earnings with Worst Drawdown Periods', xaxis_title='Date', yaxis_title='Cumulative Returns')
    return fig

def plot_earnings(stock, symbol, benchmark=None, benchmark_symbol='Benchmark'):
    """
    Plots the earnings of returns for a given stock.
    Note: This function assumes 'stock' contains earnings data.
    """
    # Convert returns to growth of $1 investment over time
    earnings_data = (1 + stock).cumprod()
    # Plot the earnings
    fig = go.Figure(data=go.Scatter(x=earnings_data.index, y=earnings_data, mode='lines', name=symbol))

    # If a benchmark is provided, plot it as well
    if benchmark is not None:
        
        benchmark_data = (1 + benchmark).cumprod()
        fig.add_trace(go.Scatter(x=benchmark_data.index, y=benchmark_data, mode='lines', name=benchmark_symbol, line=dict(color='red')))

    fig.update_layout(title='Earnings', xaxis_title='Date', yaxis_title='Value of $1')
    return fig

def plot_monthly_dist(stock):
    
    # Convert daily returns to monthly returns
    stock_monthly = stock.resample('M').apply(lambda x: (1 + x).prod() - 1)

    # Convert returns to percentages
    stock_percentage = stock_monthly * 100

    # Calculate the average
    average = np.mean(stock_percentage)

    fig = go.Figure(data=go.Histogram(x=stock_percentage, nbinsx=45, histnorm='probability density', name='Monthly Returns'))


    # Add a vertical line at the average
    fig.add_shape(
        type="line",
        x0=average, y0=0, x1=average, y1=1,  # y1 is set to 1 to make the line span the entire y-axis
        line=dict(color="Red",width=2, dash="dot"),  # dash="dot" makes the line dotted
        yref="paper"  # This makes the y-coordinates be interpreted as a fraction of the plot's height
    )
    # Add a label for the line
    fig.add_annotation(
        x=average, y=0.5,
        text="Average",
        showarrow=True,
        arrowhead=1,
        ax=-50,
        ay=-100,
        yref="paper"
    )
    # Update layout
    fig.update_layout(
        title='Monthly Returns Distribution',
        xaxis_title='Returns (%)',
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(int(stock_percentage.min()), int(stock_percentage.max())+10, 10)),
            ticktext=[f'{i}%' for i in range(int(stock_percentage.min()), int(stock_percentage.max())+10, 10)],
            range=[min(0, stock_percentage.min()), stock_percentage.max()],
        ),
        yaxis_title='Density',
        bargap=0.1 # gap between bars of adjacent location coordinates
    )

    # Calculate the KDE
    x = np.linspace(stock_percentage.min(), stock_percentage.max(), 100)
    pdf = norm.pdf(x, average, stock_percentage.std())

    # Add the KDE line to the figure
    fig.add_trace(go.Scatter(x=x, y=pdf, mode='lines', name='Distribution'))
    return fig

def plot_log_returns(stock, symbol, benchmark=None, benchmark_symbol='Benchmark'):
    """
    Plots the log returns of a given stock and optionally compares it with a benchmark data.

    Parameters:
    - stock: A pandas DataFrame containing the daily returns for the stock.
    - benchmark: A pandas DataFrame containing the daily returns for the benchmark (optional).
    - benchmark_symbol: A string representing the ticker symbol of the benchmark (default is 'SPY').

    Returns:
    - A Plotly figure displaying the daily returns.
    """
    
    # Calculate cumulative returns
    stock_cumulative_returns = (1 + stock).cumprod() * 100
    benchmark_cumulative_returns = None

    if benchmark is not None:
        benchmark_cumulative_returns = (1 + benchmark).cumprod() * 100

    # Create a Plotly figure
    fig = go.Figure()

    # Add a scatter trace for the cumulative returns data
    fig.add_trace(go.Scatter(x=stock_cumulative_returns.index, y=stock_cumulative_returns, mode='lines', name=symbol, line=dict(color='blue')))

    # Add a scatter trace for the benchmark cumulative returns data if provided
    if benchmark is not None:
        fig.add_trace(go.Scatter(x=benchmark_cumulative_returns.index, y=benchmark_cumulative_returns, mode='lines', name=benchmark_symbol, line=dict(color='red')))

    # Set the title and axis labels
    fig.update_layout(title='Cumulative Returns (Log Scaled)', xaxis_title='Date', yaxis_title='Cumulative Returns')

    # Set the y-axis to a logarithmic scale, specify tick values and text, and ensure the negative part is always visible
    fig.update_yaxes(type='log', tickvals=[-1000000, -100000, -10000, -1000, -100, 0, 100, 1000, 10000, 100000, 1000000], 
                    ticktext=['-1 mil%', '-100k%', '-10k%', '-1k%', '-100%', '0', '100%', '1k%', '10k%', '100k%', '1 mil%'])

    return fig

def plot_monthly_heatmap(stock):
    """
    Plots the monthly heatmap of returns for a given stock.
    """
    # Calculate monthly returns
    monthly_returns = stock.resample('M').apply(lambda x: (1 + x).prod() - 1)

    # Convert the index to a DatetimeIndex if it's not already
    if not isinstance(monthly_returns.index, pd.DatetimeIndex):
        monthly_returns.index = pd.to_datetime(monthly_returns.index)

    # Extract 'Year' and 'Month' from the index
    monthly_returns = monthly_returns.to_frame('Returns')
    monthly_returns['Year'] = monthly_returns.index.year
    monthly_returns['Month'] = monthly_returns.index.month_name()

    # Prepare data for the heatmap
    monthly_returns_pivot = monthly_returns.pivot(index='Year', columns='Month', values='Returns')

    # Sort the columns to start with January and end with December
    monthly_returns_pivot = monthly_returns_pivot[[
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]]

    # Create the heatmap
    heatmap = go.Heatmap(
        z=monthly_returns_pivot.values,
        x=monthly_returns_pivot.columns,
        y=monthly_returns_pivot.index,
        colorscale='RdYlGn', # Color scale from red to yellow to green
        zmin=-0.5, # Minimum value for color scale
        zmax=0.5, # Maximum value for color scale
        hoverongaps=False,
        colorbar=dict(
            title="Return %",
            tickvals=[-0.5, -0.25, 0, 0.25, 0.5],
            ticktext=["-50%", "-25%", "0%", "25%", "50%"]
        )
    )

    # Create text for each box
    annotations = []
    for y in range(monthly_returns_pivot.shape[0]):
        for x in range(monthly_returns_pivot.shape[1]):
            annotations.append(go.layout.Annotation(
                xref='x', yref='y',
                x=monthly_returns_pivot.columns[x], y=monthly_returns_pivot.index[y],
                text=f"{monthly_returns_pivot.values[y, x]:.2%}",
                showarrow=False
            ))

    # Update layout for better visualization
    layout = go.Layout(
        title='Monthly Returns Heatmap for MSFT',
        xaxis_title='Month',
        yaxis_title='Year',
        width = 1280,
        height= 800,
        annotations=annotations
    )

    # Show the figure
    fig = go.Figure(data=heatmap, layout=layout)

    return fig

def plot_returns(stock, symbol, benchmark=None, benchmark_symbol='Benchmark'):
    """
    Plots monthly returns for a given stock and optionally compares it with a benchmark data.

    Parameters:
    - stock: A pandas DataFrame containing the daily returns for the stock.
    - benchmark: A pandas DataFrame containing the daily returns for the benchmark (optional).
    - benchmark_symbol: A string representing the ticker symbol of the benchmark (default is 'SPY').

    Returns:
    - A Plotly figure displaying the monthly returns.
    """
    
    # Calculate monthly returns
    stock_monthly = stock.resample('M').apply(lambda x: (1 + x).prod() - 1)
    benchmark_monthly = None

    if benchmark is not None:
        benchmark_monthly = benchmark.resample('M').apply(lambda x: (1 + x).prod() - 1)

    # Create a Plotly figure
    fig = go.Figure()

    # Add a scatter trace for the monthly returns data
    fig.add_trace(go.Scatter(x=stock_monthly.index, y=stock_monthly, mode='lines', name=symbol, line=dict(color='blue')))

    # Add a scatter trace for the benchmark monthly returns data if provided
    if benchmark is not None:
        fig.add_trace(go.Scatter(x=benchmark_monthly.index, y=benchmark_monthly, mode='lines', name=benchmark_symbol, line=dict(color='red')))

    # Add title to the graph
    fig.update_layout(title_text='Monthly Returns')

    return fig

def plot_rolling_sharpe(stock, symbol, benchmark=None, benchmark_symbol='Benchmark'):
    """
    Plots the rolling Sharpe ratio of a given stock and optionally compares it with a benchmark data.

    Parameters:
    - stock: A pandas DataFrame containing the daily returns for the stock.
    - benchmark: A pandas DataFrame containing the daily returns for the benchmark (optional).
    - benchmark_symbol: A string representing the ticker symbol of the benchmark (default is 'SPY').

    Returns:
    - A Plotly figure displaying the rolling Sharpe ratio.
    """
    
    # Calculate rolling Sharpe ratio
    rolling_sharpe = qs.stats.rolling_sharpe(stock)
    benchmark_rolling_sharpe = None

    if benchmark is not None:
        benchmark_rolling_sharpe = qs.stats.rolling_sharpe(benchmark)

    # Create a Plotly figure
    fig = go.Figure()

    # Add a scatter trace for the rolling Sharpe ratio data
    fig.add_trace(go.Scatter(x=rolling_sharpe.index, y=rolling_sharpe, mode='lines', name=symbol, line=dict(color='blue')))

    # Add a scatter trace for the benchmark rolling Sharpe ratio data if provided
    if benchmark is not None:
        fig.add_trace(go.Scatter(x=benchmark_rolling_sharpe.index, y=benchmark_rolling_sharpe, mode='lines', name=benchmark_symbol, line=dict(color='red')))

    # Add title to the graph
    fig.update_layout(title_text='Rolling Sharpe Ratio')

    return fig

def plot_rolling_sortino(stock, symbol, benchmark=None, benchmark_symbol='Benchmark'):
    """
    Plots the rolling Sortino ratio of a given stock and optionally compares it with a benchmark data.

    Parameters:
    - stock: A pandas DataFrame containing the daily returns for the stock.
    - benchmark: A pandas DataFrame containing the daily returns for the benchmark (optional).
    - benchmark_symbol: A string representing the ticker symbol of the benchmark (default is 'SPY').

    Returns:
    - A Plotly figure displaying the rolling Sortino ratio.
    """
    
    # Calculate rolling Sortino ratio
    rolling_sortino = qs.stats.rolling_sortino(stock)
    benchmark_rolling_sortino = None

    if benchmark is not None:
        benchmark_rolling_sortino = qs.stats.rolling_sortino(benchmark)

    # Create a Plotly figure
    fig = go.Figure()

    # Add a scatter trace for the rolling Sortino ratio data
    fig.add_trace(go.Scatter(x=rolling_sortino.index, y=rolling_sortino, mode='lines', name=symbol, line=dict(color='blue')))

    # Add a scatter trace for the benchmark rolling Sortino ratio data if provided
    if benchmark is not None:
        fig.add_trace(go.Scatter(x=benchmark_rolling_sortino.index, y=benchmark_rolling_sortino, mode='lines', name=benchmark_symbol, line=dict(color='red')))

    # Add title to the graph
    fig.update_layout(title_text='Rolling Sortino Ratio')

    return fig

def plot_rolling_volatility(stock, symbol, benchmark=None, benchmark_symbol='Benchmark'):
    """
    Plots the rolling volatility of a given stock and optionally compares it with a benchmark data.

    Parameters:
    - stock: A pandas DataFrame containing the daily returns for the stock.
    - benchmark: A pandas DataFrame containing the daily returns for the benchmark (optional).
    - benchmark_symbol: A string representing the ticker symbol of the benchmark (default is 'SPY').

    Returns:
    - A Plotly figure displaying the rolling volatility.
    """
    
    # Calculate rolling volatility
    rolling_volatility = qs.stats.rolling_volatility(stock)
    benchmark_rolling_volatility = None

    if benchmark is not None:
        benchmark_rolling_volatility = qs.stats.rolling_volatility(benchmark)

    # Create a Plotly figure
    fig = go.Figure()

    # Add a scatter trace for the rolling volatility data
    fig.add_trace(go.Scatter(x=rolling_volatility.index, y=rolling_volatility, mode='lines', name=symbol, line=dict(color='blue')))

    # Add a scatter trace for the benchmark rolling volatility data if provided
    if benchmark is not None:
        fig.add_trace(go.Scatter(x=benchmark_rolling_volatility.index, y=benchmark_rolling_volatility, mode='lines', name=benchmark_symbol, line=dict(color='red')))

    # Add title to the graph
    fig.update_layout(title_text='Rolling Volatility')

    return fig

def plot_yearly_returns(stock, symbol, benchmark=None, benchmark_symbol='Benchmark'):
    """
    Plots the yearly returns of a given stock and optionally compares it with a benchmark data.

    Parameters:
    - stock: A pandas DataFrame containing the daily returns for the stock.
    - benchmark: A pandas DataFrame containing the daily returns for the benchmark (optional).
    - benchmark_symbol: A string representing the ticker symbol of the benchmark (default is 'SPY').

    Returns:
    - A Plotly figure displaying the yearly returns.
    """
    
    # Convert daily returns to yearly returns
    stock_yearly = stock.resample('Y').apply(lambda x: (1 + x).prod() - 1)
    benchmark_yearly = None

    if benchmark is not None:
        benchmark_yearly = benchmark.resample('Y').apply(lambda x: (1 + x).prod() - 1)

    # Create a Plotly figure
    fig = go.Figure()

    # Add the yearly returns plot for the stock as a bar graph
    fig.add_trace(go.Bar(x=stock_yearly.index, y=stock_yearly, name=symbol))

    # Add the yearly returns plot for the benchmark as a bar graph if provided
    if benchmark is not None:
        fig.add_trace(go.Bar(x=benchmark_yearly.index, y=benchmark_yearly, name=benchmark_symbol))

    # Update layout to show y-axis as percentage
    fig.update_layout(
        title='Yearly Returns',
        xaxis_title='Date',
        yaxis_title='Return',
        yaxis=dict(
            tickformat=".0%"
        )
    )
    return fig

######TABLES######
def table_daily_returns(stock, symbol, benchmark_symbol=None, benchmark=None):
    """
    Prepares daily returns for a given stock and optionally compares it with a benchmark for AgGrid table.

    Parameters:
    - stock: A pandas DataFrame containing the daily returns for the stock.
    - symbol: The symbol of the stock.
    - benchmark_symbol: The symbol of the benchmark (optional).
    - benchmark: A pandas DataFrame containing the daily returns for the benchmark (optional).
    """
    
    # Convert the stock data to a DataFrame and reset the index
    df = pd.DataFrame(stock).reset_index()

    # Rename the columns
    df.columns = ['Date', symbol]
    # Format the 'Date' column to 'mm/dd/yyyy'
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')

    # Round 'Daily Returns' to 2 decimal places and convert to percentage
    df[symbol] = (df[symbol] * 100).round(2)

    # If benchmark is provided, prepare it separately and then merge it with the main DataFrame
    if benchmark is not None:
        benchmark_df = pd.DataFrame(benchmark).reset_index()
        benchmark_df.columns = ['Date', benchmark_symbol]
        benchmark_df['Date'] = benchmark_df['Date'].dt.strftime('%m/%d/%Y')
        benchmark_df[benchmark_symbol] = (benchmark_df[benchmark_symbol] * 100)
        df = df.merge(benchmark_df, on='Date', how='outer')

    return df

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

    # Mark periods with no drawdown
    no_dd = drawdown_series == 0

    # Convert no_dd to boolean type
    no_dd = no_dd.astype(bool)

    # Determine start and end dates of drawdown periods
    starts = (~no_dd & no_dd.shift(1).fillna(False)).where(lambda x: x).dropna().index
    ends = (no_dd & ~no_dd.shift(1).fillna(False)).where(lambda x: x).shift(-1, fill_value=False).dropna().index
    # Handle case where series begins or ends with a drawdown
    if starts[0] > ends[0]:
        starts = starts.insert(0, drawdown_series.index[0])
    if starts[-1] > ends[-1]:
        ends = ends.append(pd.Index([drawdown_series.index[-1]]))

    # Calculate drawdown details for each period
    data = []
    for start, end in zip(starts, ends):
        dd = drawdown_series[start:end]
        data.append({
            'start date': start.strftime('%m/%d/%Y'),
            'end date': end.strftime('%m/%d/%Y'),
            'valley date': dd.idxmin().strftime('%m/%d/%Y'),
            'Days': (end - start).days + 1,
            'drawdown %': round(dd.min() * 100, 2),  # round to 2 decimal places
            '99% max drawdown %': round(dd[dd > dd.quantile(0.01)].min() * 100, 2)  # round to 2 decimal places
        })

    # Create DataFrame from results
    df = pd.DataFrame(data)

    # Get the 5 worst drawdown periods
    df = df.nsmallest(5, 'drawdown %')

    return df

def table_drawdowns_periods(stock):
    # Drop NaN values
    stock = stock.dropna()

    # Convert returns data into prices
    prices = (1 + stock).cumprod()

    # Calculate drawdown series
    drawdown_series = prices / np.maximum.accumulate(prices) - 1.0
    drawdown_series = drawdown_series.replace([np.inf, -np.inf, -0], 0)
    drawdown_series = drawdown_series.rename('drawdown')

        # Mark periods with no drawdown
    no_dd = drawdown_series == 0

    # Convert no_dd to boolean type
    no_dd = no_dd.astype(bool)

    # Determine start and end dates of drawdown periods
    starts = (~no_dd & no_dd.shift(1).fillna(False)).where(lambda x: x).dropna().index
    ends = (no_dd & ~no_dd.shift(1).fillna(False)).where(lambda x: x).shift(-1, fill_value=False).dropna().index
    # Handle case where series begins or ends with a drawdown
    if starts[0] > ends[0]:
        starts = starts.insert(0, drawdown_series.index[0])
    if starts[-1] > ends[-1]:
        ends = ends.append(pd.Index([drawdown_series.index[-1]]))

        # Calculate drawdown details for each period
    data = []
    for start, end in zip(starts, ends):
        dd = drawdown_series[start:end]
        data.append({
            'start date': start.strftime('%m/%d/%Y'),
            'end date': end.strftime('%m/%d/%Y'),
            'valley date': dd.idxmin().strftime('%m/%d/%Y'),
            'Days': (end - start).days + 1,
            'drawdown %': round(dd.min() * 100, 2),  # round to 2 decimal places
            '99% max drawdown %': round(dd[dd > dd.quantile(0.01)].min() * 100, 2)  # round to 2 decimal places
        })

    # Create DataFrame from results
    df = pd.DataFrame(data)

    # Get the 10 worst drawdown periods
    df = df.nsmallest(10, 'drawdown %')


    return df
    

def table_earnings(stock, symbol, benchmark_symbol=None, benchmark=None):
    earnings_data = (1 + stock).cumprod()
    earnings_df = earnings_data.reset_index()
    earnings_df.columns = ['Date', symbol]
    earnings_df['Date'] = earnings_df['Date'].dt.strftime('%m/%d/%Y')
    earnings_df[symbol] = earnings_df[symbol].round(2)

    if benchmark is not None:
        benchmark_earnings_data = (1 + benchmark).cumprod()
        benchmark_earnings_df = benchmark_earnings_data.reset_index()
        benchmark_earnings_df.columns = ['Date', benchmark_symbol]
        benchmark_earnings_df['Date'] = benchmark_earnings_df['Date'].dt.strftime('%m/%d/%Y')
        benchmark_earnings_df[benchmark_symbol] = benchmark_earnings_df[benchmark_symbol].round(2)

        earnings_df = earnings_df.merge(benchmark_earnings_df, on='Date', how='outer')

    return earnings_df

def table_monthly_earnings(stock, symbol, benchmark_symbol=None, benchmark=None):
    earnings_data = (1 + stock.resample('M').apply(lambda x: (1 + x).prod() - 1)).cumprod()
    earnings_df = earnings_data.reset_index()
    earnings_df.columns = ['Date', symbol]
    earnings_df['Date'] = earnings_df['Date'].dt.strftime('%m/%d/%Y')
    earnings_df[symbol] = earnings_df[symbol].round(2)

    if benchmark is not None:
        benchmark_earnings_data = (1 + benchmark.resample('M').apply(lambda x: (1 + x).prod() - 1)).cumprod()
        benchmark_earnings_df = benchmark_earnings_data.reset_index()
        benchmark_earnings_df.columns = ['Date', benchmark_symbol]
        benchmark_earnings_df['Date'] = benchmark_earnings_df['Date'].dt.strftime('%m/%d/%Y')
        benchmark_earnings_df[benchmark_symbol] = benchmark_earnings_df[benchmark_symbol].round(2)

        earnings_df = earnings_df.merge(benchmark_earnings_df, on='Date', how='outer')

    return earnings_df

def table_yearly_earnings(stock, symbol, benchmark_symbol=None, benchmark=None):
    earnings_data = (1 + stock.resample('Y').apply(lambda x: (1 + x).prod() - 1)).cumprod()
    earnings_df = earnings_data.reset_index()
    earnings_df.columns = ['Date', symbol]
    earnings_df['Date'] = earnings_df['Date'].dt.strftime('%m/%d/%Y')
    earnings_df[symbol] = earnings_df[symbol].round(2)

    if benchmark is not None:
        benchmark_earnings_data = (1 + benchmark.resample('Y').apply(lambda x: (1 + x).prod() - 1)).cumprod()
        benchmark_earnings_df = benchmark_earnings_data.reset_index()
        benchmark_earnings_df.columns = ['Date', benchmark_symbol]
        benchmark_earnings_df['Date'] = benchmark_earnings_df['Date'].dt.strftime('%m/%d/%Y')
        benchmark_earnings_df[benchmark_symbol] = benchmark_earnings_df[benchmark_symbol].round(2)

        earnings_df = earnings_df.merge(benchmark_earnings_df, on='Date', how='outer')

    return earnings_df

def table_returns(stock, symbol, benchmark_symbol=None, benchmark=None):
    stock_monthly = stock.resample('M').apply(lambda x: (1 + x).prod() - 1)
    stock_monthly_df = stock_monthly.reset_index()
    stock_monthly_df.columns = ['Date', symbol]
    stock_monthly_df[symbol] = (stock_monthly_df[symbol] * 100).round(2)
    stock_monthly_df['Date'] = stock_monthly_df['Date'].dt.strftime('%m/%d/%Y')

    if benchmark is not None:
        benchmark_monthly = benchmark.resample('M').apply(lambda x: (1 + x).prod() - 1)
        benchmark_monthly_df = benchmark_monthly.reset_index()
        benchmark_monthly_df.columns = ['Date', benchmark_symbol]
        benchmark_monthly_df[benchmark_symbol] = (benchmark_monthly_df[benchmark_symbol] * 100).round(2)
        benchmark_monthly_df['Date'] = benchmark_monthly_df['Date'].dt.strftime('%m/%d/%Y')

        stock_monthly_df = stock_monthly_df.merge(benchmark_monthly_df, on='Date', how='outer')

    return stock_monthly_df

def table_rolling_sharpe(stock, symbol, benchmark_symbol=None, benchmark=None):
    rolling_sharpe = qs.stats.rolling_sharpe(stock)
    rolling_sharpe.dropna(inplace=True)
    rolling_sharpe_df = rolling_sharpe.reset_index()
    rolling_sharpe_df.columns = ['Date', symbol]
    rolling_sharpe_df[symbol] = rolling_sharpe_df[symbol].round(2)
    rolling_sharpe_df['Date'] = rolling_sharpe_df['Date'].dt.strftime('%m/%d/%Y')

    if benchmark is not None:
        benchmark_rolling_sharpe = qs.stats.rolling_sharpe(benchmark)
        benchmark_rolling_sharpe.dropna(inplace=True)
        benchmark_rolling_sharpe_df = benchmark_rolling_sharpe.reset_index()
        benchmark_rolling_sharpe_df.columns = ['Date', benchmark_symbol]
        benchmark_rolling_sharpe_df[benchmark_symbol] = benchmark_rolling_sharpe_df[benchmark_symbol].round(2)
        benchmark_rolling_sharpe_df['Date'] = benchmark_rolling_sharpe_df['Date'].dt.strftime('%m/%d/%Y')

        rolling_sharpe_df = rolling_sharpe_df.merge(benchmark_rolling_sharpe_df, on='Date', how='outer')

    return rolling_sharpe_df

def table_rolling_sortino(stock, symbol, benchmark_symbol=None, benchmark=None):
    rolling_sortino = qs.stats.rolling_sortino(stock)
    rolling_sortino.dropna(inplace=True)
    rolling_sortino_df = rolling_sortino.reset_index()
    rolling_sortino_df.columns = ['Date', symbol]
    rolling_sortino_df[symbol] = rolling_sortino_df[symbol].round(2)
    rolling_sortino_df['Date'] = rolling_sortino_df['Date'].dt.strftime('%m/%d/%Y')

    if benchmark is not None:
        benchmark_rolling_sortino = qs.stats.rolling_sortino(benchmark)
        benchmark_rolling_sortino.dropna(inplace=True)
        benchmark_rolling_sortino_df = benchmark_rolling_sortino.reset_index()
        benchmark_rolling_sortino_df.columns = ['Date', benchmark_symbol]
        benchmark_rolling_sortino_df[benchmark_symbol] = benchmark_rolling_sortino_df[benchmark_symbol].round(2)
        benchmark_rolling_sortino_df['Date'] = benchmark_rolling_sortino_df['Date'].dt.strftime('%m/%d/%Y')

        rolling_sortino_df = rolling_sortino_df.merge(benchmark_rolling_sortino_df, on='Date', how='outer')

    return rolling_sortino_df

def table_rolling_volatility(stock, symbol, benchmark_symbol=None, benchmark=None):
    rolling_volatility = qs.stats.rolling_volatility(stock)
    rolling_volatility.dropna(inplace=True)
    rolling_volatility_df = rolling_volatility.reset_index()
    rolling_volatility_df.columns = ['Date', symbol]
    rolling_volatility_df[symbol] = rolling_volatility_df[symbol].round(2)
    rolling_volatility_df['Date'] = rolling_volatility_df['Date'].dt.strftime('%m/%d/%Y')

    if benchmark is not None:
        benchmark_rolling_volatility = qs.stats.rolling_volatility(benchmark)
        benchmark_rolling_volatility.dropna(inplace=True)
        benchmark_rolling_volatility_df = benchmark_rolling_volatility.reset_index()
        benchmark_rolling_volatility_df.columns = ['Date', benchmark_symbol]
        benchmark_rolling_volatility_df[benchmark_symbol] = benchmark_rolling_volatility_df[benchmark_symbol].round(2)
        benchmark_rolling_volatility_df['Date'] = benchmark_rolling_volatility_df['Date'].dt.strftime('%m/%d/%Y')

        rolling_volatility_df = rolling_volatility_df.merge(benchmark_rolling_volatility_df, on='Date', how='outer')

    return rolling_volatility_df

def table_yearly_returns(stock, symbol, benchmark_symbol=None, benchmark=None):
    stock_yearly = stock.resample('Y').apply(lambda x: (1 + x).prod() - 1)
    stock_yearly_df = stock_yearly.reset_index()
    stock_yearly_df.columns = ['Date', symbol]
    stock_yearly_df[symbol] = (stock_yearly_df[symbol] * 100).round(2)
    stock_yearly_df['Date'] = stock_yearly_df['Date'].dt.year

    if benchmark is not None:
        benchmark_yearly = benchmark.resample('Y').apply(lambda x: (1 + x).prod() - 1)
        benchmark_yearly_df = benchmark_yearly.reset_index()
        benchmark_yearly_df.columns = ['Date', benchmark_symbol]
        benchmark_yearly_df[benchmark_symbol] = (benchmark_yearly_df[benchmark_symbol] * 100).round(2)
        benchmark_yearly_df['Date'] = benchmark_yearly_df['Date'].dt.year

        stock_yearly_df = stock_yearly_df.merge(benchmark_yearly_df, on='Date', how='outer')

    return stock_yearly_df

def key_metrics(stock, symbol, benchmark_symbol, benchmark=None):
    # Calculate additional metrics
    stock = stock.dropna()
    returns = qs.utils.to_returns(stock)
    returns = qs.utils._prepare_returns(returns)

    metrics = {
            'Cumulative Return': qs.stats.comp(returns) * 100,
            'CAGR': qs.stats.cagr(returns) * 100,
            'Sharpe': qs.stats.sharpe(returns),
            'Prob. Sharpe Ratio': qs.stats.probabilistic_sharpe_ratio(returns),
            'Smart Sharpe': qs.stats.smart_sharpe(returns),
            'Sortino': qs.stats.sortino(returns),
            'Smart Sortino': qs.stats.smart_sortino(returns),
            'Sortino/√2': qs.stats.sortino(returns) / np.sqrt(2),
            'Smart Sortino/√2': qs.stats.smart_sortino(returns) / np.sqrt(2),
            'Max Drawdown': qs.stats.max_drawdown(returns) * 100,
            'Volatility (ann.)': qs.stats.volatility(returns) * 100,
            'Calmar': qs.stats.calmar(returns),
            'Skew': qs.stats.skew(returns),
            'Kurtosis': qs.stats.kurtosis(returns),
            'Expected Daily': qs.stats.expected_return(returns, aggregate='D') * 100,
            'Expected Monthly': qs.stats.expected_return(returns, aggregate='M') * 100,
            'Expected Yearly': qs.stats.expected_return(returns, aggregate='A') * 100,
            'Best Day': qs.stats.best(returns, 'D') * 100,
            'Worst Day': qs.stats.worst(returns, 'D') * 100,
            'Best Month': qs.stats.best(returns, 'M') * 100,
            'Worst Month': qs.stats.worst(returns, 'M') * 100,
            'Recovery Factor': qs.stats.recovery_factor(returns),
            'Ulcer Index': qs.stats.ulcer_index(returns),
            'Worst Year': qs.stats.worst(returns, 'A') * 100,
            'Best Year': qs.stats.best(returns, 'A') * 100,
            'Recovery Factor': qs.stats.recovery_factor(returns),
            'Payoff Ratio': qs.stats.payoff_ratio(returns),
            'Profit Factor': qs.stats.profit_factor(returns),
            'Common Sense Ratio': qs.stats.common_sense_ratio(returns),
            'CPC Index': qs.stats.cpc_index(returns),
            'Prob. Sharpe Ratio': qs.stats.probabilistic_sharpe_ratio(returns)*100,
            'Risk of Ruin': qs.stats.risk_of_ruin(returns)*100,
            'Daily Value-at-Risk': qs.stats.value_at_risk(returns),
            'Gain/Pain Ratio': qs.stats.gain_to_pain_ratio(returns),
            'Tail Ratio': qs.stats.tail_ratio(returns),
            
    }

    # Convert to DataFrame and round to 2 decimals
    metrics_df = pd.DataFrame.from_dict(metrics, orient='index', columns=['Stock']).round(2)

    # Append '%' symbol to the selected metrics
    percentage_metrics = ['CAGR', 'Max Drawdown', 'Volatility (ann.)', 'Expected Daily', 'Expected Monthly', 'Expected Yearly', 'Cumulative Return', 'Best Day', 'Worst Day', 'Best Month', 'Worst Month', 'Best Year', 'Worst Year','Prob. Sharpe Ratio','Risk of Ruin']
    for metric in percentage_metrics:
        metrics_df.loc[metric, 'Stock'] = str(metrics_df.loc[metric, 'Stock']) + '%'

    # Repeat the same process for the benchmark if it exists
    if benchmark is not None:
        benchmark = benchmark.dropna()
        benchmark_returns = qs.utils._prepare_returns(benchmark)

        benchmark_metrics = {
            'CAGR': qs.stats.cagr(benchmark_returns) * 100,
            'Sharpe': qs.stats.sharpe(benchmark_returns),
            'Sortino': qs.stats.sortino(benchmark_returns),
            'Max Drawdown': qs.stats.max_drawdown(benchmark_returns) * 100,
            'Volatility (ann.)': qs.stats.volatility(benchmark_returns) * 100,
            'Calmar': qs.stats.calmar(benchmark_returns),
            'Expected Daily': qs.stats.expected_return(benchmark_returns, aggregate='D') * 100,
            'Expected Monthly': qs.stats.expected_return(benchmark_returns, aggregate='M') * 100,
            'Expected Yearly': qs.stats.expected_return(benchmark_returns, aggregate='A') * 100,
            'Cumulative Return': qs.stats.comp(benchmark_returns) * 100,
            'Prob. Sharpe Ratio': qs.stats.probabilistic_sharpe_ratio(benchmark_returns)*100,
            'Smart Sharpe': qs.stats.smart_sharpe(benchmark_returns),
            'Smart Sortino': qs.stats.smart_sortino(benchmark_returns),
            'Sortino/√2': qs.stats.sortino(benchmark_returns) / np.sqrt(2),
            'Smart Sortino/√2': qs.stats.smart_sortino(benchmark_returns) / np.sqrt(2),
            'Skew': qs.stats.skew(benchmark_returns),
            'Kurtosis': qs.stats.kurtosis(benchmark_returns),
            'Daily Value-at-Risk': qs.stats.value_at_risk(benchmark_returns),
            'Gain/Pain Ratio': qs.stats.gain_to_pain_ratio(benchmark_returns),
            'Tail Ratio': qs.stats.tail_ratio(benchmark_returns),
            'Best Day': qs.stats.best(benchmark_returns, 'D') * 100,
            'Worst Day': qs.stats.worst(benchmark_returns, 'D') * 100,
            'Best Month': qs.stats.best(benchmark_returns, 'M') * 100,
            'Worst Month': qs.stats.worst(benchmark_returns, 'M') * 100,
            'Recovery Factor': qs.stats.recovery_factor(benchmark_returns),
            'Ulcer Index': qs.stats.ulcer_index(benchmark_returns),
            'Worst Year': qs.stats.worst(benchmark_returns, 'A') * 100,
            'Best Year': qs.stats.best(benchmark_returns, 'A') * 100,
            'Recovery Factor': qs.stats.recovery_factor(benchmark_returns),
            'Payoff Ratio': qs.stats.payoff_ratio(benchmark_returns),
            'Profit Factor': qs.stats.profit_factor(benchmark_returns),
            'CPC Index': qs.stats.cpc_index(benchmark_returns),
            'Risk of Ruin': qs.stats.risk_of_ruin(benchmark_returns),
            'Common Sense Ratio': qs.stats.common_sense_ratio(benchmark_returns),
        }

        metrics.update(benchmark_metrics)

        # Convert to DataFrame and round to 2 decimals
        benchmark_metrics_df = pd.DataFrame.from_dict(benchmark_metrics, orient='index', columns=['Benchmark']).round(2)

        # Append '%' symbol to the selected metrics
        for metric in percentage_metrics:
            benchmark_metrics_df.loc[metric, 'Benchmark'] = str(benchmark_metrics_df.loc[metric, 'Benchmark']) + '%'

        # Join the two dataframes
        metrics_df = metrics_df.reset_index().merge(benchmark_metrics_df.reset_index(), left_on='index', right_on='index', how='outer')
        metrics_df.columns = ['Metric', symbol, benchmark_symbol]
    else:
        metrics_df.reset_index(inplace=True)
        metrics_df.columns = ['Metric', symbol]

    return metrics_df