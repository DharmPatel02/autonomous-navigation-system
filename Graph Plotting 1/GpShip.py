#Importing the necessary libraries and modules
import random
import numpy as np

#Generation of ship

def generate_ship_layout(size):
    grid = np.full((size, size), 'D')
    interior_start = 1
    interior_end =  size - 2
    start_x = random.randint(interior_start, interior_end)
    start_y = random.randint(interior_start, interior_end)
    grid[start_x, start_y] = 'O'

    #Finding out the neighbors

    def get_neighbors(x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []

        for dx, dy in directions:
            neighbors.append((x + dx, y + dy))

        return neighbors

    while True:
        candidates = []

        # Iterate through the ship's interior cells
        for x in range(interior_start, interior_end + 1):
            for y in range(interior_start, interior_end + 1):
                if grid[x, y] == 'D':
                    open_neighbors = sum(1 for nx, ny in get_neighbors(x, y)
                                         if 1 <= nx < size - 1 and 1 <= ny < size - 1 and grid[nx, ny] == 'O')

                    if open_neighbors == 1:
                        candidates.append((x, y))
        if not candidates:
            break
        x, y = random.choice(candidates)
        grid[x, y] = 'O'

    return grid

#Fire Stimulation

def spread_fire(grid, q):
    size = len(grid)
    new_grid = np.copy(grid)

    #Finding the neighbors
    def get_neighbors(x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []

        for dx, dy in directions:
            neighbors.append((x + dx, y + dy))

        return neighbors

    for x in range(1, size - 1):
        for y in range(1, size - 1):
            if grid[x, y] == 'O':
                burning_neighbors = sum(1 for nx, ny in get_neighbors(x, y) if grid[nx, ny] == 'F')
                prob = 1 - (1 - q) ** burning_neighbors
                if burning_neighbors > 0 and random.random() <= prob:
                    new_grid[x, y] = 'F'
    return new_grid
