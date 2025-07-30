# Implementing bot 1 using bfs finding the closet path to button
# Importing necessary libraries

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from heapq import heappush, heappop

# Ship Generation code

def generate_ship_layout(ship_size):
    grid = np.full((ship_size, ship_size), 'D')

    ship_start = 1
    ship_end = ship_size - 2
    start_x = random.randint(ship_start, ship_end)
    start_y = random.randint(ship_start, ship_end)
    grid[start_x, start_y] = 'O'  # Open cell

    def get_neighbors(x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []

        for dx, dy in directions:
            neighbors.append((x + dx, y + dy))

        return neighbors

    while True:
        candidates = []

        # Iterate through the ship's interior cells
        for x in range(ship_start, ship_end + 1):
            for y in range(ship_start, ship_end + 1):
                if grid[x, y] == 'D':
                    open_neighbors = sum(1 for nx, ny in get_neighbors(x, y)
                                         if 1 <= nx < ship_size - 1 and 1 <= ny < ship_size - 1 and grid[nx, ny] == 'O')

                    if open_neighbors == 1:
                        candidates.append((x, y))
        if not candidates:
            break
        x, y = random.choice(candidates)
        grid[x, y] = 'O'

    return grid

# Fire Spreading code

def simulate_fire(grid, q):
    ship_size = len(grid)
    new_grid = np.copy(grid)

    def get_neighbors(x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []

        for dx, dy in directions:
            neighbors.append((x + dx, y + dy))

        return neighbors

    for x in range(1, ship_size - 1):
        for y in range(1, ship_size - 1):
            if grid[x, y] == 'O':
                burning_neighbors = sum(1 for nx, ny in get_neighbors(x, y) if grid[nx, ny] == 'F')
                prob = 1 - (1 - q) ** burning_neighbors
                if burning_neighbors > 0 and random.random() <= prob:
                    new_grid[x, y] = 'F'
    return new_grid

# Comparing the position of the bot and the button with fire

def check_failure():
    if ship_layout[button_position[0], button_position[1]] == 'F':
        print("Your bot fails the fire reached the button")
        exit()
    if ship_layout[bot_position[0], bot_position[1]] == 'F':
        print("Your fire reached the bot")
        exit()

# Pathfinding using Dijkstra
def find_safest_path_dijkstra(grid, start, goal, risk_map):
    """Modified Dijkstra's Algorithm for safest pathfinding."""
    open_set = []
    heappush(open_set, (0, start))
    came_from = {start: None}
    g_score = {start: 0}

    while open_set:
        _, current = heappop(open_set)
        if current == goal:
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor] == 'O':
                tentative_g = g_score[current] + risk_map.get(neighbor, 1)
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    heappush(open_set, (tentative_g, neighbor))

    if goal not in came_from:
        return None

    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from[current]
    return path[::-1]

# Risk mapping
def simulated_fire(grid, steps, q):
    """ Simulates fire spread for a given number of steps to estimate future risk areas. """
    simulated_grid = grid.copy()
    for _ in range(steps):
        simulated_grid = simulate_fire(simulated_grid, q)
    return simulated_grid


def compute_risk_map(grid, simulated_grid):
    """ Assigns risk values to each cell based on fire distance and predicted spread. """
    risk_map = {}
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x, y] == 'F':
                risk_map[(x, y)] = float('inf')  # Current fire is extremely risky
            elif simulated_grid[x, y] == 'F':
                risk_map[(x, y)] = 5  # Predicted fire spread is risky
            else:
                risk_map[(x, y)] = 1  # Default low risk
    return risk_map

fire_stopped = False
bot_path_taken = []

# Path Plotting
def update(frame):
    global ship_layout, bot_position, fire_stopped, bot_path_taken

    if q < 0.1:
        step1 = 6
    elif q < 0.3:
        step1 = 4
    elif q < 0.6:
        step1 = 3
    elif q < 0.8:
        step1 = 2
    else:
        step1 = 1

    if not fire_stopped:
        ship_layout = simulate_fire(ship_layout, q)

    check_failure()
    simulated_grid = simulated_fire(ship_layout, steps=step1, q=q)  # Predict fire spread
    risk_map = compute_risk_map(ship_layout, simulated_grid)
    path = find_safest_path_dijkstra(ship_layout, bot_position, button_position, risk_map)


    if path is not None and len(path) > 1:
        bot_position = path[1]
        bot_path_taken.append(bot_position)

        if bot_position == button_position:
            fire_stopped = True
            print("The bot successfully reached the button the fire has stopped from spreading")
            print(f"Path taken by the bot: {bot_path_taken}")
        elif path is None:
            print("The bot is unable to find any path")

#plotting the variables

    plt.clf()
    visual_grid=[]
    for row in ship_layout:
        new_row = []
        for cell in row:
            if cell == 'O' or cell == 'F':
                new_row.append(1)
            else:
                new_row.append(0)
        visual_grid.append(new_row)

    visual_grid = np.array(visual_grid)
    plt.imshow(visual_grid, cmap='gray', interpolation='nearest')

    fire_positions=[]
    for x in range(len(ship_layout)):
        for y in range(len(ship_layout[0])):
            if ship_layout[x,y] == 'F':
                fire_positions.append((x,y))

    plt.scatter(bot_position[1], bot_position[0], color='blue', s=100, marker='o', zorder=5)
    plt.scatter(button_position[1], button_position[0], color='green', s=100, marker='o', zorder=5)

    if fire_positions:
        fire_x, fire_y = zip(*fire_positions)
        plt.scatter(fire_y, fire_x, color='red', s=50, marker='o', zorder=5)

    if path is not None:
        path_x = [p[1] for p in path]
        path_y = [p[0] for p in path]
        plt.plot(path_x, path_y, color='cyan', linewidth=2, zorder=6)

    if fire_stopped:
        plt.title("The bot reached the button successfully")
    else:
        plt.title("Bot is heading towards the button")


    plt.xticks([])
    plt.yticks([])

# Main Function calling
if __name__ == "__main__":

    #Ship size and flammability index
    ship_size = int(input("Enter the size of the shape\n"))
    q = round(random.uniform(0, 1), 2)
    print(f"The rate at which the fire is spreading: {q}")

    ship_layout = generate_ship_layout(ship_size)
    open_cells = []
    for x in range(ship_size):
        for y in range(ship_size):
            if ship_layout[x, y] == 'O':
                open_cells.append((x, y))

    bot_position = random.choice(open_cells)
    button_position = random.choice(open_cells)
    print(f"The starting point of the bot is {bot_position}\nThe destination point of bot is {button_position}")

    fire_start_x, fire_start_y = random.choice(open_cells)
    print(f"The starting point of fire is ({fire_start_x},{fire_start_y})")
    ship_layout[fire_start_x, fire_start_y] = 'F'

# Run animation
fig = plt.figure(figsize=(10, 10))
ani = animation.FuncAnimation(fig, update, frames=300, interval=500, repeat=False)
plt.show()
