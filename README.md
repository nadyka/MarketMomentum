# MarketMomentum

MarketMomentum is a Streamlit application designed to generate custom reports for a selected stock and its benchmark. Users can choose the desired graphs and tables to be displayed in the report, which can be exported as an HTML or CSV file. The application also provides a snapshot of the stock's performance using the QuantStats library, which is saved as an HTML file and can be viewed within the application.

The application uses the AgGrid component for table display and Streamlit's download_button function for report exportation. The snapshot HTML file is displayed using Streamlit's components.html function. The application's sidebar contains widgets for user input, including a text input for the stock symbol, a checkbox for including a benchmark, a text input for the benchmark symbol, date input widgets for the start and end dates, and buttons for Snapshot and Custom Report. Based on the user's input, the application displays the selected graphs and tables in the main section. It also provides download buttons for exporting the report to HTML and CSV files. The snapshot HTML file is displayed within the application.

MarketMomentum is beneficial for financial analysts, stock traders, portfolio managers, and individual investors who need to analyze and monitor the performance of specific stocks on a daily basis. It provides a comprehensive snapshot of a stock's performance and allows users to generate custom reports with selected graphs and tables, which can be exported for further analysis. The inclusion of a benchmark comparison also provides valuable context for the stock's performance.

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
6. Export your custom report to HTML or CSV.

## Environment

Create a conda environment named marketmomentum and install the required packages:

bash conda create --name marketmomentum conda install streamlit streamlit-aggrid pandas numpy plotly streamlit-components quantstats

## Installation

Clone the repository and install the dependencies:

bash git clone https://github.com/jrebelo/MarketMomentum.git cd MarketMomentum


## Additional Planned Features

- Add definitions of each metric when hovering over the name
- Add automatic stock analysis
- LLM integration for analysis once the analysis algorithms are sufficient




## UI-features implemented and planned for future releases

- **Input Validation**: Added validation for user inputs. For example, our app checks if the entered stock symbol or benchmark symbol is valid. If not, it displays an error message to the user.
- TODO:**Loading Indicators**: Show a loading indicator when fetching data or generating reports, which might take some time, to inform the user that the process is ongoing.
- TODO:**Help Texts and Tooltips**: Provide help texts or tooltips for inputs and controls to guide the user on what to enter or what each control does.
- **Error Handling**: Implemented proper error handling. If something goes wrong (like a failed data fetch), the app shows a user-friendly error message.
- **Responsive Design**: Ensured the app is responsive and looks good on various screen sizes.
- **Default Values**: Where applicable, provided sensible default values. For example, the start date defaults to 5 years ago from the end date, which defaults as today.
- **Organize Inputs**: Grouped related inputs together in the sidebar to make the interface cleaner and more intuitive.
- **Searchable Dropdowns**: We made them searchable to improve user experience.
- TODO:**Pagination for Tables**: If tables can get very long, consider adding pagination to improve load times and usability.
- **Interactive Charts**: We've implamented interactive charts that allow users to zoom, pan, and hover over data points to see their values.

Remember, user-friendliness often comes from iterative feedback and improvements. Consider getting user feedback regularly and making necessary adjustments based on that feedback.

## Error Handling

The application can handle the following errors:

- **Invalid Stock Symbol**: If the user enters an invalid stock symbol, the application should catch the error and display a user-friendly message. This can be done by checking the response from the `qs.utils.download_returns(symbol)` function.
- **Invalid Benchmark Symbol**: Similar to the stock symbol, the application should handle cases where the user enters an invalid benchmark symbol.
- **Invalid Date Range**: The application should handle cases where the user enters an invalid date range. For example, the start date should not be later than the end date.
- **Data Unavailability**: The application should handle cases where data for the specified stock symbol or benchmark symbol is not available for the specified date range.

## Future Development (V2)

The current version (V1) is complete. For the next version (V2), we aim to enhance the functionality:
## Metric Descriptions

These descriptions should be added as tooltips for each metric when the user hovers over them:

