import mazegen
import random


if __name__ == "__main__":
    try:
        parameters = mazegen.parser("config.txt")

        entry_tuple = tuple(map(int, parameters["ENTRY"].split(",")))
        exit_tuple = tuple(map(int, parameters["EXIT"].split(",")))

        current_seed = random.randint(1, 100000)

        maze = mazegen.MazeGenerator(
            int(parameters["WIDTH"]),
            int(parameters["HEIGHT"]),
            current_seed,
            entry=entry_tuple,
            exit=exit_tuple
        )

        maze.generate()

        color_options = ["47", "46", "45", "44", "42"]
        color_index = 0
        show_path = False

        while True:
            maze.display(color=color_options[color_index])

            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")

            choice = input("Select an option (1-4): ").strip()

            if choice == "1":
                current_seed = random.randint(1, 100000)
                maze = mazegen.MazeGenerator(
                    int(parameters["WIDTH"]),
                    int(parameters["HEIGHT"]),
                    current_seed,
                    entry=entry_tuple,
                    exit=exit_tuple
                )
                maze.generate()
                print("\n[+] New maze generated!")

            elif choice == "2":
                show_path = not show_path

            elif choice == "3":
                color_index = (color_index + 1) % len(color_options)

            elif choice == "4":

                output_name = parameters["OUTPUT_FILE"]
                entry_name = parameters["ENTRY"]
                exit_name = parameters["EXIT"]
                with open(output_name, "w") as file:
                    for row in maze.maze:
                        hex = "".join(f"{cell:X}" for cell in row)
                        file.write(hex + "\n")
                    file.write("\n")
                    file.write(entry_name)
                    file.write("\n")
                    file.write(exit_name)
                    print(f"\n[+] Maze saved to {output_name}. Goodbye!")
                    break
            else:
                print("\n[-] Invalid choice, please try again.")
    except Exception as e:
        print(f"Error: {e}")
