from heapq import heappush, heappop
from GpShip import spread_fire
from SaveData1 import save_result

#Calculating out the shortest path while calculating the risk awareness predicting using the flammability index using different values of q
#how far the fire will spread
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def simulate_fire(grid, steps, q):

    simulated_grid = grid.copy()
    for _ in range(steps):
        simulated_grid = spread_fire(simulated_grid, q)
    return simulated_grid


def compute_risk_map(grid, simulated_grid):

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


def find_safest_path_dijkstra(grid, start, goal, risk_map):
    #Modifying the algorithm based on the risk awareness that we have computed above
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
                tentative_g = g_score[current] + risk_map.get(neighbor, 1)
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    heappush(open_set, (tentative_g, neighbor))

    if goal not in came_from:
        return None

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

#Running the simulation to store the bot conditions
def run_simulation(size, q, ship_layout, bot_position, button_position, fire_start_x, fire_start_y):

    print(bot_position, button_position, (fire_start_x, fire_start_y))
    fire_stopped = False
    ship_layout[fire_start_x, fire_start_y] = 'F'

    # Calculate prediction steps based on q value
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

    for _ in range(100):  # Limit to 100 steps max
        if ship_layout[button_position[0], button_position[1]] == 'F':
            save_result("Failure", q, "Bot4")
            return

        if not fire_stopped:
            ship_layout = spread_fire(ship_layout, q)

        simulated_grid = simulate_fire(ship_layout, steps=step1, q=q)  # Predict fire spread
        risk_map = compute_risk_map(ship_layout, simulated_grid)
        path = find_safest_path_dijkstra(ship_layout, bot_position, button_position, risk_map)

        if path is None:
            save_result("Failure", q, "Bot4")
            return

        if len(path) > 1:
            bot_position = path[1]

        if bot_position == button_position:
            fire_stopped = True
            save_result("Success", q, "Bot4")
            return



'''
from heapq import heappush, heappop
from GpShip import spread_fire
from SaveData1 import save_result


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def simulate_fire(grid, steps, q):
    """ Simulates fire spread for a given number of steps to estimate future risk areas. """
    simulated_grid = grid.copy()
    for _ in range(steps):
        simulated_grid = spread_fire(simulated_grid, q)
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


def find_safest_path_dijkstra(grid, start, goal, risk_map):
    """ Modified Dijkstra's Algorithm with risk-aware pathfinding. """
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
                tentative_g = g_score[current] + risk_map.get(neighbor, 1)
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    heappush(open_set, (tentative_g, neighbor))

    if goal not in came_from:
        return None

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def run_simulation(size, q, ship_layout, bot_position, button_position, fire_start_x, fire_start_y):
    """
    Runs the simulation for Bot4 with predictive fire-aware navigation.
    """
    print(bot_position, button_position, (fire_start_x, fire_start_y))
    fire_stopped = False
    ship_layout[fire_start_x, fire_start_y] = 'F'

    for _ in range(100):  # Limit to 100 steps max
        if ship_layout[button_position[0], button_position[1]] == 'F':
            save_result("Failure", q, "Bot4")
            return

        if not fire_stopped:
            ship_layout = spread_fire(ship_layout, q)

        simulated_grid = simulate_fire(ship_layout, steps=3, q=q)  # Predict fire spread
        risk_map = compute_risk_map(ship_layout, simulated_grid)
        path = find_safest_path_dijkstra(ship_layout, bot_position, button_position, risk_map)

        if path is None:
            save_result("Failure", q, "Bot4")
            return

        if len(path) > 1:
            bot_position = path[1]

        if bot_position == button_position:
            fire_stopped = True
            save_result("Success", q, "Bot4")
            return

'''