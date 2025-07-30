import csv
import os

#Using the file and storing it in variable
file_path = "firesimulation.csv"

# Using the dictionary to temporarily store bot results before writing to CSV
results_dict = {}

def save_result(result, q, bot_name, bot_position, button_position, fire_position):
   #Stores the result in the memory and store the values of each bot in one row
    global results_dict

    # Initialize entry for Q value if not present
    if q not in results_dict:
        results_dict[q] = {
            "Bot1": None, "Bot1 Pos": None,
            "Bot2": None, "Bot2 Pos": None,
            "Bot3": None, "Bot3 Pos": None,
            "Bot4": None, "Bot4 Pos": None,
            "Button Pos": str(button_position),
            "Fire Pos": str(fire_position)
        }

    # Assign the result to the corresponding bot
    results_dict[q][bot_name] = result
    results_dict[q][f"{bot_name} Pos"] = str(bot_position)  # Store bot position as a string

    # If all bots have results, write to CSV and print
    if all(results_dict[q].values()):
        write_to_csv(
            q, results_dict[q]["Bot1"], results_dict[q]["Bot1 Pos"],
            results_dict[q]["Bot2"], results_dict[q]["Bot2 Pos"],
            results_dict[q]["Bot3"], results_dict[q]["Bot3 Pos"],
            results_dict[q]["Bot4"], results_dict[q]["Bot4 Pos"],
            results_dict[q]["Button Pos"], results_dict[q]["Fire Pos"]
        )
        print_results(
            q, results_dict[q]["Bot1"], results_dict[q]["Bot1 Pos"],
            results_dict[q]["Bot2"], results_dict[q]["Bot2 Pos"],
            results_dict[q]["Bot3"], results_dict[q]["Bot3 Pos"],
            results_dict[q]["Bot4"], results_dict[q]["Bot4 Pos"],
            results_dict[q]["Button Pos"], results_dict[q]["Fire Pos"]
        )
        del results_dict[q]  # Free memory after writing

def write_to_csv(q, bot1_result, bot1_position, bot2_result, bot2_position,
                 bot3_result, bot3_position, bot4_result, bot4_position,
                 button_pos, fire_pos):

   # Writes results of all bots in a single row when all results are available.
    #Ensures headers are written correctly.

    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write headers only if the file does not exist or is empty
        if not file_exists or os.stat(file_path).st_size == 0:
            writer.writerow([
                "Q Value", "Bot1 Result", "Bot1 Position",
                "Bot2 Result", "Bot2 Position",
                "Bot3 Result", "Bot3 Position",
                "Bot4 Result", "Bot4 Position",
                "Button Position", "Fire Position"
            ])

        # Write the new result row
        writer.writerow([
            q, bot1_result, bot1_position,
            bot2_result, bot2_position,
            bot3_result, bot3_position,
            bot4_result, bot4_position,
            button_pos, fire_pos
        ])

def print_results(q, bot1_result, bot1_position, bot2_result, bot2_position,
                  bot3_result, bot3_position, bot4_result, bot4_position,
                  button_pos, fire_pos):

    #Prints the results of all bots after each run.

    print(f"\n Simulation for Q = {q} ")
    print(f"Bot1 Result: {bot1_result} | Position: {bot1_position}")
    print(f"Bot2 Result: {bot2_result} | Position: {bot2_position}")
    print(f"Bot3 Result: {bot3_result} | Position: {bot3_position}")
    print(f"Bot4 Result: {bot4_result} | Position: {bot4_position}")
    print(f"Button Position: {button_pos} |  Fire Start Position: {fire_pos}")
    print("-" * 50)
