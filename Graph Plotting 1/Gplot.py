import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data into a DataFrame
data = pd.read_csv('firesimulation.csv', usecols=['Q Value', 'Bot1 Result', 'Bot2 Result', 'Bot3 Result', 'Bot4 Result'])

# Initialize dictionaries to store success counts and total attempts for all bots
success_counts = {"Bot1": {}, "Bot2": {}, "Bot3": {}, "Bot4": {}}
total_attempts = {"Bot1": {}, "Bot2": {}, "Bot3": {}, "Bot4": {}}

# Iterate through the data and count successes and attempts for each Q value
for index, row in data.iterrows():
    q_value = row['Q Value']

    for bot in ["Bot1", "Bot2", "Bot3", "Bot4"]:
        bot_result = row[f'{bot} Result']

        if q_value not in success_counts[bot]:
            success_counts[bot][q_value] = 0
            total_attempts[bot][q_value] = 0

        if bot_result == 'Success':
            success_counts[bot][q_value] += 1
        total_attempts[bot][q_value] += 1

# Calculate success rates for all bots
success_rates = {
    bot: {q: success_counts[bot][q] / total_attempts[bot][q] for q in success_counts[bot]}
    for bot in ["Bot1", "Bot2", "Bot3", "Bot4"]
}

# Prepare data for plotting
q_values = sorted(data['Q Value'].unique())
bot1_success_rates = [success_rates["Bot1"].get(q, 0) for q in q_values]
bot2_success_rates = [success_rates["Bot2"].get(q, 0) for q in q_values]
bot3_success_rates = [success_rates["Bot3"].get(q, 0) for q in q_values]
bot4_success_rates = [success_rates["Bot4"].get(q, 0) for q in q_values]

# Plot the graph for Bot1, Bot2, Bot3, and Bot4
plt.figure(figsize=(10, 6))
plt.plot(q_values, bot1_success_rates, marker='o', linestyle='-', label='Bot1 Success Rate')
plt.plot(q_values, bot2_success_rates, marker='s', linestyle='-', label='Bot2 Success Rate')
plt.plot(q_values, bot3_success_rates, marker='^', linestyle='-', label='Bot3 Success Rate')
plt.plot(q_values, bot4_success_rates, marker='d', linestyle='-', label='Bot4 Success Rate')

# Graph settings
plt.xlabel('Q Value')
plt.ylabel('Success Rate')
plt.title('Success Rate vs Q Value for All Bots')
plt.ylim(0, 1)
plt.legend()
plt.grid(True)
plt.show()
