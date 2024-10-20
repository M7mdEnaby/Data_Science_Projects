import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Input two stock tickers for comparison
print("Enter the first stock ticker:")
first_input = input().upper()
print("vs.")
print("Enter the second stock ticker:")
second_input = input().upper()

# Get Ticker objects for the selected stocks
first_stock = yf.Ticker(first_input)
second_stock = yf.Ticker(second_input)

# Retrieve financial data (Net Income) for both stocks
first_financials = first_stock.financials
second_financials = second_stock.financials

# Extract Net Income data
first_net_income = first_financials.loc['Net Income']
second_net_income = second_financials.loc['Net Income']

# Create a comparison DataFrame
comparison_df = pd.DataFrame({
    first_input: first_net_income,
    second_input: second_net_income
})

# Reset index to include the 'Date' as a column for plotting
comparison_df = comparison_df.reset_index()

# Create the Plotly graph
fig = go.Figure()

# Add a line for the first stock's Net Income
fig.add_trace(go.Scatter(x=comparison_df['index'], y=comparison_df[first_input],
                         mode='lines+markers', name=f'{first_input} Net Income'))

# Add a line for the second stock's Net Income
fig.add_trace(go.Scatter(x=comparison_df['index'], y=comparison_df[second_input],
                         mode='lines+markers', name=f'{second_input} Net Income'))

# Set layout for the dashboard
fig.update_layout(
    title=f'Net Income Comparison: {first_input} vs {second_input}',
    xaxis_title='Date',
    yaxis_title='Net Income (USD)',
    legend_title="Stocks",
    template='plotly_dark'
)

# Show the dashboard
fig.show()
