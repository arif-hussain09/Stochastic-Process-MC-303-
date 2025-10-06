import pandas as pd
import numpy as np

# --- Parameters for Simulation ---
S0 = 150.0       # Initial stock price
MU_ANNUAL = 0.15   # Expected annual return (drift)
SIGMA_ANNUAL = 0.25 # Annual volatility
YEARS = 1
TRADING_DAYS = 252

# --- Simulation ---
print("Generating dummy stock price data...")

# Time step
dt = 1 / TRADING_DAYS
n_steps = int(TRADING_DAYS * YEARS)

# Generate random shocks from a standard normal distribution
random_shocks = np.random.normal(0, 1, n_steps)

# Generate price path using the discrete GBM formula
price_path = [S0]
current_price = S0
for i in range(n_steps):
    # This is the discrete solution to the GBM SDE
    drift = (MU_ANNUAL - 0.5 * SIGMA_ANNUAL**2) * dt
    shock = SIGMA_ANNUAL * np.sqrt(dt) * random_shocks[i]
    current_price *= np.exp(drift + shock)
    price_path.append(current_price)

# Create a DataFrame
dates = pd.to_datetime('2024-01-01') + pd.to_timedelta(np.arange(n_steps + 1), 'd')
stock_data = pd.DataFrame({
    'date': dates,
    'price': price_path
})

# Save to CSV
file_name = 'stock_price_data.csv'
stock_data.to_csv(file_name, index=False)

print(f"\nSuccessfully created '{file_name}'!")
print(f"Simulated data for {n_steps} trading days.")
print("\nFirst 5 rows of the dataset:")
print(stock_data.head())

# Plot the generated data for visualization
stock_data.plot(x='date', y='price', title='Simulated Stock Price (GBM)', grid=True)
import matplotlib.pyplot as plt
plt.ylabel('Stock Price ($)')
plt.show()