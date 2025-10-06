import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_arrivals_from_intensity(intensity_func, day_name_str, plot_intensity=False):
    """
    Generates arrival timestamps for a non-homogeneous Poisson process (NHPP)
    using a given intensity function lambda(t). This method uses the 'thinning'
    or 'acceptance-rejection' algorithm.

    Args:
        intensity_func (function): A function lambda(t) that returns the arrival rate at time t (in hours).
        day_name_str (str): The base name for the output file (e.g., 'festival_day').
        plot_intensity (bool): If True, displays a plot of the intensity and generated data.
    """
    print(f"Generating arrival data for '{day_name_str}'...")

    # Find the maximum intensity rate over the 24-hour period to use as lambda_max for the homogeneous process.
    t_values = np.linspace(0, 24, 1000)
    lambda_max = np.max(intensity_func(t_values)) * 1.1 # Add a 10% buffer

    # Generate a set of arrivals from a homogeneous Poisson process with the max rate.
    # The expected number of arrivals is lambda_max * 24. We generate more to be safe.
    num_candidates = np.random.poisson(lambda_max * 24)
    candidate_arrivals_hours = np.random.uniform(0, 24, size=num_candidates)

    # Thin the homogeneous process to get the non-homogeneous arrivals.
    # An arrival at time t is kept with probability lambda(t) / lambda_max.
    acceptance_probabilities = intensity_func(candidate_arrivals_hours) / lambda_max
    accepted_mask = np.random.rand(num_candidates) < acceptance_probabilities

    final_arrivals_hours = np.sort(candidate_arrivals_hours[accepted_mask])

    # Convert the accepted arrival times (in hours) to full timestamps for a specific date.
    day_offset = 1 if 'festival' in day_name_str else 2
    start_date = pd.to_datetime(f'2025-07-{day_offset}')
    timestamps = [start_date + pd.to_timedelta(t, 'h') for t in final_arrivals_hours]

    # Create and save the DataFrame.
    df = pd.DataFrame({'timestamp': timestamps})
    file_path = f'{day_name_str}.csv'
    df.to_csv(file_path, index=False)

    print(f"-> Successfully generated {len(df)} arrivals and saved to '{file_path}'")

    # Optionally plot the true intensity function and the density of the generated arrivals.
    if plot_intensity:
        plt.figure(figsize=(12, 6))
        plt.plot(t_values, intensity_func(t_values), 'r-', linewidth=2, label='True Intensity Function λ(t)')
        plt.hist(final_arrivals_hours, bins=48, density=True, alpha=0.7, label='Density of Simulated Arrivals')
        plt.title(f'Arrival Intensity Profile: {day_name_str.replace("_", " ").title()}', fontsize=16)
        plt.xlabel('Hour of Day', fontsize=12)
        plt.ylabel('Intensity (arrivals/hour)', fontsize=12)
        plt.legend()
        plt.grid(True, linestyle='--')
        plt.xlim(0, 24)
        plt.xticks(np.arange(0, 25, 2))
        plt.show()

# --- Define Intensity Functions (lambda(t) in arrivals/hour) ---

def festival_intensity(t):
    """Intensity for a festival day: low base, a huge evening spike for the main event, and a smaller late-night spike as people leave."""
    # Base rate of arrivals
    base = 50
    # Main event spike (e.g., concert from 7 PM to 10 PM, peaking at 8:30 PM)
    main_event_spike = 800 * np.exp(-((t - 20.5)**2) / (2 * 1.5**2))
    # Late-night leaving spike (peaking around 1 AM)
    leaving_spike = 300 * np.exp(-((t - 1)**2) / (2 * 1.0**2))
    return base + main_event_spike + leaving_spike

def regular_intensity(t):
    """Intensity for a regular day: morning and evening commute peaks."""
    # Base rate of arrivals
    base = 40
    # Morning commute (peaking at 8:30 AM)
    morning_peak = 200 * np.exp(-((t - 8.5)**2) / (2 * 1.0**2))
    # Evening commute (peaking at 5:30 PM)
    evening_peak = 250 * np.exp(-((t - 17.5)**2) / (2 * 1.5**2))
    return base + morning_peak + evening_peak

# --- Main script execution ---
if __name__ == "__main__":
    # Generate the data and create the plots for visualization
    generate_arrivals_from_intensity(festival_intensity, 'festival_day', plot_intensity=True)
    generate_arrivals_from_intensity(regular_intensity, 'regular_day', plot_intensity=True)
    print("\nData generation complete.")
