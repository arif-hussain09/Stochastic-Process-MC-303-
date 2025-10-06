import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# --- Part b(i): Fit a Non-Homogeneous Poisson Process (NHPP) ---

def fit_nhpp_piecewise(df, bin_width_hours=1):
    """
    Fits an NHPP with a piecewise-constant intensity function (lambda(t)).
    Estimates are the MLEs for each bin.
    """
    # Convert timestamps to hours from the start of the day
    start_time = df['timestamp'].min().floor('D')
    df['hours'] = (df['timestamp'] - start_time).dt.total_seconds() / 3600
    
    num_bins = int(24 / bin_width_hours)
    bins = np.arange(0, 24 + bin_width_hours, bin_width_hours)
    
    # Count arrivals in each bin
    counts, _ = np.histogram(df['hours'], bins=bins)
    
    # The MLE for lambda in each bin is (number of events) / (time duration)
    lambda_estimates = counts / bin_width_hours
    
    bin_centers = bins[:-1] + bin_width_hours / 2
    
    return lambda_estimates, bin_centers, bin_width_hours

def plot_intensity(lambda_estimates, bin_centers, bin_width, title):
    """Plots the estimated piecewise-constant intensity function."""
    plt.figure(figsize=(12, 7))
    plt.step(bin_centers, lambda_estimates, where='mid', label='Estimated λ(t)', color='b', linewidth=2)
    plt.title(title, fontsize=16)
    plt.xlabel('Hour of Day', fontsize=12)
    plt.ylabel('Estimated Intensity (arrivals/hour)', fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(np.arange(0, 25, 2))
    plt.xlim(0, 24)
    plt.legend()
    plt.show()

# --- Part (c): Model Comparison and Diagnostics ---

def calculate_log_likelihood(df_holdout, lambda_estimates, bin_width_hours):
    """
    Calculates the log-likelihood of the hold-out data given the fitted model.
    The log-likelihood for an NHPP is: sum(log(lambda(t_i))) - integral(lambda(t) dt)
    """
    # Convert holdout timestamps to hours
    start_time = df_holdout['timestamp'].min().floor('D')
    df_holdout['hours'] = (df_holdout['timestamp'] - start_time).dt.total_seconds() / 3600
    
    # Calculate the first term: sum(log(lambda(t_i)))
    def get_lambda_at_time(t):
        bin_index = int(t / bin_width_hours)
        # Ensure index is within bounds
        bin_index = min(bin_index, len(lambda_estimates) - 1)
        return lambda_estimates[bin_index]
    
    log_lambda_sum = np.sum(np.log(df_holdout['hours'].apply(get_lambda_at_time)))
    
    # Calculate the second term: integral of lambda(t) over [0, T]
    # For a piecewise-constant function, this is the sum of lambda_i * width_i
    integral_lambda = np.sum(lambda_estimates * bin_width_hours)
    
    log_likelihood = log_lambda_sum - integral_lambda
    return log_likelihood

def plot_qq_residuals(df, lambda_estimates, bin_width_hours):
    """
    Generates a Q-Q plot for the rescaled inter-arrival times to check the NHPP model fit.
    """
    df_sorted = df.sort_values(by='hours').reset_index(drop=True)
    
    # The 'time rescaling theorem' states that the transformed inter-arrival times
    # should be i.i.d. Exponential(1) variables.
    # The transform is the integral of lambda(t) between arrivals.
    
    def integral_lambda_t(t_start, t_end, lambdas, width):
        start_bin = int(t_start / width)
        end_bin = int(t_end / width)
        
        if start_bin == end_bin:
            return lambdas[start_bin] * (t_end - t_start)
        
        integral = lambdas[start_bin] * (width * (start_bin + 1) - t_start)
        for i in range(start_bin + 1, end_bin):
            integral += lambdas[i] * width
        integral += lambdas[end_bin] * (t_end - width * end_bin)
        return integral

    rescaled_times = []
    for i in range(1, len(df_sorted)):
        t_prev = df_sorted['hours'][i-1]
        t_curr = df_sorted['hours'][i]
        rescaled_inter_arrival = integral_lambda_t(t_prev, t_curr, lambda_estimates, bin_width_hours)
        rescaled_times.append(rescaled_inter_arrival)
        
    plt.figure(figsize=(8, 6))
    stats.probplot(rescaled_times, dist=stats.expon, sparams=(0, 1), plot=plt)
    plt.title('Q-Q Plot of Rescaled Inter-arrival Times vs. Exponential(1)')
    plt.xlabel('Theoretical Quantiles (Exponential)')
    plt.ylabel('Sample Quantiles (Rescaled Times)')
    plt.grid(True)
    plt.show()


# --- Main Execution ---
# Load data
festival_df = pd.read_csv('festival_day.csv', parse_dates=['timestamp'])
regular_df = pd.read_csv('regular_day.csv', parse_dates=['timestamp'])

# 1. Fit NHPP model to festival data
lambdas_fest, bins_fest, width_fest = fit_nhpp_piecewise(festival_df, bin_width_hours=1)
plot_intensity(lambdas_fest, bins_fest, width_fest, 'Estimated Hourly Arrival Intensity - Festival Day')

# 2. Fit NHPP model to regular data for comparison
lambdas_reg, bins_reg, width_reg = fit_nhpp_piecewise(regular_df, bin_width_hours=1)
plot_intensity(lambdas_reg, bins_reg, width_reg, 'Estimated Hourly Arrival Intensity - Regular Day')

# 3. Calculate predictive log-likelihood on hold-out data
# How well does the festival model predict the regular day?
ll_fest_on_reg = calculate_log_likelihood(regular_df, lambdas_fest, width_fest)
# How well does the regular model predict the regular day?
ll_reg_on_reg = calculate_log_likelihood(regular_df, lambdas_reg, width_reg)

print("\n--- Model Comparison ---")
print("Higher log-likelihood indicates a better predictive fit for the hold-out data.")
print(f"Log-Likelihood of Festival Model on Regular Day Data: {ll_fest_on_reg:.2f}")
print(f"Log-Likelihood of Regular Model on Regular Day Data:  {ll_reg_on_reg:.2f}")

# 4. Diagnostic Q-Q Plot for the festival model
plot_qq_residuals(festival_df, lambdas_fest, width_fest)