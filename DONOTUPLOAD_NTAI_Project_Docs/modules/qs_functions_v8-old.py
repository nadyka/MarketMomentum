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

def plot_daily_returns(stock, benchmark=None):
    """
    Plots daily returns for a given stock and optionally compares it with SPY data.

    Parameters:
    - stock: A pandas DataFrame containing the daily returns for the stock.
    - benchmark: A pandas DataFrame containing the daily returns for SPY (optional).

    Returns:
    - A Plotly figure displaying the daily returns.
    """
    
    fig = go.Figure()

    # Add the daily returns plot for the stock
    fig.add_trace(go.Scatter(x=stock.index, y=stock, mode='lines', name='Daily Returns'))

    # Add the SPY data plot if benchmark is provided
    if benchmark is not None:
        fig.add_trace(go.Scatter(x=benchmark.index, y=benchmark, mode='lines', name='SPY', line=dict(color='black')))

    # Customize the layout
    fig.update_layout(title='Daily Returns', xaxis_title='Date', yaxis_title='Returns')

    return fig

def plot_distribution(stock):
    
    # Convert returns to percentages
    stock_percentage = stock * 100

    # Calculate the average
    average = np.mean(stock_percentage)

    fig = go.Figure(data=go.Histogram(x=stock_percentage, nbinsx=50, histnorm='probability density', name='Daily Returns'))


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
        title='Daily Returns Distribution',
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

def plot_earnings(stock):
    
    """
    Plots the earnings of returns for a given stock.
    Note: This function assumes 'stock' contains earnings data.
    """
    # Convert returns to growth of $1 investment over time
    earnings_data = (1 + stock).cumprod()
    # Plot the earnings
    fig = go.Figure(data=go.Scatter(x=earnings_data.index, y=earnings_data, mode='lines'))
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

def plot_log_returns(stock):
    """
    Plots the log returns of a given stock.
    """
    returns_data = stock
    # Calculate cumulative returns
    cumulative_returns = (1 + returns_data).cumprod() *100

    # Create a Plotly figure
    fig = go.Figure()

    # Add a scatter trace for the cumulative returns data
    fig.add_trace(go.Scatter(x=cumulative_returns.index, y=cumulative_returns, mode='lines', name='Cumulative Returns '))

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

def plot_returns(stock):
    stock_monthly = stock.resample('M').apply(lambda x: (1 + x).prod() - 1)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=stock_monthly.index, y=stock_monthly, mode='lines', name='Monthly Returns'))

    # Add title to the graph
    fig.update_layout(title_text='Monthly Returns')

    return fig

def plot_rolling_sharpe(stock):
    """
    Plots the rolling Sharpe ratio of a given stock.
    """
    rolling_sharpe = qs.stats.rolling_sharpe(stock)

    # Calculate the average of the Sharpe ratio
    average_sharpe = rolling_sharpe.mean()

    fig = go.Figure(data=go.Scatter(x=rolling_sharpe.index, y=rolling_sharpe, mode='lines'))
    # Add a red dotted line at the average
    fig.add_shape(
        type='line',
        x0=rolling_sharpe.index[0],
        x1=rolling_sharpe.index[-1],
        y0=average_sharpe,
        y1=average_sharpe,
        line=dict(color='Red', dash='dot')
    )
    fig.update_layout(title='Rolling Sharpe Ratio', xaxis_title='Date', yaxis_title='Sharpe Ratio')
    return fig

def plot_rolling_sortino(stock):
    """
    Plots the rolling Sortino ratio of a given stock.
    """
    returns_data = stock
    qs_daily_returns = qs.plots.rolling_sortino(returns_data)

    rolling_sortino = qs.stats.rolling_sortino(stock)

    # Calculate the average of the Sharpe ratio
    average_sortino = rolling_sortino.mean()

    fig = go.Figure(data=go.Scatter(x=rolling_sortino.index, y=rolling_sortino, mode='lines'))
    # Add a red dotted line at the average
    fig.add_shape(
        type='line',
        x0=rolling_sortino.index[0],
        x1=rolling_sortino.index[-1],
        y0=average_sortino,
        y1=average_sortino,
        line=dict(color='Red', dash='dot')
    )
    fig.update_layout(title='Rolling Sortino Ratio', xaxis_title='Date', yaxis_title='Sortino Ratio')

    return fig

