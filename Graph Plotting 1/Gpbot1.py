import random
import numpy as np
from collections import deque
from SaveData1 import save_result

#Fire Spreading code
def spread_fire(grid, q):

    size = len(grid)
    new_grid = np.copy(grid)

    def get_neighbors(x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []

        for dx, dy in directions:
            neighbors.append((x + dx, y + dy))

        return neighbors

    for x in range(1, size - 1):
        for y in range(1, size - 1):
            if grid[x, y] == 'O':  # Fire spreads only in open spaces
                burning_neighbors = sum(1 for nx, ny in get_neighbors(x, y) if grid[nx, ny] == 'F')
                prob = 1 - (1 - q) ** burning_neighbors
                if burning_neighbors > 0 and random.random() <= prob:
                    new_grid[x, y] = 'F'
    return new_grid

#Calculating out the shortest path

def find_shortest_path(grid, start, goal):

    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and (nx, ny) not in came_from and grid[nx, ny] == 'O':
                queue.append((nx, ny))
                came_from[(nx, ny)] = current

    if goal not in came_from:
        return None

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

#Running out the simulations

def run_simulation(size, q, ship_layout, bot_position, button_position, fire_start_x, fire_start_y):

    print(bot_position,button_position,(fire_start_x,fire_start_y))
    fire_stopped = False
    start_position=bot_position
    for i in range(100):
        if ship_layout[button_position[0], button_position[1]] == 'F':
            save_result("Failure", q, "Bot1",start_position, button_position, (fire_start_x, fire_start_y))
            return

        if ship_layout[bot_position[0], bot_position[1]] == 'F':
            save_result("Failure", q, "Bot1",start_position, button_position, (fire_start_x, fire_start_y))
            return


        if not fire_stopped:
            ship_layout = spread_fire(ship_layout, q)

        path = find_shortest_path(ship_layout, bot_position, button_position)

        if path is None:  # No valid path found
            save_result("Failure", q, "Bot1",start_position, button_position, (fire_start_x, fire_start_y))
            return

        if len(path) > 1:
            bot_position = path[1]

        if bot_position == button_position:
            fire_stopped = True
            save_result("Success", q, "Bot1",start_position, button_position, (fire_start_x, fire_start_y))
            return
