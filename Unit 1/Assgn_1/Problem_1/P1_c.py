import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# --- 1. Load Data and Estimate Lambda ---
try:
    # Assuming the CSV has a column with timestamps
    df = pd.read_csv(r'call_center_data.csv')
    # Make sure the timestamp column is a datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'])
except FileNotFoundError:
    print("Simulating data since 'your_data.csv' was not found.")
    # If no file, create some plausible fake data for demonstration
    # Simulating an average rate of 2.5 calls/min over 30 days
    simulated_rate = 2.5
    T_minutes = 30 * 24 * 60
    num_calls_sim = np.random.poisson(simulated_rate * T_minutes)
    # Generate uniform arrival times and sort them
    arrival_times_minutes = np.sort(np.random.uniform(0, T_minutes, num_calls_sim))
    start_time = pd.to_datetime('2025-10-01 00:00:00')
    timestamps = [start_time + pd.to_timedelta(t, 'm') for t in arrival_times_minutes]
    df = pd.DataFrame({'timestamp': timestamps})


# --- 2. Calculate n and T ---
n_calls = len(df)
T_minutes = 30 * 24 * 60 # Total observation time in minutes

# Calculate the MLE for lambda (calls per minute)
lambda_hat = n_calls / T_minutes

print(f"Total calls observed (n): {n_calls}")
print(f"Total time in minutes (T): {T_minutes}")
print(f"Estimated MLE for lambda (λ_hat): {lambda_hat:.4f} calls/minute")

# --- 3. Calculate 95% Confidence Interval ---
se_lambda = np.sqrt(lambda_hat / T_minutes)
z_score = 1.96
ci_lower = lambda_hat - z_score * se_lambda
ci_upper = lambda_hat + z_score * se_lambda

print(f"95% Confidence Interval for λ: [{ci_lower:.4f}, {ci_upper:.4f}]")

# --- 4. Assumption Check: Inter-arrival Times ---
# Sort by timestamp just in case they are not ordered
df = df.sort_values(by='timestamp').reset_index(drop=True)

# Calculate inter-arrival times in minutes
inter_arrival_times = df['timestamp'].diff().dt.total_seconds().div(60).dropna()

# --- 5. Generate Q-Q Plot ---
plt.figure(figsize=(8, 6))
# Compare inter-arrival times to an exponential distribution
# The 'scale' parameter for stats.expon is 1/lambda
stats.probplot(inter_arrival_times, dist=stats.expon, sparams=(0, 1/lambda_hat), plot=plt)
plt.title('Q-Q Plot of Inter-arrival Times vs. Exponential Distribution')
plt.xlabel('Theoretical Quantiles (Exponential)')
plt.ylabel('Sample Quantiles (Observed Inter-arrival Times)')
plt.grid(True)
plt.show()