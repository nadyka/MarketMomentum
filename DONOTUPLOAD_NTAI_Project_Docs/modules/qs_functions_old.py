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

def stock_price_performance():
        # plot the stock price performance in the first column
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(price)
    ax.set_title('Stock Price Performance')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    col1.pyplot(fig)
    plt.clf()  # Clear the current figure