1. `CAGR`: Compound Annual Growth Rate, the mean annual growth rate of an investment over a specified period of time longer than one year.
2. `Sharpe`: The Sharpe ratio, a measure of risk-adjusted return.
3. `Sortino`: The Sortino ratio, a variation of the Sharpe ratio that only factors in downside risk.
4. `Max Drawdown`: The maximum observed loss from a peak to a trough of a portfolio, before a new peak is attained.
5. `Volatility (ann.)`: The annualized standard deviation of returns, a measure of risk.
6. `Calmar`: The Calmar ratio, a comparison of the average annual compounded rate of return and the maximum drawdown risk.
7. `Expected Daily`: The expected daily return.
8. `Expected Monthly`: The expected monthly return.
9. `Expected Yearly`: The expected yearly return.
10. `Cumulative Return`: The total return on an investment.
11. `Prob. Sharpe Ratio`: The Probabilistic Sharpe Ratio, a measure of the probability that the expected Sharpe ratio of a strategy is greater than a benchmark Sharpe ratio.
12. `Smart Sharpe`: A variation of the Sharpe ratio that attempts to adjust for skewness and kurtosis in the returns distribution.
13. `Smart Sortino`: A variation of the Sortino ratio that attempts to adjust for skewness and kurtosis in the returns distribution.
14. `Sortino/√2`: The Sortino ratio divided by the square root of 2, a normalization technique.
15. `Smart Sortino/√2`: The Smart Sortino ratio divided by the square root of 2, a normalization technique.
16. `Skew`: A measure of the asymmetry of the probability distribution of returns.
17. `Kurtosis`: A measure of the "tailedness" of the probability distribution of returns.
18. `Daily Value-at-Risk`: The estimated maximum amount that the investment is likely to lose in one day with a certain probability.
19. `Gain/Pain Ratio`: The total of all monthly gains divided by the absolute total of all monthly losses.
20. `Tail Ratio`: The ratio of the average return of the 10% of months with the highest returns to the average return of the 10% of months with the lowest returns.
21. `Best Day`: The best single-day return.
22. `Worst Day`: The worst single-day return.
23. `Best Month`: The best single-month return.
24. `Worst Month`: The worst single-month return.
25. `Recovery Factor`: The ratio of total return to maximum drawdown.
26. `Ulcer Index`: A measure of the depth and duration of drawdowns in prices.
27. `Worst Year`: The worst single-year return.
28. `Best Year`: The best single-year return.
29. `Payoff Ratio`: The ratio of the average winning trade to the average losing trade.
30. `Profit Factor`: The ratio of gross profit to gross loss.
31. `CPC Index`: A measure of the robustness of a strategy, defined as the product of the Probabilistic Sharpe Ratio and the Profit Factor.
32. `Risk of Ruin`: The probability of an investment depleting to a specified level.
33. `Common Sense Ratio`: A ratio used to analyze the performance of an investment by comparing the expected return and the maximum drawdown.

## Metric Descriptions

Here are the descriptions listed with numbers for easier reference that should be added as the user hovers over each object:

