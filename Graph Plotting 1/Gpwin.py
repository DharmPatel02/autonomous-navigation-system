import numpy as np
import random
from heapq import heappush, heappop
from GpShip import spread_fire

#Calculating the ideal bot using the astar algorithm checking out the condition for winnability
def heuristic(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_shortest_path(grid, start, goal):

    size = len(grid)
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
            if 0 <= neighbor[0] < size and 0 <= neighbor[1] < size and grid[neighbor] == 'O':
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heappush(open_set, (f_score, neighbor))

    if goal not in came_from:
        return None  # No path found

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    return path[::-1]

def is_winnable(grid, bot_position, button_position, fire_map, q):

    # Check if a fire-free path exists at the start
    start_path = find_shortest_path(grid, bot_position, button_position)
    if start_path is None:
        return False  # No possible path even at the beginning

    # Simulate fire spread over time and check if an ideal bot could still win
    fire_sim = np.copy(fire_map)
    for i in range(100):  # Simulate up to 100 steps
        fire_sim = spread_fire(grid, q)
        path = find_shortest_path(grid, bot_position, button_position)
        if path:
            return True  # Winnable, since an optimal bot could reach the button

    return False  # If no path was ever possible, it was not winnable
