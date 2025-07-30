# Implementing bot 2 using bfs finding the closet path to button
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

    #Finding out the neighbours of the open cells

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

    #Finding neighbours to simulate the fire

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


def check_failure():
    if ship_layout[button_position[0], button_position[1]] == 'F':
        print("Your bot fails the fire reached the button")
        exit()
    if ship_layout[bot_position[0], bot_position[1]] == 'F':
        print("Your fire reached the bot")
        exit()

#Applying manhatten distance to calculate the heuristic
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

#Calculating the shortest path using the astar algorithm
#Calculating path at each step and avoiding fire taking shortest path to the button

def find_shortest_path_astar(grid, start, goal, avoid_fire=True):
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

            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]):

                if grid[neighbor[0], neighbor[1]] != 'O' and (avoid_fire or grid[neighbor[0], neighbor[1]] == 'F'):
                    continue
                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heappush(open_set, (f_score, neighbor))

    if goal not in came_from:
        return None

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


fire_stopped = False
bot_path_taken= []


def update(frame):
    global ship_layout, bot_position, fire_stopped, bot_path_taken

    if not fire_stopped:
        ship_layout = simulate_fire(ship_layout, q)

    check_failure()

    path = find_shortest_path_astar(ship_layout, bot_position, button_position)

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
        plt.title("Bot recalculates the path using A*")


    plt.xticks([])
    plt.yticks([])

#Main function calling passing the interferences
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

fig = plt.figure(figsize=(10, 10))
ani = animation.FuncAnimation(fig, update, frames=300, interval=500, repeat=False)
plt.show()
