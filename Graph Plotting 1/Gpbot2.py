from heapq import heappush, heappop
from GpShip import spread_fire
from SaveData1 import save_result

#Calculating out the shortest path using the astar algorithm planning the path in each step
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_shortest_path_astar(grid, start, goal):

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
                if grid[neighbor[0], neighbor[1]] != 'O':
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

#Running out the simulations to calculate the
def run_simulation(size, q, ship_layout, bot_position, button_position, fire_start_x, fire_start_y):

    print(bot_position, button_position, (fire_start_x, fire_start_y))
    start_position=bot_position
    fire_stopped = False
    ship_layout[fire_start_x, fire_start_y] = 'F'

    for i in range(100):
        if ship_layout[button_position[0], button_position[1]] == 'F':
            save_result("Failure", q, "Bot2",start_position, button_position, (fire_start_x, fire_start_y))
            return

        if not fire_stopped:
            ship_layout = spread_fire(ship_layout, q)

        path = find_shortest_path_astar(ship_layout, bot_position, button_position)

        if path is None:
            save_result("Failure", q, "Bot2",start_position, button_position, (fire_start_x, fire_start_y))
            return

        if len(path) > 1:
            bot_position = path[1]

        if bot_position == button_position:
            fire_stopped = True
            save_result("Success", q, "Bot2",start_position, button_position, (fire_start_x, fire_start_y))
            return
