# MarketMomentum

MarketMomentum is a financial analysis tool built with Python and Streamlit. It allows users to analyze the performance of stocks over a specified date range, compare them to a benchmark, and generate custom reports with various metrics and visualizations. Based on formulas from the popular Quantstats repository which can be found here: https://github.com/ranaroussi/quantstats


## Features

- **Home Page**: Enter a stock symbol to generate a custom report or see a key metrics snapshot.
- **Snapshot**: Provides a comprehensive report of the selected stock's performance, including various metrics and visualizations.
- **Benchmark Comparison**: Optional benchmark data can be included to compare to selected stock. Enter the stock market ticker symbol for the ETF or stock for results.
- **Custom Report**: Allows users to select specific graphs and tables to display, creating a custom report tailored to their needs.
- **Export**: Export the results of your custom report to HTML for graphs and tables, or as csv for table data. 

## Usage

1. Start streamlit app from main_mvp.py
2. Enter a stock symbol in the sidebar.
3. Select a date range for analysis.
4. Optionally, include a benchmark symbol for comparison. Supports NYSE ticker symbols.
5. Click on 'Snapshot' to generate a comprehensive report, or 'Custom Report' to select specific metrics and visualizations for your report.
6. Export your custom report to HTML or CSV 

## Environment

conda create --name marketmomentum

conda install streamlit streamlit-aggrid pandas numpy plotly streamlit-components quantstats


### Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/jrebelo/MarketMomentum.git
cd MarketMomentum
```

#### Additional Planned Features

- Add definitions of each metric when hovering over the name
- Add automatic stock analysis
- LLM integration for analysis once the analysis algorithms are sufficient
