import matplotlib.pyplot as plt
import numpy as np
import quantstats as qs

def stock_price_performance(price, col):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(price)
    ax.set_title('Stock Price Performance')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    col.pyplot(fig)
    plt.clf()

def returns(stock, col):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(stock)
    ax.set_title('Returns')
    ax.set_xlabel('Date')
    ax.set_ylabel('Returns')
    col.pyplot(fig)
    plt.clf()

def monthly_returns(stock, col):
    monthly_returns = stock.resample('ME').apply(qs.stats.comp)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_returns)
    ax.set_title('Monthly Returns')
    ax.set_xlabel('Date')
    ax.set_ylabel('Monthly Returns')
    col.pyplot(fig)
    plt.clf()

def average_monthly_returns(stock, col):
    avg_monthly_returns = stock.resample('ME').apply(np.mean)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(avg_monthly_returns)
    ax.set_title('Average Monthly Returns')
    ax.set_xlabel('Date')
    ax.set_ylabel('Average Monthly Returns')
    col.pyplot(fig)
    plt.clf()

def expected_returns(stock, col):
    expected_returns = qs.stats.expected_return(stock)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(expected_returns)
    ax.set_title('Expected Returns')
    ax.set_xlabel('Date')
    ax.set_ylabel('Expected Returns')
    col.pyplot(fig)
    plt.clf()