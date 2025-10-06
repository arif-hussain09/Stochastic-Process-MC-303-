import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# --- 1. Load Data and Prepare ---
try:
    df = pd.read_csv('stock_price_data.csv')
except FileNotFoundError:
    print("Error: 'stock_price_data.csv' not found. Please run the data generation script first.")
    exit()

# Calculate log-returns
df['log_return'] = np.log(df['price']) - np.log(df['price'].shift(1))
df = df.dropna() # Drop the first row with NaN log_return

log_returns = df['log_return']
n = len(log_returns)

# Define time step (e.g., 1/252 for daily data)
TRADING_DAYS_PER_YEAR = 252
dt = 1 / TRADING_DAYS_PER_YEAR

# --- 2. Implement MLE Estimators ---
# Estimate mean and variance of log-returns
m_hat = log_returns.mean()
v_hat = log_returns.var(ddof=0) # Use ddof=0 for MLE which uses N in denominator

# Calculate mu and sigma
mu_hat = m_hat / dt
sigma_hat = np.sqrt(v_hat / dt)

print("--- Parameter Estimates ---")
print(f"Estimated Annual Drift (μ): {mu_hat:.4f} ({mu_hat*100:.2f}%)")
print(f"Estimated Annual Volatility (σ): {sigma_hat:.4f} ({sigma_hat*100:.2f}%)")


# --- 3. Test Residual Normality ---
# For this model, residuals are the de-meaned log-returns
residuals = log_returns - m_hat

# Perform Shapiro-Wilk test for normality
shapiro_stat, shapiro_p_value = stats.shapiro(residuals)
print("\n--- Normality Test of Residuals ---")
print(f"Shapiro-Wilk Test Statistic: {shapiro_stat:.4f}")
print(f"P-value: {shapiro_p_value:.4f}")

if shapiro_p_value > 0.05:
    print("Conclusion: The p-value is > 0.05, so we fail to reject the null hypothesis of normality.")
else:
    print("Conclusion: The p-value is < 0.05, so we reject the null hypothesis of normality.")

# Create Q-Q plot for visual inspection
plt.figure(figsize=(8, 6))
stats.probplot(residuals, dist="norm", plot=plt)
plt.title('Q-Q Plot of Model Residuals')
plt.xlabel('Theoretical Quantiles (Normal)')
plt.ylabel('Sample Quantiles (Residuals)')
plt.grid(True)
plt.show()