def plot_rolling_volatility(stock):
    """
    Plots the rolling volatility of a given stock.
    """
    rolling_volatility = qs.stats.rolling_volatility(stock)

    # Calculate the average of the Sharpe ratio
    average_volatility = rolling_volatility.mean()

    fig = go.Figure(data=go.Scatter(x=rolling_volatility.index, y=rolling_volatility, mode='lines'))
    # Add a red dotted line at the average
    fig.add_shape(
        type='line',
        x0=rolling_volatility.index[0],
        x1=rolling_volatility.index[-1],
        y0=average_volatility,
        y1=average_volatility,
        line=dict(color='Red', dash='dot')
    )
    fig.update_layout(title='Rolling Volatility', xaxis_title='Date', yaxis_title='Volatility')
    return fig

def plot_yearly_returns(stock):
    """
    Plots the yearly returns of a given stock.
    """
    # Convert daily returns to yearly returns
    stock_yearly = stock.resample('Y').apply(lambda x: (1 + x).prod() - 1)

    # Calculate the average of the yearly returns
    average_yearly_return = stock_yearly.mean()

    fig = go.Figure()

    # Add the yearly returns plot for the stock as a bar graph
    fig.add_trace(go.Bar(x=stock_yearly.index, y=stock_yearly, name='EOY Returns'))

    # Add a red dotted line at the average
    fig.add_shape(
        type='line',
        x0=stock_yearly.index[0],
        x1=stock_yearly.index[-1],
        y0=average_yearly_return,
        y1=average_yearly_return,
        line=dict(color='Red', dash='dot')
    )

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

def table_daily_returns(stock, benchmark=None):
    """
    Prepares daily returns for a given stock and optionally compares it with SPY data for AgGrid table.

    Parameters:
    - stock: A pandas DataFrame containing the daily returns for the stock.
    - benchmark: A pandas DataFrame containing the daily returns for SPY (optional).
    """
    
    # Convert the stock data to a DataFrame and reset the index
    df = pd.DataFrame(stock).reset_index()

    # Rename the columns
    df.columns = ['Date', 'Daily Returns']
    # Format the 'Date' column to 'mm/dd/yyyy'
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')

    # Round 'Daily Returns' to 2 decimal places
    df['Daily Returns'] = df['Daily Returns'].round(2)

    # If benchmark is provided, add it to the DataFrame and round it
    if benchmark is not None:
        df['SPY'] = benchmark.round(2)

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
    


def table_earnings(stock):
    # Convert returns to growth of $1 investment over time
    earnings_data = (1 + stock).cumprod()

    # Convert the series to a DataFrame and reset the index to get 'Date' as a column
    earnings_df = earnings_data.reset_index()
    earnings_df.columns = ['Date', 'Value of $1']

    # Format 'Date' to mm/dd/yyyy and remove time
    earnings_df['Date'] = earnings_df['Date'].dt.strftime('%m/%d/%Y')

    # Round 'Value of $1' to 2 decimal places
    earnings_df['Value of $1'] = earnings_df['Value of $1'].round(2)

    # Display the earnings as an ag-Grid table

    return earnings_df


def table_returns(stock):
    stock_monthly = stock.resample('M').apply(lambda x: (1 + x).prod() - 1)
    stock_monthly_df = stock_monthly.reset_index()
    stock_monthly_df.columns = ['Date', 'Monthly Returns']

    # Round the returns to 2 decimal places
    stock_monthly_df['Monthly Returns'] = stock_monthly_df['Monthly Returns'].round(2)

    # Format the date to mm/dd/yyyy without any time
    stock_monthly_df['Date'] = stock_monthly_df['Date'].dt.strftime('%m/%d/%Y')

    return stock_monthly_df

