import yfinance as yf
import pandas as pd
import mplfinance as mpf

# Download historical data for Microsoft (MSFT) stock for the past 10 years
msft = yf.Ticker("MSFT")
msft_data = msft.history(period="10y")

# Resample the data to show yearly data (OHLC - Open, High, Low, Close)
df_msft = msft_data.resample('YE').agg({'Open': 'first', 
                                         'High': 'max', 
                                         'Low': 'min', 
                                         'Close': 'last'})

# Ensure the index is a DatetimeIndex
df_msft.index = pd.to_datetime(df_msft.index)

# Plot the Japanese candlestick chart
mpf.plot(df_msft, type='candle', style='charles', title='MSFT Yearly Candlestick Chart', ylabel='Price (USD)', volume=False)
