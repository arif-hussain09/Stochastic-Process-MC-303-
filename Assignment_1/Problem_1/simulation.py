import numpy as np

# --- Simulation Parameters ---
N = 200           # Absorbing barrier at N
p = 0.49          # Probability of moving right (+1)
q = 1 - p         # Probability of moving left (-1)
NUM_SIMULATIONS = 10000

def simulate_absorption_time(N, p):
    """
    Simulate the time until absorption at N for a single random walk
    with a reflecting barrier at 0.
    """
    state = 0
    steps = 0
    while state < N:
        if state == 0:
            state = 1  # Reflect at 0
        else:
            state += 1 if np.random.rand() < p else -1
        steps += 1
    return steps

# --- Vectorized Simulation ---
print(f"Running {NUM_SIMULATIONS} simulations for N={N}, p={p} ...")
absorption_times = np.array([simulate_absorption_time(N, p) for _ in range(NUM_SIMULATIONS)])

# --- Results ---
mean_time = np.mean(absorption_times)
std_time = np.std(absorption_times)
theoretical_time = N**2  # for symmetric case p = 0.5

# --- Display ---
print("\n--- Simulation Results ---")
print(f"Number of simulations: {NUM_SIMULATIONS}")
print(f"Absorbing state N = {N}")
print(f"Probability p(right) = {p}, q(left) = {q}")
print(f"Estimated probability of absorption at N: 1.0000 (since only absorbing state)")
print(f"Mean absorption time: {mean_time:.2f} steps")
print(f"Std. deviation: {std_time:.2f}")
print(f"Theoretical (p=0.5) mean time ≈ N² = {theoretical_time}")

print("\nAnalysis:")
print("Since p < 0.5, the random walk has a slight drift toward 0 (reflecting barrier).")
print("This increases the expected absorption time compared to the symmetric case.")
