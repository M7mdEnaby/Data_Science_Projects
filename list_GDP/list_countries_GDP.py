import numpy as np
import pandas as pd

# Suppress warnings
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn
warnings.filterwarnings('ignore')

# URL of the Wikipedia page containing GDP data
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

# Read tables from the webpage
countries = pd.read_html(url)

# Select the appropriate table (adjusted to 2 based on your previous findings)
df = countries[2]

# Set the first row as column headers and drop that row
df.columns = df.iloc[0]
df = df[1:]

# Retain the relevant columns (Country Name and GDP Value)
df = df.iloc[0:10, [0, 1]]  # Select first and second columns

# Rename the columns for clarity
df.columns = ["country", "GDP"]

# Clean the 'GDP' column by removing unwanted characters and convert to int
# Remove whitespace, dollar signs, and commas, and handle non-numeric entries
df["GDP"] = df["GDP"].replace({'\$': '', ',': '', r'\[n 1\]': ''}, regex=True)  # Adjust regex if needed
df["GDP"] = df["GDP"].str.strip()  # Strip any whitespace
df["GDP"] = pd.to_numeric(df["GDP"], errors='coerce')  # Convert to numeric, coercing errors to NaN

# Check for NaN values and handle them (you might want to drop them or fill them)
print("NaN values in GDP column:", df["GDP"].isna().sum())
df = df.dropna(subset=["GDP"])  # Drop rows where GDP is NaN

# Convert GDP from Million USD to Billion USD and round to 2 decimal places
df["GDP"] = np.round(df["GDP"] / 1000000, 2)

# Sort the DataFrame by GDP in descending order and select the top 10
#df = df.sort_values(by="GDP", ascending=False).head(10)

# Output filename
outfile = "Largest_economies.csv"

# Display the DataFrame
print(df)

# Save the DataFrame to a CSV file
df.to_csv(outfile, index=False)