def table_rolling_sharpe(stock):
    rolling_sharpe = qs.stats.rolling_sharpe(stock)
    rolling_sharpe.dropna(inplace=True)
    rolling_sharpe_df = rolling_sharpe.reset_index()
    rolling_sharpe_df.columns = ['Date', 'Rolling Sharpe Ratio']

    # Round the returns to 2 decimal places
    rolling_sharpe_df['Rolling Sharpe Ratio'] = rolling_sharpe_df['Rolling Sharpe Ratio'].round(2)

    # Format the date to mm/dd/yyyy without any time
    rolling_sharpe_df['Date'] = rolling_sharpe_df['Date'].dt.strftime('%m/%d/%Y')

    return rolling_sharpe_df

def table_rolling_sortino(stock):
    rolling_sortino = qs.stats.rolling_sortino(stock)
    rolling_sortino.dropna(inplace=True)
    rolling_sortino_df = rolling_sortino.reset_index()
    rolling_sortino_df.columns = ['Date', 'Rolling Sortino Ratio']

    # Round the ratio to 2 decimal places
    rolling_sortino_df['Rolling Sortino Ratio'] = rolling_sortino_df['Rolling Sortino Ratio'].round(2)

    # Format the date to mm/dd/yyyy without any time
    rolling_sortino_df['Date'] = rolling_sortino_df['Date'].dt.strftime('%m/%d/%Y')
    return rolling_sortino_df

def table_rolling_volatility(stock):
    rolling_volatility = qs.stats.rolling_volatility(stock)
    rolling_volatility.dropna(inplace=True)
    rolling_volatility_df = rolling_volatility.reset_index()
    rolling_volatility_df.columns = ['Date', 'Rolling Volatility']

    # Round the volatility to 2 decimal places
    rolling_volatility_df['Rolling Volatility'] = rolling_volatility_df['Rolling Volatility'].round(2)

    # Format the date to mm/dd/yyyy without any time
    rolling_volatility_df['Date'] = rolling_volatility_df['Date'].dt.strftime('%m/%d/%Y')
    return rolling_volatility_df

def table_yearly_returns(stock):
    stock_yearly = stock.resample('Y').apply(lambda x: (1 + x).prod() - 1)
    stock_yearly_df = stock_yearly.reset_index()
    stock_yearly_df.columns = ['Date', 'Yearly Returns']

    # Round the returns to 2 decimal places
    stock_yearly_df['Yearly Returns'] = stock_yearly_df['Yearly Returns'].round(2)

    # Extract the year from the date
    stock_yearly_df['Date'] = stock_yearly_df['Date'].dt.year

    return stock_yearly_df

