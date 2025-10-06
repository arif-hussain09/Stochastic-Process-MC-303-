import pandas as pd
import numpy as np

# --- Parameters for Simulation ---
LAMBDA_PER_MINUTE = 2.5  # Average call arrival rate
MEAN_REVENUE = 15.0      # Average revenue per call ($)
DAYS = 30                # Observation period

# --- Simulation ---
print("Generating dummy dataset...")

# Total observation time in minutes
T_total_minutes = DAYS * 24 * 60

# We simulate the process by generating the times between arrivals
# For a Poisson process, inter-arrival times are exponentially distributed
mean_inter_arrival_time = 1 / LAMBDA_PER_MINUTE

# To ensure we have enough events, we generate a slightly larger number than expected
# Expected number of calls = LAMBDA_PER_MINUTE * T_total_minutes
num_calls_to_generate = int(LAMBDA_PER_MINUTE * T_total_minutes * 1.1)

# Generate inter-arrival times
inter_arrivals = np.random.exponential(scale=mean_inter_arrival_time, size=num_calls_to_generate)

# Calculate the actual arrival times by taking a cumulative sum
arrival_times_in_minutes = np.cumsum(inter_arrivals)

# Filter out any calls that arrive after the 30-day period ends
final_arrival_times = arrival_times_in_minutes[arrival_times_in_minutes <= T_total_minutes]
actual_num_calls = len(final_arrival_times)

# Convert arrival times in minutes to actual timestamps
start_date = pd.to_datetime('2025-09-01 00:00:00')
timestamps = [start_date + pd.to_timedelta(t, 'm') for t in final_arrival_times]

# Generate random revenues for each call
revenues = np.random.exponential(scale=MEAN_REVENUE, size=actual_num_calls)
revenues = np.round(revenues, 2) # Format to two decimal places for currency

# --- Create DataFrame and Save ---
call_data = pd.DataFrame({
    'timestamp': timestamps,
    'revenue': revenues
})

file_name = 'call_center_data.csv'
call_data.to_csv(file_name, index=False)

print(f"\nSuccessfully created '{file_name}'!")
print(f"Total calls generated: {actual_num_calls}")
print(f"Data spans from {call_data['timestamp'].min()} to {call_data['timestamp'].max()}")

print("\nFirst 5 rows of the dataset:")
print(call_data.head())