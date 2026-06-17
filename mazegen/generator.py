import random
from mazegen import MIN_HEIGHT, MIN_WIDTH
from collections import deque

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int,
                 entry: tuple[int, int], exit: tuple[int, int]) -> None:
        self.__width: int = width
        self.__height: int = height
        self.__entry: tuple[int, int] = entry
        self.__exit: tuple[int, int] = exit
        self.__maze: list[list[int]] = []
        self.__dmaze: list[list[str]] = []
        self.__ft_banner_coordinates: set[tuple[int, int]] = set()
        self.__visited_blocks: list[tuple[int, int]] = []
        self.__backtracking: list[tuple[int, int]] = []
        self.__blocks_coordinates: list[tuple[int, int]] = []
        self.__solution_coordinates: list[tuple[int, int]] = []
        self.__path_str: str = ""
        self.__chooser: random.Random = random.Random(seed)
        self.__create_maze_instance()

    def __create_maze_instance(self) -> None:
        for y in range(self.__height):
            row: list[int] = []
            for x in range(self.__width):
                self.__blocks_coordinates.append((x, y))
                row.append(15)
            self.__maze.append(row)
        self.__display_maze()
        if len(self.__ft_banner_coordinates) != 0:
            for i in self.__ft_banner_coordinates:
                self.__blocks_coordinates.remove(i)

    def __clear_maze(self) -> None:
        self.__maze.clear()
        self.__dmaze.clear()
        self.__blocks_coordinates.clear()
        self.__visited_blocks.clear()
        self.__backtracking.clear()
        self.__solution_coordinates.clear()
        self.__path_str = ""

    def __wall_breaker(self, x1: int, x2: int, y1: int, y2: int) -> None:
        if x1 == x2:
            if y1 < y2:
                self.__maze[y1][x1] -= SOUTH
                self.__maze[y2][x2] -= NORTH
            elif y1 > y2:
                self.__maze[y1][x1] -= NORTH
                self.__maze[y2][x2] -= SOUTH
        elif y1 == y2:
            if x1 < x2:
                self.__maze[y1][x1] -= EAST
                self.__maze[y2][x2] -= WEST
            elif x1 > x2:
                self.__maze[y1][x1] -= WEST
                self.__maze[y2][x2] -= EAST

    @property
    def maze(self) -> list[list[int]]:
        import copy
        return copy.deepcopy(self.__maze)

    def __get_random(self, number: int) -> int:
        return self.__chooser.choice(range(0, number))

    def __allowed_wall(self, x: int, y: int) -> list[int]:
        allowed_wall_list: list[int] = [NORTH, EAST, SOUTH, WEST]
        if x == 0:
            allowed_wall_list.remove(WEST)
        if x == self.__width - 1:
            allowed_wall_list.remove(EAST)
        if y == 0:
            allowed_wall_list.remove(NORTH)
        if y == self.__height - 1:
            allowed_wall_list.remove(SOUTH)
        if (x, y - 1) in self.__ft_banner_coordinates:
            allowed_wall_list.remove(NORTH)
        if (x, y + 1) in self.__ft_banner_coordinates:
            allowed_wall_list.remove(SOUTH)
        if (x - 1, y) in self.__ft_banner_coordinates:
            allowed_wall_list.remove(WEST)
        if (x + 1, y) in self.__ft_banner_coordinates:
            allowed_wall_list.remove(EAST)
        if (not (self.__maze[y][x] & 1)) and (NORTH in allowed_wall_list):
            allowed_wall_list.remove(NORTH)
        if (not (self.__maze[y][x] & 2)) and (EAST in allowed_wall_list):
            allowed_wall_list.remove(EAST)
        if (not (self.__maze[y][x] & 4)) and (SOUTH in allowed_wall_list):
            allowed_wall_list.remove(SOUTH)
        if (not (self.__maze[y][x] & 8)) and (WEST in allowed_wall_list):
            allowed_wall_list.remove(WEST)
        if ((x - 1, y) in self.__visited_blocks) and \
           (WEST in allowed_wall_list):
            allowed_wall_list.remove(WEST)
        if ((x + 1, y) in self.__visited_blocks) and \
           (EAST in allowed_wall_list):
            allowed_wall_list.remove(EAST)
        if ((x, y - 1) in self.__visited_blocks) and \
           (NORTH in allowed_wall_list):
            allowed_wall_list.remove(NORTH)
        if ((x, y + 1) in self.__visited_blocks) and \
           (SOUTH in allowed_wall_list):
            allowed_wall_list.remove(SOUTH)
        return allowed_wall_list

    def generate(self, perfect: bool = True) -> None:
        self.__clear_maze()
        self.__create_maze_instance()

        x: int = self.__get_random(self.__width)
        y: int = self.__get_random(self.__height)

        while (x, y) in self.__ft_banner_coordinates:
            x = self.__get_random(self.__width)
            y = self.__get_random(self.__height)

        self.__visited_blocks.append((x, y))
        self.__backtracking.append((x, y))
        self.__blocks_coordinates.remove((x, y))

        while len(self.__blocks_coordinates) != 0:
            walls: list[int] = self.__allowed_wall(x, y)
            if len(walls) != 0:
                wall: int = self.__chooser.choice(walls)
                if wall == NORTH:
                    self.__wall_breaker(x, x, y, y - 1)
                    next_block = (x, y - 1)
                elif wall == EAST:
                    self.__wall_breaker(x, x + 1, y, y)
                    next_block = (x + 1, y)
                elif wall == SOUTH:
                    self.__wall_breaker(x, x, y, y + 1)
                    next_block = (x, y + 1)
                elif wall == WEST:
                    self.__wall_breaker(x, x - 1, y, y)
                    next_block = (x - 1, y)
                if next_block in self.__blocks_coordinates:
                    self.__blocks_coordinates.remove(next_block)
                (x, y) = next_block
                if next_block not in self.__visited_blocks:
                    self.__visited_blocks.append(next_block)
                self.__backtracking.append(next_block)
            else:
                if len(self.__backtracking) > 0:
                    self.__backtracking.pop()
                    if len(self.__backtracking) > 0:
                        (x, y) = self.__backtracking[-1]
        if not perfect and self.__height > MIN_HEIGHT and \
           self.__width > MIN_WIDTH:
            num_walls_to_break = int((self.__width * self.__height) * 0.1)
            if num_walls_to_break == 0 and self.__width > MIN_WIDTH and \
               self.__height > MIN_HEIGHT:
                num_walls_to_break = 1

            broken_count = 0
            attempts = 0
            while broken_count < num_walls_to_break and attempts < 1000:
                attempts += 1

                rx = self.__chooser.randint(0, self.__width - 1)
                ry = self.__chooser.randint(0, self.__height - 1)

                if (rx, ry) in self.__ft_banner_coordinates:
                    continue
                direction = self.__chooser.choice([NORTH, EAST, SOUTH, WEST])
                if direction == NORTH and ry > 0:
                    if (rx, ry - 1) not in self.__ft_banner_coordinates:
                        if self.__maze[ry][rx] & NORTH:
                            self.__wall_breaker(rx, rx, ry, ry - 1)
                            broken_count += 1

                elif direction == EAST and rx < self.__width - 1:
                    if (rx + 1, ry) not in self.__ft_banner_coordinates:
                        if self.__maze[ry][rx] & EAST:
                            self.__wall_breaker(rx, rx + 1, ry, ry)
                            broken_count += 1

                elif direction == SOUTH and ry < self.__height - 1:
                    if (rx, ry + 1) not in self.__ft_banner_coordinates:
                        if self.__maze[ry][rx] & SOUTH:
                            self.__wall_breaker(rx, rx, ry, ry + 1)
                            broken_count += 1

                elif direction == WEST and rx > 0:
                    if (rx - 1, ry) not in self.__ft_banner_coordinates:
                        if self.__maze[ry][rx] & WEST:
                            self.__wall_breaker(rx, rx - 1, ry, ry)
                            broken_count += 1

    def __banner(self) -> set[tuple[int, int]]:
        x: int = 0
        y: int = 0
        if self.__width % 2 == 0:
            x = self.__width // 2 - 1
        else:
            x = self.__width // 2
        if self.__height % 2 == 0:
            y = self.__height // 2 - 1
        else:
            y = self.__height // 2
        ft_banner: set[tuple[int, int]] = {
                                        (x - 1, y), (x - 2, y), (x - 3, y),
                                        (x - 3, y - 1), (x - 3, y - 2),
                                        (x - 1, y + 1), (x - 1, y + 2),
                                        (x + 1, y), (x + 2, y), (x + 3, y),
                                        (x + 3, y - 1), (x + 3, y - 2),
                                        (x + 2, y - 2), (x + 1, y - 2),
                                        (x + 1, y + 1), (x + 1, y + 2),
                                        (x + 2, y + 2), (x + 3, y + 2)}
        if len(self.__ft_banner_coordinates) == 0:
            self.__ft_banner_coordinates = ft_banner
        ft_big_banner: set[tuple[int, int]] = set()
        for i in ft_banner:
            coordinate_1: tuple[int, int] = (3 * i[0] + 1, 3 * i[1] + 1)
            coordinate_2: tuple[int, int] = (3 * i[0] + 1, 3 * i[1] + 2)
            coordinate_3: tuple[int, int] = (3 * i[0] + 2, 3 * i[1] + 1)
            coordinate_4: tuple[int, int] = (3 * i[0] + 2, 3 * i[1] + 2)
            ft_big_banner.add(coordinate_1)
            ft_big_banner.add(coordinate_2)
            ft_big_banner.add(coordinate_3)
            ft_big_banner.add(coordinate_4)

        return ft_big_banner

    def __entry_point(self) -> set[tuple[int, int]]:
        entry_points: set[tuple[int, int]] = set()
        x: int = self.__entry[0]
        y: int = self.__entry[1]
        coordinate_1: tuple[int, int] = (3 * x + 1, 3 * y + 1)
        coordinate_2: tuple[int, int] = (3 * x + 1, 3 * y + 2)
        coordinate_3: tuple[int, int] = (3 * x + 2, 3 * y + 1)
        coordinate_4: tuple[int, int] = (3 * x + 2, 3 * y + 2)
        entry_points.add(coordinate_1)
        entry_points.add(coordinate_2)
        entry_points.add(coordinate_3)
        entry_points.add(coordinate_4)
        return entry_points

    def __exit_point(self) -> set[tuple[int, int]]:
        exit_points: set[tuple[int, int]] = set()
        x: int = self.__exit[0]
        y: int = self.__exit[1]
        coordinate_1: tuple[int, int] = (3 * x + 1, 3 * y + 1)
        coordinate_2: tuple[int, int] = (3 * x + 1, 3 * y + 2)
        coordinate_3: tuple[int, int] = (3 * x + 2, 3 * y + 1)
        coordinate_4: tuple[int, int] = (3 * x + 2, 3 * y + 2)
        exit_points.add(coordinate_1)
        exit_points.add(coordinate_2)
        exit_points.add(coordinate_3)
        exit_points.add(coordinate_4)
        return exit_points

    def solve(self) -> None:
        start = self.__entry
        end = self.__exit

        queue = deque([(start[0], start[1], [start], "")])

        visited = set()
        visited.add(start)

        directions = [
            (NORTH, 0, -1, 'N'),
            (EAST,  1,  0, 'E'),
            (SOUTH, 0,  1, 'S'),
            (WEST, -1,  0, 'W')
        ]

        while queue:
            cx, cy, path_coords, path_str = queue.popleft()

            if (cx, cy) == end:
                self.__solution_coordinates = path_coords
                self.__path_str = path_str
                break

            for direction_bit, dx, dy, direction_char in directions:

                if not (self.__maze[cy][cx] & direction_bit):
                    nx, ny = cx + dx, cy + dy

                    if 0 <= nx < self.__width and 0 <= ny < self.__height:
                        if (nx, ny) not in visited:
                            if (nx, ny) in self.__ft_banner_coordinates:
                                continue

                            visited.add((nx, ny))
                            queue.append((
                                          nx, ny, path_coords + [(nx, ny)],
                                          path_str + direction_char))

    def __display_maze(self, show_solution: bool = False) -> None:
        MAX_Y = 3 * self.__height + 1
        MAX_X = 3 * self.__width + 1
        if (self.__height >= 6 and self.__width >= 8):
            ft_banner: set[tuple[int, int]] = self.__banner()
        entry_points: set[tuple[int, int]] = self.__entry_point()
        exit_points: set[tuple[int, int]] = self.__exit_point()

        solution_points = set()
        if show_solution and len(self.__solution_coordinates):
            for (sx, sy) in self.__solution_coordinates:
                solution_points.add((3 * sx + 1, 3 * sy + 1))
                solution_points.add((3 * sx + 1, 3 * sy + 2))
                solution_points.add((3 * sx + 2, 3 * sy + 1))
                solution_points.add((3 * sx + 2, 3 * sy + 2))

        for y in range(MAX_Y):
            row: list[str] = []
            for x in range(MAX_X):
                if (y == 0 or y == (MAX_Y - 1) or x == 0 or x == (MAX_X - 1)):
                    row.append("wall")
                elif (
                      (self.__height >= 6 and self.__width >= 8) and
                      (x, y) in ft_banner
                      ):
                    row.append("banner")
                elif (x, y) in entry_points:
                    row.append("entry")
                elif (x, y) in exit_points:
                    row.append("exit")
                elif show_solution and (x, y) in solution_points:
                    row.append("path")
                elif x % 3 != 0 and y % 3 != 0:
                    row.append("empty")
                elif x % 3 == 0 and y % 3 != 0:
                    if self.__maze[(y - 1) // 3][(x - 1) // 3] & EAST:
                        row.append("wall")
                    elif (((x - 1) // 3, (y - 1) // 3)
                          in self.__solution_coordinates and
                          ((x - 1) // 3 + 1, (y - 1) // 3) in
                          self.__solution_coordinates and show_solution):
                        row.append("path")
                    else:
                        row.append("empty")
                elif y % 3 == 0 and x % 3 != 0:
                    if self.__maze[(y - 1) // 3][(x - 1) // 3] & SOUTH:
                        row.append("wall")
                    elif (((x - 1) // 3, (y - 1) // 3)
                          in self.__solution_coordinates and
                          ((x - 1) // 3, (y - 1) // 3 + 1)
                          in self.__solution_coordinates
                          and show_solution):
                        row.append("path")
                    else:
                        row.append("empty")
                elif y % 3 == 0 and x % 3 == 0:
                    if (
                        self.__maze[(y - 1) // 3][(x - 1) // 3] & SOUTH or
                        self.__maze[(y - 1) // 3][((x - 1) // 3) + 1] & WEST or
                        self.__maze[((y - 1) // 3) + 1][(x - 1) // 3] & EAST or
                        self.__maze[((y - 1) // 3) + 1][((x - 1) // 3) + 1] & 1
                       ) == 0:
                        row.append("empty")
                    else:
                        row.append("wall")
            self.__dmaze.append(row)

    def display(self, show_solution: bool = True,
                theme: dict[str, str] = {"wall": "47", "banner": "41",
                                         "entry": "42", "exit": "43",
                                         "path": "46"}) -> None:
        self.__dmaze.clear()
        if len(self.__path_str) == 0:
            show_solution = False
        self.__display_maze(show_solution)
        MAX_Y = 3 * self.__height + 1
        MAX_X = 3 * self.__width + 1

        for y in range(MAX_Y):
            for x in range(MAX_X):
                cell = self.__dmaze[y][x]
                if cell == "wall":
                    print(f"\x1b[{theme['wall']}m  \x1b[0m", end="")
                elif cell == "banner":
                    print(f"\x1b[{theme['banner']}m  \x1b[0m", end="")
                elif cell == "entry":
                    print(f"\x1b[{theme['entry']}m  \x1b[0m", end="")
                elif cell == "exit":
                    print(f"\x1b[{theme['exit']}m  \x1b[0m", end="")
                elif cell == "path":
                    print(f"\x1b[{theme['path']}m  \x1b[0m", end="")
                elif cell == "empty":
                    print("\x1b[49m  \x1b[0m", end="")
            print("")

    def output_file(self, filename: str) -> None:
        output_name = filename
        entry_name: str = f"{self.__entry[0]},{self.__entry[1]}"
        exit_name: str = f"{self.__exit[0]},{self.__exit[1]}"

        with open(output_name, "w") as file:
            for row in self.__maze:
                hex_row = "".join(f"{cell:X}" for cell in row)
                file.write(hex_row + "\n")
            file.write("\n")
            file.write(entry_name + "\n")
            file.write(exit_name + "\n")
            file.write(self.__path_str + "\n")
