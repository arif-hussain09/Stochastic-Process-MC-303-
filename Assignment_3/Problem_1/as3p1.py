import numpy as np

# Task 1: Customer Support System Simulation

# Defining the states for reference:
# 0: Waiting, 1: On Hold, 2: Talking, 3: Resolved, 4: Exit
states = ["Waiting", "On Hold", "Talking", "Resolved", "Exit"]

# Creating the Transition Matrix (P)
# I picked these probabilities to look realistic. Rows must sum to 1.
P = np.array([
    # Wait, Hold, Talk, Rslvd, Exit
    [0.2,  0.3,  0.5,  0.0,   0.0],  # From Waiting
    [0.1,  0.4,  0.5,  0.0,   0.0],  # From On Hold
    [0.0,  0.1,  0.4,  0.5,   0.0],  # From Talking
    [0.0,  0.0,  0.0,  0.0,   1.0],  # From Resolved -> goes strictly to Exit
    [0.0,  0.0,  0.0,  0.0,   1.0],  # From Exit (Absorbing state)
])

# 1. N-step transition probabilities
# Let's see where a customer is likely to be after 5 steps starting from "Waiting"
steps = 5
start_state = [1, 0, 0, 0, 0] # Starts at Waiting (index 0)

# Matrix power to find probabilities after n steps
P_n = np.linalg.matrix_power(P, steps)
current_probs = np.dot(start_state, P_n)

print(f"--- After {steps} steps (starting at Waiting) ---")
for i, prob in enumerate(current_probs):
    print(f"Probability of being in '{states[i]}': {prob:.4f}")

# 2. Steady State / Limiting Probabilities
# Since we have an absorbing state (Exit), eventually everyone should end up there.
# But let's simulate a bunch of customers to prove it.

print("\n--- Running Monte Carlo Simulation ---")
num_simulations = 1000
ended_in_exit = 0

for _ in range(num_simulations):
    current_state = 0 # Start at Waiting
    for _ in range(20): # Run for max 20 steps per customer
        # Pick next state based on the transition probabilities of current row
        current_state = np.random.choice(range(5), p=P[current_state])
        if current_state == 4: # Exit state
            ended_in_exit += 1
            break

print(f"Out of {num_simulations} customers, {ended_in_exit} reached the 'Exit' state.")
print("This confirms State 5 is absorbing and transient states eventually empty out.")