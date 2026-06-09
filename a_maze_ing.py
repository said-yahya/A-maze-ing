import mazegen
import random


if __name__ == "__main__":
    try:
        parameters = mazegen.parser("config.txt")
        print(parameters)
        seed = random.seed()
        maze = mazegen.MazeGenerator(
            int(parameters["WIDTH"]),
            int(parameters["HEIGHT"]),
            seed,
        )

        maze.generate()
        maze.display()

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

    except Exception as e:
        print(e)
