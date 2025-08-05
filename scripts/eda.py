import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('../data/raw/BrentOilPrices.csv')
data['Date'] = pd.to_datetime(data['Date'], format='mixed', dayfirst=True, errors='coerce')
data = data.sort_values('Date')

# Check for invalid dates
if data['Date'].isna().any():
    print("Warning: Some dates could not be parsed:")
    print(data[data['Date'].isna()])

# Compute log returns
data['Log_Returns'] = np.log(data['Price']).diff()

# Plot price series
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Price'], label='Brent Oil Price (USD)')
plt.title('Brent Oil Prices (1987-2022)')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.savefig('../outputs/price_series.png')
plt.close()

# Plot log returns
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Log_Returns'], label='Log Returns')
plt.title('Log Returns of Brent Oil Prices')
plt.xlabel('Date')
plt.ylabel('Log Returns')
plt.legend()
plt.savefig('../outputs/log_returns.png')
plt.close()