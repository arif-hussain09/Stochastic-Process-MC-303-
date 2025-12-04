import numpy as np

# Task 4: Disease Spread with Absorbing State

# Parameters
total_population = 1000
initial_infected = 5
prob_infect = 0.05   # Chance S -> I (per contact/step)
prob_recover = 0.1   # Chance I -> R

# Initial counts
S = total_population - initial_infected
I = initial_infected
R = 0

history = []

print("--- Starting Disease Spread Simulation ---")
print(f"Initial: S={S}, I={I}, R={R}")

step = 0
while I > 0: # Run until no one is infected (Disease dies out)
    step += 1
    
    # 1. Calculate new infections
    # Each Infected person has a chance to infect Susceptible ones
    # Simplified model: New infections = current S * chance they get it from I
    # (Using a basic contact assumption here)
    
    # Probability a single S person gets infected depends on how many I represent
    infection_chance = 1 - (1 - prob_infect)**I 
    new_infected = np.random.binomial(S, infection_chance)
    
    # 2. Calculate recoveries
    new_recovered = np.random.binomial(I, prob_recover)
    
    # Update states
    S -= new_infected
    I = I + new_infected - new_recovered
    R += new_recovered
    
    history.append((S, I, R))

print(f"\nDisease died out after {step} days.")
print(f"Final Stats -> Susceptible: {S}, Infected: {I}, Recovered: {R}")
print(f"Total people who caught the disease: {R + I}") # I should be 0 at end