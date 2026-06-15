import random
from .parser import MIN_HEIGHT, MIN_WIDTH
from collections import deque

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int,
                 entry: tuple[int, int], exit: tuple[int, int]) -> None:
        self._width: int = width
        self._height: int = height
        self._entry: tuple[int, int] = entry
        self._exit: tuple[int, int] = exit
        self._maze: list[list[int]] = []
        self._dmaze: list[list[str]] = []
        self._ft_banner_coordinates: set[tuple[int, int]] = set()
        self._visited_blocks: list[tuple[int, int]] = []
        self._backtracking: list[tuple[int, int]] = []
        self._blocks_coordinates: list[tuple[int, int]] = []
        self._chooser: random.Random = random.Random(seed)
        for y in range(height):
            row: list[int] = []
            for x in range(width):
                self._blocks_coordinates.append((x, y))
                row.append(15)
            self._maze.append(row)
        self.__display_maze()
        if len(self._ft_banner_coordinates) != 0:
            for i in self._ft_banner_coordinates:
                self._blocks_coordinates.remove(i)

    def __wall_breaker(self, x1: int, x2: int, y1: int, y2: int) -> None:
        if x1 == x2:
            if y1 < y2:
                self._maze[y1][x1] -= SOUTH
                self._maze[y2][x2] -= NORTH
            elif y1 > y2:
                self._maze[y1][x1] -= NORTH
                self._maze[y2][x2] -= SOUTH
        elif y1 == y2:
            if x1 < x2:
                self._maze[y1][x1] -= EAST
                self._maze[y2][x2] -= WEST
            elif x1 > x2:
                self._maze[y1][x1] -= WEST
                self._maze[y2][x2] -= EAST

    @property
    def maze(self) -> list[list[int]]:
        import copy
        return copy.deepcopy(self._maze)

    def __get_random(self, number: int) -> int:
        return self._chooser.choice(range(0, number))

    def __allowed_wall(self, x: int, y: int) -> list[int]:
        allowed_wall_list: list[int] = [NORTH, EAST, SOUTH, WEST]
        if x == 0:
            allowed_wall_list.remove(WEST)
        if x == self._width - 1:
            allowed_wall_list.remove(EAST)
        if y == 0:
            allowed_wall_list.remove(NORTH)
        if y == self._height - 1:
            allowed_wall_list.remove(SOUTH)
        if (x, y - 1) in self._ft_banner_coordinates:
            allowed_wall_list.remove(NORTH)
        if (x, y + 1) in self._ft_banner_coordinates:
            allowed_wall_list.remove(SOUTH)
        if (x - 1, y) in self._ft_banner_coordinates:
            allowed_wall_list.remove(WEST)
        if (x + 1, y) in self._ft_banner_coordinates:
            allowed_wall_list.remove(EAST)
        if (not (self._maze[y][x] & 1)) and (NORTH in allowed_wall_list):
            allowed_wall_list.remove(NORTH)
        if (not (self._maze[y][x] & 2)) and (EAST in allowed_wall_list):
            allowed_wall_list.remove(EAST)
        if (not (self._maze[y][x] & 4)) and (SOUTH in allowed_wall_list):
            allowed_wall_list.remove(SOUTH)
        if (not (self._maze[y][x] & 8)) and (WEST in allowed_wall_list):
            allowed_wall_list.remove(WEST)
        if ((x - 1, y) in self._visited_blocks) and \
           (WEST in allowed_wall_list):
            allowed_wall_list.remove(WEST)
        if ((x + 1, y) in self._visited_blocks) and \
           (EAST in allowed_wall_list):
            allowed_wall_list.remove(EAST)
        if ((x, y - 1) in self._visited_blocks) and \
           (NORTH in allowed_wall_list):
            allowed_wall_list.remove(NORTH)
        if ((x, y + 1) in self._visited_blocks) and \
           (SOUTH in allowed_wall_list):
            allowed_wall_list.remove(SOUTH)
        return allowed_wall_list

    def generate(self, perfect: bool = True) -> None:
        x: int = self.__get_random(self._width)
        y: int = self.__get_random(self._height)

        while (x, y) in self._ft_banner_coordinates:
            x = self.__get_random(self._width)
            y = self.__get_random(self._height)

        self._visited_blocks.append((x, y))
        self._backtracking.append((x, y))
        self._blocks_coordinates.remove((x, y))

        while len(self._blocks_coordinates) != 0:
            walls: list[int] = self.__allowed_wall(x, y)
            if len(walls) != 0:
                wall: int = self._chooser.choice(walls)
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
                if next_block in self._blocks_coordinates:
                    self._blocks_coordinates.remove(next_block)
                (x, y) = next_block
                if next_block not in self._visited_blocks:
                    self._visited_blocks.append(next_block)
                self._backtracking.append(next_block)
            else:
                if len(self._backtracking) > 0:
                    self._backtracking.pop()
                    if len(self._backtracking) > 0:
                        (x, y) = self._backtracking[-1]
        if not perfect and self._height > MIN_HEIGHT and \
           self._width > MIN_WIDTH:
            num_walls_to_break = int((self._width * self._height) * 0.1)
            if num_walls_to_break == 0 and self._width > MIN_WIDTH and \
               self._height > MIN_HEIGHT:
                num_walls_to_break = 1

            broken_count = 0
            attempts = 0
            while broken_count < num_walls_to_break and attempts < 1000:
                attempts += 1

                rx = self._chooser.randint(0, self._width - 1)
                ry = self._chooser.randint(0, self._height - 1)

                if (rx, ry) in self._ft_banner_coordinates:
                    continue
                direction = self._chooser.choice([NORTH, EAST, SOUTH, WEST])
                if direction == NORTH and ry > 0:
                    if (rx, ry - 1) not in self._ft_banner_coordinates:
                        if self._maze[ry][rx] & NORTH:
                            self.__wall_breaker(rx, rx, ry, ry - 1)
                            broken_count += 1

                elif direction == EAST and rx < self._width - 1:
                    if (rx + 1, ry) not in self._ft_banner_coordinates:
                        if self._maze[ry][rx] & EAST:
                            self.__wall_breaker(rx, rx + 1, ry, ry)
                            broken_count += 1

                elif direction == SOUTH and ry < self._height - 1:
                    if (rx, ry + 1) not in self._ft_banner_coordinates:
                        if self._maze[ry][rx] & SOUTH:
                            self.__wall_breaker(rx, rx, ry, ry + 1)
                            broken_count += 1

                elif direction == WEST and rx > 0:
                    if (rx - 1, ry) not in self._ft_banner_coordinates:
                        if self._maze[ry][rx] & WEST:
                            self.__wall_breaker(rx, rx - 1, ry, ry)
                            broken_count += 1

    def __banner(self) -> set[tuple[int, int]]:
        x: int = 0
        y: int = 0
        if self._width % 2 == 0:
            x = self._width // 2 - 1
        else:
            x = self._width // 2
        if self._height % 2 == 0:
            y = self._height // 2 - 1
        else:
            y = self._height // 2
        ft_banner: set[tuple[int, int]] = {
                                        (x - 1, y), (x - 2, y), (x - 3, y),
                                        (x - 3, y - 1), (x - 3, y - 2),
                                        (x - 1, y + 1), (x - 1, y + 2),
                                        (x + 1, y), (x + 2, y), (x + 3, y),
                                        (x + 3, y - 1), (x + 3, y - 2),
                                        (x + 2, y - 2), (x + 1, y - 2),
                                        (x + 1, y + 1), (x + 1, y + 2),
                                        (x + 2, y + 2), (x + 3, y + 2)}
        if len(self._ft_banner_coordinates) == 0:
            self._ft_banner_coordinates = ft_banner
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
        x: int = self._entry[0]
        y: int = self._entry[1]
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
        x: int = self._exit[0]
        y: int = self._exit[1]
        coordinate_1: tuple[int, int] = (3 * x + 1, 3 * y + 1)
        coordinate_2: tuple[int, int] = (3 * x + 1, 3 * y + 2)
        coordinate_3: tuple[int, int] = (3 * x + 2, 3 * y + 1)
        coordinate_4: tuple[int, int] = (3 * x + 2, 3 * y + 2)
        exit_points.add(coordinate_1)
        exit_points.add(coordinate_2)
        exit_points.add(coordinate_3)
        exit_points.add(coordinate_4)
        return exit_points

    def solve(self) -> tuple[list[tuple[int, int]], str]:
        start = self._entry
        end = self._exit

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
                return path_coords, path_str

            for direction_bit, dx, dy, direction_char in directions:

                if not (self._maze[cy][cx] & direction_bit):
                    nx, ny = cx + dx, cy + dy

                    if 0 <= nx < self._width and 0 <= ny < self._height:
                        if (nx, ny) not in visited:
                            if (nx, ny) in self._ft_banner_coordinates:
                                continue

                            visited.add((nx, ny))
                            queue.append((
                                          nx, ny, path_coords + [(nx, ny)],
                                          path_str + direction_char))
        return ([], "")

    def __display_maze(self, show_solution: bool = False,
                       solution_coords: list[tuple[int, int]] = []) -> None:
        MAX_Y = 3 * self._height + 1
        MAX_X = 3 * self._width + 1
        if (self._height >= 6 and self._width >= 8):
            ft_banner: set[tuple[int, int]] = self.__banner()
        entry_points: set[tuple[int, int]] = self.__entry_point()
        exit_points: set[tuple[int, int]] = self.__exit_point()

        solution_points = set()
        if show_solution and len(solution_coords):
            for (sx, sy) in solution_coords:
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
                      (self._height >= 6 and self._width >= 8) and
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
                    if self._maze[(y - 1) // 3][(x - 1) // 3] & EAST:
                        row.append("wall")
                    elif (((x - 1) // 3, (y - 1) // 3) in solution_coords and
                          ((x - 1) // 3 + 1, (y - 1) // 3) in solution_coords
                          and show_solution):
                        row.append("path")
                    else:
                        row.append("empty")
                elif y % 3 == 0 and x % 3 != 0:
                    if self._maze[(y - 1) // 3][(x - 1) // 3] & SOUTH:
                        row.append("wall")
                    elif (((x - 1) // 3, (y - 1) // 3) in solution_coords and
                          ((x - 1) // 3, (y - 1) // 3 + 1) in solution_coords
                          and show_solution):
                        row.append("path")
                    else:
                        row.append("empty")
                elif y % 3 == 0 and x % 3 == 0:
                    if (
                        self._maze[(y - 1) // 3][(x - 1) // 3] & SOUTH or
                        self._maze[(y - 1) // 3][((x - 1) // 3) + 1] & WEST or
                        self._maze[((y - 1) // 3) + 1][(x - 1) // 3] & EAST or
                        self._maze[((y - 1) // 3) + 1][((x - 1) // 3) + 1] & 1
                       ) == 0:
                        row.append("empty")
                    else:
                        row.append("wall")
            self._dmaze.append(row)

    def display(self, theme: dict[str, str],
                show_solution: bool = True) -> None:
        self._dmaze.clear()
        solution_coords, solution_path = self.solve()
        self.__display_maze(show_solution, solution_coords)
        MAX_Y = 3 * self._height + 1
        MAX_X = 3 * self._width + 1

        for y in range(MAX_Y):
            for x in range(MAX_X):
                cell = self._dmaze[y][x]
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
