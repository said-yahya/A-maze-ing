from typing import Any


MIN_WIDTH = 2
MIN_HEIGHT = 2
MAX_WIDTH = 200
MAX_HEIGHT = 200


class InvalidParameterError(Exception):
    def __init__(self, message: str = "Provided parameter is invalid"):
        self.message = message
        super().__init__(self.message)


class MissingParameterError(Exception):
    def __init__(self, message: str = "Parameter has missed"):
        self.message = message
        super().__init__(self.message)


def parser(filename: str) -> dict[str, Any]:
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
    parameters: dict[str, Any] = {}
    keys: set[str] = {"WIDTH", "HEIGHT", "ENTRY", "EXIT",
                      "PERFECT", "OUTPUT_FILE", "SEED"}
    with open(filename, 'r') as f:
        args: list[str] = (f.read()).splitlines()
    for arg in args:
        argument: str = arg.strip()
        if argument.startswith("#") or argument == "":
            continue
        elif "=" in argument:
            key, value = argument.split("=", 1)
            key = key.strip()
            if "#" in value:
                value = value.split("#")[0]
            value = value.strip()
            if key in keys:
                if key in parameters:
                    raise InvalidParameterError("Duplicate parameter found: "
                                                f"{key}")
                parameters.update({key: value})
            else:
                raise InvalidParameterError(f"Unknown parameter: {key}")
        else:
            raise InvalidParameterError("Invalid line in config "
                                        f"file: {argument}")

    parameters_keys = parameters.keys()

    if "WIDTH" in parameters_keys:
        try:
            width_value = int(parameters["WIDTH"])
        except ValueError:
            raise InvalidParameterError("WIDTH must be equal to just one "
                                        "integer.")

        if MIN_WIDTH <= width_value <= MAX_WIDTH:
            parameters["WIDTH"] = width_value
        else:
            raise InvalidParameterError("WIDTH must be between "
                                        f"{MIN_WIDTH} and {MAX_WIDTH}.")
    else:
        raise MissingParameterError("WIDTH parameter is missing.")

    if "HEIGHT" in parameters_keys:
        try:
            heidht_value = int(parameters["HEIGHT"])
        except ValueError:
            raise InvalidParameterError("HEIGHT must be equal to just one "
                                        "integer.")

        if MIN_HEIGHT <= heidht_value <= MAX_HEIGHT:
            parameters["HEIGHT"] = heidht_value
        else:
            raise InvalidParameterError("HEIGHT must be between "
                                        f"{MIN_HEIGHT} and {MAX_HEIGHT}.")
    else:
        raise MissingParameterError("HEIGHT parameter is missing.")

    ft_banner = banner(parameters["WIDTH"], parameters["HEIGHT"])

    if "ENTRY" in parameters_keys:
        try:
            x, y = parameters["ENTRY"].split(",")
        except ValueError:
            raise InvalidParameterError("ENTRY have to have 2 parameters as "
                                        "x, y")
        try:
            x = int(x.strip())
            y = int(y.strip())
            if (0 <= x < parameters["WIDTH"]) and \
               (0 <= y < parameters["HEIGHT"]):
                if parameters["HEIGHT"] > 5 and parameters["WIDTH"] > 7:
                    if (x, y) in ft_banner:
                        raise InvalidParameterError("ENTRY coordinates cannot"
                                                    " be on 42 banner "
                                                    "coordinates!")
                parameters["ENTRY"] = (x, y)
            else:
                raise InvalidParameterError("ENTRY coordinates must be within"
                                            " the maze dimensions.")
        except ValueError:
            raise InvalidParameterError("ENTRY coordinates must be integers.")
    else:
        raise MissingParameterError("ENTRY parameter is missing.")

    if "EXIT" in parameters_keys:
        try:
            x, y = parameters["EXIT"].split(",")
        except ValueError:
            raise InvalidParameterError("EXIT have to have 2 parameters as "
                                        "x, y")
        try:
            x = int(x.strip())
            y = int(y.strip())
            if (0 <= x < parameters["WIDTH"]) and \
               (0 <= y < parameters["HEIGHT"]):
                if parameters["HEIGHT"] > 5 and parameters["WIDTH"] > 7:
                    if (x, y) in ft_banner:
                        raise InvalidParameterError("EXIT coordinates cannot"
                                                    " be on 42 banner "
                                                    "coordinates!")
                parameters["EXIT"] = (x, y)
            else:
                raise InvalidParameterError("EXIT coordinates must be within"
                                            " the maze dimensions.")
        except ValueError:
            raise InvalidParameterError("EXIT coordinates must be integers.")
    else:
        raise MissingParameterError("EXIT parameter is missing.")

    if "PERFECT" in parameters_keys:
        if parameters["PERFECT"].lower() == "true":
            parameters["PERFECT"] = True
        elif parameters["PERFECT"].lower() == "false":
            parameters["PERFECT"] = False
        else:
            raise InvalidParameterError("PERFECT must be 'True' or 'False'.")
    else:
        raise MissingParameterError("PERFECT parameter is missing.")

    if "OUTPUT_FILE" in parameters_keys:
        if parameters["OUTPUT_FILE"].endswith(".txt"):
            if len(parameters["OUTPUT_FILE"].split()) == 1:
                pass
            else:
                raise InvalidParameterError("OUTPUT_FILE name cannot "
                                            "include space.")
        else:
            raise InvalidParameterError("OUTPUT_FILE must end with .txt")
    else:
        raise MissingParameterError("OUTPUT_FILE parameter is missing.")

    if "SEED" in parameters_keys:
        try:
            parameters["SEED"] = int(parameters["SEED"])
        except ValueError:
            raise InvalidParameterError("SEED must be equal to just one "
                                        "integer.")

    (x1, y1) = parameters["ENTRY"]
    (x2, y2) = parameters["EXIT"]
    if x1 == x2 and y1 == y2:
        raise ValueError("ENTRY and EXIT cannot be at the same coordinates.")

    if parameters["HEIGHT"] < 6 or parameters["WIDTH"] < 8:
        print("Maze too small to implement 42 Banner!")

    return parameters
