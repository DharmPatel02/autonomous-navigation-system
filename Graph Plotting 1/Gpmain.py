#importing all libraries and modules

import random
from GpShip import generate_ship_layout
from Gpbot1 import run_simulation as run_bot1
from Gpbot2 import run_simulation as run_bot2
from Gpbot3 import run_simulation as run_bot3
from Gpbot4 import run_simulation as run_bot4


#main function calling

if __name__ == "__main__":
    size = 40

    #Number of tuples

    num_runs = 20
    q_values = [round(i * 0.1, 2) for i in range(1, 10)]

    for q in q_values:
        for _ in range(num_runs):

            ship_layout = generate_ship_layout(size)
            open_cells = [(x, y) for x in range(size) for y in range(size) if ship_layout[x, y] == 'O']

            # Selecting randomly the choice of bot position, button,and the fire starting point for all bots

            bot_position = random.choice(open_cells)
            button_position = random.choice(open_cells)
            fire_start_x, fire_start_y = random.choice(open_cells)


            ship_layout[fire_start_x, fire_start_y] = 'F'

            # Calling Bot1
            run_bot1(size, q, ship_layout.copy(), bot_position, button_position, fire_start_x, fire_start_y)

            # Calling Bot2
            run_bot2(size, q, ship_layout.copy(), bot_position, button_position, fire_start_x, fire_start_y)

            # Calling Bot3
            run_bot3(size, q, ship_layout.copy(), bot_position, button_position, fire_start_x, fire_start_y)

            # Calling Bot4
            run_bot4(size, q, ship_layout.copy(), bot_position, button_position, fire_start_x, fire_start_y)

    print("All Simulations completed for all values of Flammability Index")
