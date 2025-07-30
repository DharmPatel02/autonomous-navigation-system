import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from GpShip import generate_ship_layout, spread_fire  # Ensure these are correct
from Gpwin import is_winnable  # Import your is_winnable function

# Load the CSV data
data = pd.read_csv('firesimulation.csv')

# Dictionaries to track bot wins in winnable cases
winnable_counts = {}  # Total winnable cases per Q
bot_wins = {f'Bot{i}': {} for i in range(1, 5)}  # Wins per bot in winnable cases

# Iterate through the data
for index, row in data.iterrows():
    q_value = row['Q Value']
    bot_results = {f'Bot{i}': row[f'Bot{i} Result'] for i in range(1, 5)}

    # Ensure dictionaries have entries
    if q_value not in winnable_counts:
        winnable_counts[q_value] = 0
        for i in range(1, 5):
            bot_wins[f'Bot{i}'][q_value] = 0

    # **Check if the simulation was winnable**
    if any(result == 'Success' for result in bot_results.values()):
        is_winnable_case = True  # If any bot succeeded, the case was winnable
    else:
        # **Reconstruct ship layout and fire map**
        size = 40  # Ship size
        ship_layout = generate_ship_layout(size)  # Generate new layout
        fire_map = np.zeros_like(ship_layout)  # Initialize fire map

        # Get positions from CSV (assuming they are saved as strings "(x, y)")
        bot_position = eval(row['Bot1 Position'])
        button_position = eval(row['Button Position'])
        fire_start_x, fire_start_y = eval(row['Fire Position'])

        # Place fire at its starting point
        fire_map[fire_start_x, fire_start_y] = 1

        # Run winnability test
        is_winnable_case = is_winnable(ship_layout, bot_position, button_position, fire_map, q_value)

    # If the case was winnable, record results
    if is_winnable_case:
        winnable_counts[q_value] += 1  # Increment winnable count

        for bot in bot_results:
            if bot_results[bot] == 'Success':
                bot_wins[bot][q_value] += 1  # Count wins per bot

# **Compute the fraction of winnable simulations that each bot won**
bot_success_rates = {f'Bot{i}': {} for i in range(1, 5)}
for i in range(1, 5):
    for q in winnable_counts:
        if winnable_counts[q] > 0:
            bot_success_rates[f'Bot{i}'][q] = bot_wins[f'Bot{i}'][q] / winnable_counts[q]
        else:
            bot_success_rates[f'Bot{i}'][q] = 0  # Avoid division by zero

# **Prepare Data for Plotting**
q_values = sorted(winnable_counts.keys())
plt.figure(figsize=(10, 6))

for i in range(1, 5):
    plt.plot(q_values, [bot_success_rates[f'Bot{i}'][q] for q in q_values],
             marker='o', linestyle='-', label=f'Bot {i}')

# **Plot Winnable Success Rate**
plt.xlabel('Q Value (Flammability)')
plt.ylabel('Fraction of Winnable Simulations Won')
plt.title('Bot Performance in Winnable Simulations')
plt.ylim(0, 1)
plt.legend()
plt.grid(True)
plt.show()