def key_metrics(stock, benchmark=None):
    # Calculate additional metrics
    stock = stock.dropna()
    returns = qs.utils.to_returns(stock)
    returns = qs.utils._prepare_returns(returns)

    metrics = {
        'CAGR': qs.stats.cagr(returns),
        'Sharpe': qs.stats.sharpe(returns),
        'Sortino': qs.stats.sortino(returns),
        'Max Drawdown': qs.stats.max_drawdown(returns),
        'Volatility (ann.)': qs.stats.volatility(returns),
        'Calmar': qs.stats.calmar(returns),
        'Expected Daily': qs.stats.expected_return(returns, aggregate='D') * 100,
        'Expected Monthly': qs.stats.expected_return(returns, aggregate='M') * 100,
        'Expected Yearly': qs.stats.expected_return(returns, aggregate='A') * 100,
        'Cumulative Return': qs.stats.comp(returns) * 100,
        'Prob. Sharpe Ratio': qs.stats.probabilistic_sharpe_ratio(returns),
        'Smart Sharpe': qs.stats.smart_sharpe(returns),
        'Smart Sortino': qs.stats.smart_sortino(returns),
        'Sortino/√2': qs.stats.sortino(returns) / np.sqrt(2),
        'Smart Sortino/√2': qs.stats.smart_sortino(returns) / np.sqrt(2),
        'Skew': qs.stats.skew(returns),
        'Kurtosis': qs.stats.kurtosis(returns),
        'Daily Value-at-Risk': qs.stats.value_at_risk(returns),
        'Expected Shortfall (cVaR)': qs.stats.cvar(returns),
        'Gain/Pain Ratio': qs.stats.gain_to_pain_ratio(returns),
        'Tail Ratio': qs.stats.tail_ratio(returns),
        'Best Day': qs.stats.best(returns, 'D'),
        'Worst Day': qs.stats.worst(returns, 'D'),
        'Best Month': qs.stats.best(returns, 'M'),
        'Worst Month': qs.stats.worst(returns, 'M'),
        'Recovery Factor': qs.stats.recovery_factor(returns),
        'Ulcer Index': qs.stats.ulcer_index(returns),
    }

    # Convert to DataFrame and round to 2 decimals
    metrics_df = pd.DataFrame.from_dict(metrics, orient='index', columns=['Stock']).round(2)

    if benchmark is not None:
        benchmark = benchmark.dropna()
        benchmark_returns = qs.utils._prepare_returns(benchmark)

        benchmark_metrics = {
            'CAGR': qs.stats.cagr(benchmark_returns),
            'Sharpe': qs.stats.sharpe(benchmark_returns),
            'Sortino': qs.stats.sortino(benchmark_returns),
            'Max Drawdown': qs.stats.max_drawdown(benchmark_returns),
            'Volatility (ann.)': qs.stats.volatility(benchmark_returns),
            'Calmar': qs.stats.calmar(benchmark_returns),
            'Expected Daily': qs.stats.expected_return(benchmark_returns, aggregate='D') * 100,
            'Expected Monthly': qs.stats.expected_return(benchmark_returns, aggregate='M') * 100,
            'Expected Yearly': qs.stats.expected_return(benchmark_returns, aggregate='A') * 100,
            'Cumulative Return': qs.stats.comp(benchmark_returns) * 100,
            'Prob. Sharpe Ratio': qs.stats.probabilistic_sharpe_ratio(benchmark_returns),
            'Smart Sharpe': qs.stats.smart_sharpe(benchmark_returns),
            'Smart Sortino': qs.stats.smart_sortino(benchmark_returns),
            'Sortino/√2': qs.stats.sortino(benchmark_returns) / np.sqrt(2),
            'Smart Sortino/√2': qs.stats.smart_sortino(benchmark_returns) / np.sqrt(2),
            'Skew': qs.stats.skew(benchmark_returns),
            'Kurtosis': qs.stats.kurtosis(benchmark_returns),
            'Daily Value-at-Risk': qs.stats.value_at_risk(benchmark_returns),
            'Expected Shortfall (cVaR)': qs.stats.cvar(benchmark_returns),
            'Gain/Pain Ratio': qs.stats.gain_to_pain_ratio(benchmark_returns),
            'Tail Ratio': qs.stats.tail_ratio(benchmark_returns),
            'Best Day': qs.stats.best(benchmark_returns, 'D'),
            'Worst Day': qs.stats.worst(benchmark_returns, 'D'),
            'Best Month': qs.stats.best(benchmark_returns, 'M'),
            'Worst Month': qs.stats.worst(benchmark_returns, 'M'),
            'Recovery Factor': qs.stats.recovery_factor(benchmark_returns),
            'Ulcer Index': qs.stats.ulcer_index(benchmark_returns),
        }

        metrics.update(benchmark_metrics)

        # Convert to DataFrame and round to 2 decimals
        benchmark_metrics_df = pd.DataFrame.from_dict(benchmark_metrics, orient='index', columns=['Benchmark']).round(2)

        # Join the two dataframes
        metrics_df = metrics_df.reset_index().merge(benchmark_metrics_df.reset_index(), left_on='index', right_on='index', how='outer')
        metrics_df.columns = ['Metric', 'Stock', 'Benchmark']
    else:
        metrics_df.reset_index(inplace=True)
        metrics_df.columns = ['Metric', 'Stock']

    return metrics_df