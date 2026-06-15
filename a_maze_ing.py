from mazegen import InvalidParameterError, MazeGenerator, parser
import random
import sys


if __name__ == "__main__":
    try:
        if sys.argv[1] != "config.txt":
            raise InvalidParameterError(f"Wrong argument {sys.argv[1]}\n"
                                        "Program must run like 'python3 "
                                        "a_maze_ing.py config.txt'")
        parameters = parser(sys.argv[1])

        if "SEED" in parameters.keys():
            current_seed = parameters["SEED"]
        else:
            current_seed = random.randint(1, 100000)

        maze = MazeGenerator(
            int(parameters["WIDTH"]),
            int(parameters["HEIGHT"]),
            current_seed,
            entry=parameters["ENTRY"],
            exit=parameters["EXIT"]
        )

        themes = [
            {
                "wall": "47",
                "banner": "41",
                "entry": "42",
                "exit": "43",
                "path": "46"
            },
            {
                "wall": "44",
                "banner": "45",
                "entry": "47",
                "exit": "43",
                "path": "42"
            },
            {
                "wall": "46",
                "banner": "41",
                "entry": "45",
                "exit": "47",
                "path": "43"
            },
            {
                "wall": "100",
                "banner": "46",
                "entry": "42",
                "exit": "41",
                "path": "45"
            }
        ]
        theme_index = 0
        show_path = True

        maze.generate(parameters["PERFECT"])

        while True:
            current_theme = themes[theme_index]
            maze.display(
                theme=current_theme,
                show_solution=show_path,
            )

            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")

            choice = input("Select an option (1-4): ").strip()

            if choice == "1":
                current_seed = random.randint(1, 100000)
                maze = MazeGenerator(
                    int(parameters["WIDTH"]),
                    int(parameters["HEIGHT"]),
                    current_seed,
                    entry=parameters["ENTRY"],
                    exit=parameters["EXIT"]
                )
                maze.generate(perfect=parameters["PERFECT"])
                print("\n[+] New maze generated with a new seed!")

            elif choice == "2":
                show_path = not show_path

            elif choice == "3":
                theme_index = (theme_index + 1) % len(themes)
                print(f"\n[+] Switched to Theme {theme_index + 1}")

            elif choice == "4":
                output_name = parameters["OUTPUT_FILE"]
                entry_name: str = f"{parameters["ENTRY"][0]},{parameters["ENTRY"][1]}"
                exit_name: str = f"{parameters["EXIT"][0]},{parameters["EXIT"][1]}"

                solution_path, path_str = maze.solve()

                with open(output_name, "w") as file:
                    for row in maze.maze:
                        hex_row = "".join(f"{cell:X}" for cell in row)
                        file.write(hex_row + "\n")
                    file.write("\n")
                    file.write(entry_name + "\n")
                    file.write(exit_name + "\n")
                    file.write(path_str + "\n")
                    print(f"\n[+] Maze saved to {output_name}. Goodbye!")
                    break
            else:
                print("\n[-] Invalid choice, please try again.")
    except Exception as e:
        print(f"{e}")
