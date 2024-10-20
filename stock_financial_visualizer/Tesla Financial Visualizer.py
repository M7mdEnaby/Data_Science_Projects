import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=0.3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype(float), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype(float), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False, height=900, title=stock, xaxis_rangeslider_visible=True)
    fig.show()

# Fetch Tesla stock data
TSLA = yf.Ticker('TSLA')
tesla_data = TSLA.history(period='max')
tesla_data.reset_index(inplace=True)

# Download the revenue data
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
res = requests.get(url)
html_data = res.content
soup = BeautifulSoup(html_data, 'html5lib')
tables = soup.find_all('table')

# Step 2: Identify the relevant table
tesla_table = None
for table in tables:
    if "Tesla Quarterly Revenue" in table.get_text():
        tesla_table = table
        break  # Stop searching once the relevant table is found

# Check if the relevant table was found
if tesla_table is None:
    print("Relevant table not found.")
else:
    # Step 3: Initialize a DataFrame
    tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

    # Step 4: Loop through rows
    for row in tesla_table.find_all('tr')[1:]:  # Skip header row
        columns = row.find_all('td')
        if len(columns) >= 2:  # Ensure there are at least two columns
            date = columns[0].get_text(strip=True)  # Extract date
            revenue = columns[1].get_text(strip=True)  # Extract revenue

            # Step 5: Clean revenue data
            revenue = revenue.replace('$', '').replace(',', '')  # Remove dollar signs and commas
            
            # Check if revenue is not empty before conversion
            if revenue:  # If revenue is not an empty string
                try:
                    revenue_value = float(revenue)  # Convert to float
                except ValueError:
                    print(f"Skipping invalid revenue value: {revenue}")
                    continue  # Skip this iteration if conversion fails

                # Step 6: Create a new DataFrame for the new row
                new_row = pd.DataFrame({"Date": [date], "Revenue": [revenue_value]})

                # Append the new row to the DataFrame using pd.concat
                tesla_revenue = pd.concat([tesla_revenue, new_row], ignore_index=True)

    # Convert the Date column to datetime
    tesla_revenue['Date'] = pd.to_datetime(tesla_revenue['Date'])

    # Display the DataFrame
    print(tesla_revenue.head())

# Finally, call the graphing function to visualize the data
make_graph(tesla_data, tesla_revenue, 'Tesla (TSLA)')
