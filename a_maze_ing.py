import mazegen
import random

if __name__ == "__main__":
    try:
        parameters = mazegen.parser("config.txt")
        print(parameters)
        seed = random.seed()
        maze = mazegen.MazeGenerator(int(parameters["WIDTH"]), int(parameters["HEIGHT"]), seed)

        maze.generate()
        maze.display()

    except Exception as e:
        print(e)
