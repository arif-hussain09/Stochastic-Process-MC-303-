import random
import statistics

# Task 2: M/M/1 Queue Simulation

# Setup parameters
lambd = 3.0  # Arrival rate (customers per minute)
mu = 4.0     # Service rate (customers per minute) - must be > lambda for stability

print(f"--- M/M/1 Parameters: Lambda={lambd}, Mu={mu} ---")

# Analytical / Theoretical values to check against
rho = lambd / mu # Utilization
L_theoretical = rho / (1 - rho) # Avg customers in system
W_theoretical = 1 / (mu - lambd) # Avg waiting time

print(f"Theoretical Avg Customers (L): {L_theoretical:.2f}")
print(f"Theoretical Avg Wait Time (W): {W_theoretical:.2f} mins")

# Simulation variables
clock = 0.0
next_arrival = random.expovariate(lambd)
next_departure = float('inf') # Infinite because no one is being served yet
queue = 0
num_in_system_log = [] # To track history
total_wait_times = []
arrivals = [] # store arrival times

max_time = 1000 # Run for 1000 minutes

# Discrete Event Simulation Loop
while clock < max_time:
    
    # Check what happens first: arrival or departure?
    if next_arrival < next_departure:
        # Event: Arrival
        clock = next_arrival
        queue += 1
        arrivals.append(clock)
        
        # Schedule next arrival
        next_arrival = clock + random.expovariate(lambd)
        
        # If this was the only person, schedule their departure immediately
        if queue == 1:
            next_departure = clock + random.expovariate(mu)
            
    else:
        # Event: Departure
        clock = next_departure
        queue -= 1
        
        # Calculate how long this person waited/was in system
        arrival_time = arrivals.pop(0)
        total_wait_times.append(clock - arrival_time)
        
        # Schedule next departure if anyone is left
        if queue > 0:
            next_departure = clock + random.expovariate(mu)
        else:
            next_departure = float('inf')

    # Record system state for stats
    num_in_system_log.append(queue)

# Results
avg_system_size = statistics.mean(num_in_system_log)
avg_wait = statistics.mean(total_wait_times)

print("\n--- Simulation Results ---")
print(f"Simulated Avg Customers (L): {avg_system_size:.2f}")
print(f"Simulated Avg Wait Time (W): {avg_wait:.2f} mins")
print("Note: Simulation results should be close to theoretical values.")