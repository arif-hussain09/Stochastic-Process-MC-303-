import matplotlib.pyplot as plt
import random

# Task 3: Birth-Death Process

# Parameters
beta = 0.5  # Birth rate
delta = 0.5 # Death rate (Equal rates usually mean fluctuation around initial)
initial_pop = 20
max_iter = 500

population = [initial_pop]
curr_pop = initial_pop

print(f"Starting simulation with population: {initial_pop}")

for t in range(max_iter):
    if curr_pop == 0:
        # Extinction event
        population.append(0)
        continue

    # In a small time step, check for birth OR death
    # We generate a random number. 
    # Probability of birth is roughly proportional to beta * N
    # This is a simplified discrete step approach
    
    change = 0
    
    # Check for birth
    if random.random() < (beta * 0.1 * curr_pop): 
        change += 1
        
    # Check for death
    if random.random() < (delta * 0.1 * curr_pop): 
        change -= 1
        
    curr_pop += change
    
    # Prevent negative population (just in case)
    if curr_pop < 0: curr_pop = 0
        
    population.append(curr_pop)

avg_pop = sum(population) / len(population)
print(f"Simulation ended. Final Population: {curr_pop}")
print(f"Average Population over time: {avg_pop:.2f}")

# Note: You can plot 'population' list using matplotlib if needed
# plt.plot(population)
# plt.show()