import mazegen


if __name__ == "__main__":

    try:
        parameters = mazegen.parser("config.txt")
        maze = mazegen.MazeGenerator(int(parameters["WIDTH"]), int(parameters["HEIGHT"]))
        maze.display()
    except Exception as e:
        print(e)