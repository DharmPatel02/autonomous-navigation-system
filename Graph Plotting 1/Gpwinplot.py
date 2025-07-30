import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from GpShip import generate_ship_layout, spread_fire  # Ensure these functions are correct
from Gpwin import is_winnable  # Import the winnability test function

# Load the CSV data
data = pd.read_csv('firesimulation.csv')

# Dictionary to track winnable and total cases for each Q value
winnable_counts = {}
total_counts = {}

# Iterate through the data
for index, row in data.iterrows():
    q_value = row['Q Value']
    bot1_result = row['Bot1 Result']
    bot2_result = row['Bot2 Result']
    bot3_result = row['Bot3 Result']
    bot4_result = row['Bot4 Result']

    # Ensure dictionaries have entries
    if q_value not in winnable_counts:
        winnable_counts[q_value] = 0
        total_counts[q_value] = 0

    # If any bot succeeded, the scenario is automatically winnable
    if bot1_result == 'Success' or bot2_result == 'Success' or bot3_result == 'Success' or bot4_result == 'Success':
        winnable_counts[q_value] += 1
    else:
        # **Reconstruct ship layout and fire map**
        size = 40  # Ship size (adjust if different)
        ship_layout = generate_ship_layout(size)  # Generate new layout
        fire_map = np.zeros_like(ship_layout)  # Initialize fire map

        # Get positions from CSV
        bot_position = eval(row['Bot1 Position'])  # Ensure these are saved as strings like "(x, y)"
        button_position = eval(row['Button Position'])
        fire_start_x, fire_start_y = eval(row['Fire Position'])

        # Place fire at its starting point
        fire_map[fire_start_x, fire_start_y] = 1

        # Run winnability test
        is_winnable_case = is_winnable(ship_layout, bot_position, button_position, fire_map, q_value)

        if is_winnable_case:
            winnable_counts[q_value] += 1  # Mark as winnable

    total_counts[q_value] += 1

# Compute percentage of winnable cases
winnability_rates = {q: winnable_counts[q] / total_counts[q] for q in winnable_counts}

# Prepare data for plotting
q_values = sorted(winnability_rates.keys())
winnable_percentages = [winnability_rates[q] for q in q_values]

# **Plot Winnability vs Q**
plt.figure(figsize=(10, 6))
plt.plot(q_values, winnable_percentages, marker='o', linestyle='-', color='g', label='Winnability Rate')

plt.xlabel('Q Value (Flammability)')
plt.ylabel('Percentage of Winnable Simulations')
plt.title('Winnability vs Q Value')
plt.ylim(0, 1)
plt.legend()
plt.grid(True)
plt.show()
