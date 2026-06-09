MIN_WIDTH = 1
MIN_HEIGHT = 1
MAX_WIDTH = 100
MAX_HEIGHT = 100


def parser(filename: str) -> dict:
    def banner(width: int, height: int) -> list[tuple[int, int]]:
        x: int = 0
        y: int = 0
        if width % 2 == 0:
            x = width // 2 - 1
        else:
            x = width // 2
        if height % 2 == 0:
            y = height // 2 - 1
        else:
            y = height // 2
        ft_banner: list[tuple[int, int]] = [
            (x - 1, y), (x - 2, y), (x - 3, y),
            (x - 3, y - 1), (x - 3, y - 2),
            (x - 1, y + 1), (x - 1, y + 2),
            (x + 1, y), (x + 2, y), (x + 3, y),
            (x + 3, y - 1), (x + 3, y - 2),
            (x + 2, y - 2), (x + 1, y - 2),
            (x + 1, y + 1), (x + 1, y + 2),
            (x + 2, y + 2), (x + 3, y + 2)
        ]
        return ft_banner
    parameters: dict[str, str] = {}
    keys: set[str] = {"WIDTH", "HEIGHT", "ENTRY", "EXIT",
                      "PERFECT", "OUTPUT_FILE"}
    with open(filename, 'r') as f:
        args: list[str] = (f.read()).splitlines()
    for arg in args:
        argument: str = arg.strip()
        if argument.startswith("#") or argument == "":
            continue
        elif "=" in argument:
            key, value = argument.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key in keys:
                parameters.update({key: value})
            else:
                raise ValueError(f"Unknown parameter: {key}")
        else:
            raise ValueError(f"Invalid line in config file: {argument}")

    if parameters["WIDTH"]:
        if parameters["WIDTH"].isdigit():
            if MIN_WIDTH <= int(parameters["WIDTH"]) <= MAX_WIDTH:
                pass
            else:
                raise ValueError(f"WIDTH must be between {MIN_WIDTH} "
                                 f"and {MAX_WIDTH}.")
        else:
            raise ValueError("WIDTH must be an integer.")
    else:
        raise ValueError("WIDTH parameter is missing.")

    if parameters["HEIGHT"]:
        if parameters["HEIGHT"].isdigit():
            if MIN_HEIGHT <= int(parameters["HEIGHT"]) <= MAX_HEIGHT:
                pass
            else:
                raise ValueError(f"HEIGHT must be between {MIN_HEIGHT} "
                                 f"and {MAX_HEIGHT}.")
        else:
            raise ValueError("HEIGHT must be an integer.")
    else:
        raise ValueError("HEIGHT parameter is missing.")

    if parameters["ENTRY"]:
        try:
            x, y = parameters["ENTRY"].split(",")
        except ValueError:
            raise ValueError("ENTRY have to have 2 parameters as x, y")
        x = x.strip()
        y = y.strip()
        if x.isdigit() and y.isdigit():
            if (
                0 <= int(x) < int(parameters["WIDTH"])
                and 0 <= int(y) < int(parameters["HEIGHT"])
            ):
                if (int(parameters["HEIGHT"]) <= 6 or
                        int(parameters["WIDTH"]) <= 8):
                    ft_banner = banner(int(parameters["WIDTH"]),
                                       int(parameters["HEIGHT"]))
                    if (int(x), int(y)) in ft_banner:
                        raise ValueError("ENTRY coordinates cannot be on "
                                         "42 banner coordinates!")
            else:
                raise ValueError("ENTRY coordinates must be within"
                                 " the maze dimensions.")
        else:
            raise ValueError("ENTRY coordinates must be integers.")
    else:
        raise ValueError("ENTRY parameter is missing.")

    if parameters["EXIT"]:
        try:
            x, y = parameters["EXIT"].split(",")
        except ValueError:
            raise ValueError("EXIT have to have 2 parameters as x, y")
        x = x.strip()
        y = y.strip()
        if x.isdigit() and y.isdigit():
            if (
                0 <= int(x) < int(parameters["WIDTH"])
                and 0 <= int(y) < int(parameters["HEIGHT"])
            ):
                if (int(parameters["HEIGHT"]) <= 6 or
                        int(parameters["WIDTH"]) <= 8):
                    ft_banner = banner(int(parameters["WIDTH"]),
                                       int(parameters["HEIGHT"]))
                    if (int(x), int(y)) in ft_banner:
                        raise ValueError("EXIT coordinates cannot be on "
                                         "42 banner coordinates!")
            else:
                raise ValueError("EXIT coordinates must be within"
                                 " the maze dimensions.")
        else:
            raise ValueError("EXIT coordinates must be integers.")
    else:
        raise ValueError("EXIT parameter is missing.")

    if parameters["PERFECT"]:
        if parameters["PERFECT"].lower() in ["true", "false"]:
            pass
        else:
            raise ValueError("PERFECT must be 'true' or 'false'.")
    else:
        raise ValueError("PERFECT parameter is missing.")

    if parameters["OUTPUT_FILE"]:
        if parameters["OUTPUT_FILE"].endswith(".txt"):
            pass
        else:
            raise ValueError("OUTPUT_FILE must end with .txt.")
    else:
        raise ValueError("OUTPUT_FILE parameter is missing.")

    x1, y1 = parameters["ENTRY"].split(",")
    x2, y2 = parameters["EXIT"].split(",")
    if int(x1) == int(x2) and int(y1) == int(y2):
        raise ValueError("ENTRY and EXIT cannot be at the same coordinates.")

    if int(parameters["HEIGHT"]) < 6 or int(parameters["WIDTH"]) < 8:
        print("Maze too small to implement 42 Banner!")

    return parameters