1. `Cumulative Return`: The total return on an investment.
2. `CAGR`: Compound Annual Growth Rate, the mean annual growth rate of an investment over a specified period of time longer than one year.
3. `Sharpe`: The Sharpe ratio, a measure of risk-adjusted return.
4. `Prob. Sharpe Ratio`: The Probabilistic Sharpe Ratio, a measure of the probability that the expected Sharpe ratio of a strategy is greater than a benchmark Sharpe ratio.
5. `Smart Sharpe`: A variation of the Sharpe ratio that attempts to adjust for skewness and kurtosis in the returns distribution.
6. `Sortino`: The Sortino ratio, a variation of the Sharpe ratio that only factors in downside risk.
7. `Smart Sortino`: A variation of the Sortino ratio that attempts to adjust for skewness and kurtosis in the returns distribution.
8. `Sortino/√2`: The Sortino ratio divided by the square root of 2, a normalization technique.
9. `Smart Sortino/√2`: The Smart Sortino ratio divided by the square root of 2, a normalization technique.
10. `Max Drawdown`: The maximum observed loss from a peak to a trough of a portfolio, before a new peak is attained.
11. `Volatility (ann.)`: The annualized standard deviation of returns, a measure of risk.
12. `Calmar`: The Calmar ratio, a comparison of the average annual compounded rate of return and the maximum drawdown risk.
13. `Skew`: A measure of the asymmetry of the probability distribution of returns.
14. `Kurtosis`: A measure of the "tailedness" of the probability distribution of returns.
15. `Expected Daily`: The expected daily return.
16. `Expected Monthly`: The expected monthly return.
17. `Expected Yearly`: The expected yearly return.
18. `Best Day`: The best single-day return.
19. `Worst Day`: The worst single-day return.
20. `Best Month`: The best single-month return.
21. `Worst Month`: The worst single-month return.
22. `Recovery Factor`: The ratio of total return to maximum drawdown.
23. `Ulcer Index`: A measure of the depth and duration of drawdowns in prices.
24. `Worst Year`: The worst single-year return.
25. `Best Year`: The best single-year return.
26. `Payoff Ratio`: The ratio of the average winning trade to the average losing trade.
27. `Profit Factor`: The ratio of gross profit to gross loss.
28. `Common Sense Ratio`: A ratio used to analyze the performance of an investment by comparing the expected return and the maximum drawdown.
29. `CPC Index`: A measure of the robustness of a strategy, defined as the product of the Probabilistic Sharpe Ratio and the Profit Factor.
30. `Risk of Ruin`: The probability of an investment depleting to a specified level.
31. `Daily Value-at-Risk`: The estimated maximum amount that the investment is likely to lose in one day with a certain probability.
32. `Gain/Pain Ratio`: The total of all monthly gains divided by the absolute total of all monthly losses.
33. `Tail Ratio`: The ratio of the average return of the 10% of months with the highest returns to the average return of the 10% of months with the lowest returns.

We aim to incorporating Natural Language Processing (NLP) techniques to generate a detailed analysis of the stock data. While the `quantstats` package is already utilized to analyze stock data and produce various graphs and tables, it lacks the capability to automatically generate a comprehensive narrative analysis. To address this, we plan to integrate NLP libraries such as `nltk` or `spaCy`, enabling the system to generate insightful sentences based on the analyzed data.

Implementing this feature will necessitate a substantial addition of code and requires a solid grasp of NLP techniques. The quality of the generated analysis will be contingent upon the sophistication of the employed NLP model. As an illustrative example, consider the following Python snippet demonstrating how `nltk` could be leveraged to generate a basic sentence reflecting the mean return of a stock:

```bash
import nltk

mean_return = stock.mean()

if mean_return > 0: sentence = "The average return of the stock is positive." else: sentence = "The average return of the stock is negative."

nltk.word_tokenize(sentence)
```

This example is rudimentary, and actual implementation would entail more intricate analysis and sentence generation mechanisms.

In preparation for V2, we have outlined a preliminary approach to fetching daily returns for a specified stock and, optionally, a benchmark symbol. This involves managing session states and displaying errors through the `streamlit` library. The process includes several steps:

1. Checking if the 'stock' or 'symbol' keys are absent from the session state, or if the stored 'symbol' mismatches the provided symbol. Upon meeting these conditions, the system downloads the returns for the supplied symbol and refreshes the session state.
2. Introducing a brief pause to mitigate server overload risks associated with rapid successive requests.
3. In scenarios where a benchmark symbol is furnished, downloading the benchmark returns and filtering them according to the chosen date range. An empty DataFrame, signifying unavailability of data for the benchmark symbol within the specified date range, triggers an error message and halts execution.
4. Retrieving the 'stock' from the session state, applying filters to the returns based on the selected date range, and reconstructing price data from the filtered returns. Similar to the benchmark scenario, an empty DataFrame prompts an error message and cessation of execution.
5. Displaying an error message and terminating execution upon encountering an `IndexError` at any stage of the process. The error message includes details about the `IndexError`.
6. Handling other exceptions by presenting an error message detailing the occurrence and nature of the error, followed by stopping execution.

These enhancements aim to refine the application's functionality, ensuring robust error management and an improved user experience.
