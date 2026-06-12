import random
from collections import deque

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int,
                 entry: tuple, exit: tuple) -> None:
        self.width: int = width
        self.height: int = height
        self.entry: tuple[int] = entry
        self.exit: tuple[int] = exit
        self.maze: list[list[int]] = []
        self.dmaze: list[list[str]] = []
        self.ft_banner_coordinates: list[tuple[int]] = []
        self.visited_blocks: list[tuple[int]] = []
        self.backtracking: list[tuple[int]] = []
        self.blocks_coordinates: list[tuple[int]] = []
        self.chooser: random.Random = random.Random(seed)
        for y in range(height):
            row: list[int] = []
            for x in range(width):
                self.blocks_coordinates.append((x, y))
                row.append(15)
            self.maze.append(row)
        self.display_maze()
        if len(self.ft_banner_coordinates) != 0:
            for i in self.ft_banner_coordinates:
                self.blocks_coordinates.remove(i)

    def wall_breaker(self, x1: int, x2: int, y1: int, y2: int) -> None:
        if x1 == x2:
            if y1 < y2:
                self.maze[y1][x1] -= SOUTH
                self.maze[y2][x2] -= NORTH
            elif y1 > y2:
                self.maze[y1][x1] -= NORTH
                self.maze[y2][x2] -= SOUTH
        elif y1 == y2:
            if x1 < x2:
                self.maze[y1][x1] -= EAST
                self.maze[y2][x2] -= WEST
            elif x1 > x2:
                self.maze[y1][x1] -= WEST
                self.maze[y2][x2] -= EAST

    def get_random(self, number: int) -> int:
        return self.chooser.choice(range(0, number))

    def allowed_wall(self, x: int, y: int) -> list[int]:
        allowed_wall_list: list[int] = [NORTH, EAST, SOUTH, WEST]
        if x == 0:
            allowed_wall_list.remove(WEST)
        if x == self.width - 1:
            allowed_wall_list.remove(EAST)
        if y == 0:
            allowed_wall_list.remove(NORTH)
        if y == self.height - 1:
            allowed_wall_list.remove(SOUTH)
        if (x, y - 1) in self.ft_banner_coordinates:
            allowed_wall_list.remove(NORTH)
        if (x, y + 1) in self.ft_banner_coordinates:
            allowed_wall_list.remove(SOUTH)
        if (x - 1, y) in self.ft_banner_coordinates:
            allowed_wall_list.remove(WEST)
        if (x + 1, y) in self.ft_banner_coordinates:
            allowed_wall_list.remove(EAST)
        if (not (self.maze[y][x] & 1)) and (NORTH in allowed_wall_list):
            allowed_wall_list.remove(NORTH)
        if (not (self.maze[y][x] & 2)) and (EAST in allowed_wall_list):
            allowed_wall_list.remove(EAST)
        if (not (self.maze[y][x] & 4)) and (SOUTH in allowed_wall_list):
            allowed_wall_list.remove(SOUTH)
        if (not (self.maze[y][x] & 8)) and (WEST in allowed_wall_list):
            allowed_wall_list.remove(WEST)
        if ((x - 1, y) in self.visited_blocks) and (WEST in allowed_wall_list):
            allowed_wall_list.remove(WEST)
        if ((x + 1, y) in self.visited_blocks) and (EAST in allowed_wall_list):
            allowed_wall_list.remove(EAST)
        if ((x, y - 1) in self.visited_blocks) and \
                (NORTH in allowed_wall_list):
            allowed_wall_list.remove(NORTH)
        if ((x, y + 1) in self.visited_blocks) and \
                (SOUTH in allowed_wall_list):
            allowed_wall_list.remove(SOUTH)
        return allowed_wall_list

    def generate(self, perfect: bool = True) -> None:
        x: int = self.get_random(self.width)
        y: int = self.get_random(self.height)

        while (x, y) in self.ft_banner_coordinates:
            x = self.get_random(self.width)
            y = self.get_random(self.height)

        self.visited_blocks.append((x, y))
        self.backtracking.append((x, y))
        if (x, y) in self.blocks_coordinates:
            self.blocks_coordinates.remove((x, y))

        while len(self.blocks_coordinates) != 0:
            walls: list[int] = self.allowed_wall(x, y)
            if len(walls) != 0:
                wall: int = self.chooser.choice(walls)
                if wall == NORTH:
                    self.wall_breaker(x, x, y, y - 1)
                    next_block = (x, y - 1)
                elif wall == EAST:
                    self.wall_breaker(x, x + 1, y, y)
                    next_block = (x + 1, y)
                elif wall == SOUTH:
                    self.wall_breaker(x, x, y, y + 1)
                    next_block = (x, y + 1)
                elif wall == WEST:
                    self.wall_breaker(x, x - 1, y, y)
                    next_block = (x - 1, y)
                if next_block in self.blocks_coordinates:
                    self.blocks_coordinates.remove(next_block)
                (x, y) = next_block
                if next_block not in self.visited_blocks:
                    self.visited_blocks.append(next_block)
                self.backtracking.append(next_block)
            else:
                if len(self.backtracking) > 0:
                    self.backtracking.pop()
                    if len(self.backtracking) > 0:
                        (x, y) = self.backtracking[-1]
        if not perfect:
            num_walls_to_break = int((self.width * self.height) * 0.1)
            if num_walls_to_break == 0 and self.width > 1 and self.height > 1:
                num_walls_to_break = 1

            broken_count = 0
            attempts = 0
            while broken_count < num_walls_to_break and attempts < 1000:
                attempts += 1

                rx = self.chooser.randint(0, self.width - 1)
                ry = self.chooser.randint(0, self.height - 1)

                if (rx, ry) in self.ft_banner_coordinates:
                    continue
                direction = self.chooser.choice([NORTH, EAST, SOUTH, WEST])
                if direction == NORTH and ry > 0:
                    if (rx, ry - 1) not in self.ft_banner_coordinates:
                        if self.maze[ry][rx] & NORTH:
                            self.wall_breaker(rx, rx, ry, ry - 1)
                            broken_count += 1

                elif direction == EAST and rx < self.width - 1:
                    if (rx + 1, ry) not in self.ft_banner_coordinates:
                        if self.maze[ry][rx] & EAST:
                            self.wall_breaker(rx, rx + 1, ry, ry)
                            broken_count += 1

                elif direction == SOUTH and ry < self.height - 1:
                    if (rx, ry + 1) not in self.ft_banner_coordinates:
                        if self.maze[ry][rx] & SOUTH:
                            self.wall_breaker(rx, rx, ry, ry + 1)
                            broken_count += 1

                elif direction == WEST and rx > 0:
                    if (rx - 1, ry) not in self.ft_banner_coordinates:
                        if self.maze[ry][rx] & WEST:
                            self.wall_breaker(rx, rx - 1, ry, ry)
                            broken_count += 1

    def banner(self) -> list[tuple[int]]:
        x: int = 0
        y: int = 0
        if self.width % 2 == 0:
            x = self.width / 2 - 1
        else:
            x = self.width // 2
        if self.height % 2 == 0:
            y = self.height / 2 - 1
        else:
            y = self.height // 2
        ft_banner: list[tuple[int]] = [
                                        (x - 1, y), (x - 2, y), (x - 3, y),
                                        (x - 3, y - 1), (x - 3, y - 2),
                                        (x - 1, y + 1), (x - 1, y + 2),
                                        (x + 1, y), (x + 2, y), (x + 3, y),
                                        (x + 3, y - 1), (x + 3, y - 2),
                                        (x + 2, y - 2), (x + 1, y - 2),
                                        (x + 1, y + 1), (x + 1, y + 2),
                                        (x + 2, y + 2), (x + 3, y + 2)
                                       ]
        self.ft_banner_coordinates.extend(ft_banner)
        ft_big_banner: list[tuple[int]] = []
        for i in ft_banner:
            coordinate_1: tuple[int] = (3 * i[0] + 1, 3 * i[1] + 1)
            coordinate_2: tuple[int] = (3 * i[0] + 1, 3 * i[1] + 2)
            coordinate_3: tuple[int] = (3 * i[0] + 2, 3 * i[1] + 1)
            coordinate_4: tuple[int] = (3 * i[0] + 2, 3 * i[1] + 2)
            ft_big_banner.append(coordinate_1)
            ft_big_banner.append(coordinate_2)
            ft_big_banner.append(coordinate_3)
            ft_big_banner.append(coordinate_4)

        return ft_big_banner

    def entry_point(self) -> list[tuple[int]]:
        entry_points: list[tuple[int]] = []
        x: int = self.entry[0]
        y: int = self.entry[1]
        coordinate_1: tuple[int] = (3 * x + 1, 3 * y + 1)
        coordinate_2: tuple[int] = (3 * x + 1, 3 * y + 2)
        coordinate_3: tuple[int] = (3 * x + 2, 3 * y + 1)
        coordinate_4: tuple[int] = (3 * x + 2, 3 * y + 2)
        entry_points.append(coordinate_1)
        entry_points.append(coordinate_2)
        entry_points.append(coordinate_3)
        entry_points.append(coordinate_4)
        return entry_points

    def exit_point(self) -> list[tuple[int]]:
        exit_points: list[tuple[int]] = []
        x: int = self.exit[0]
        y: int = self.exit[1]
        coordinate_1: tuple[int] = (3 * x + 1, 3 * y + 1)
        coordinate_2: tuple[int] = (3 * x + 1, 3 * y + 2)
        coordinate_3: tuple[int] = (3 * x + 2, 3 * y + 1)
        coordinate_4: tuple[int] = (3 * x + 2, 3 * y + 2)
        exit_points.append(coordinate_1)
        exit_points.append(coordinate_2)
        exit_points.append(coordinate_3)
        exit_points.append(coordinate_4)
        return exit_points

    def solve(self) -> tuple[list[tuple[int, int]], str]:

        start = self.entry
        end = self.exit

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

                if not (self.maze[cy][cx] & direction_bit):
                    nx, ny = cx + dx, cy + dy

                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if (nx, ny) not in visited:

                            if (nx, ny) in self.ft_banner_coordinates:
                                continue

                            visited.add((nx, ny))
                            queue.append((
                                            nx, ny, path_coords + [(nx, ny)],
                                            path_str + direction_char))

        return [], ""

    def display_maze(self, show_solution: bool = False,
                     solution_coords: list = None) -> None:
        MAX_Y = 3 * self.height + 1
        MAX_X = 3 * self.width + 1
        if (self.height >= 6 and self.width >= 8):
            ft_banner: list[tuple[int]] = self.banner()
        entry_points: list[tuple[int]] = self.entry_point()
        exit_points: list[tuple[int]] = self.exit_point()

        solution_points = set()
        if show_solution and solution_coords:
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
                      (self.height >= 6 and self.width >= 8) and
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
                    if self.maze[(y - 1) // 3][(x - 1) // 3] & EAST:
                        row.append("wall")
                    else:
                        row.append("empty")
                elif y % 3 == 0 and x % 3 != 0:
                    if self.maze[(y - 1) // 3][(x - 1) // 3] & SOUTH:
                        row.append("wall")
                    else:
                        row.append("empty")
                elif y % 3 == 0 and x % 3 == 0:
                    if (
                        (self.maze[(y - 1) // 3][(x - 1) // 3] & SOUTH) or
                        (self.maze[(y - 1) // 3][((x - 1) // 3) + 1] & WEST) or
                        (self.maze[((y - 1) // 3) + 1][(x - 1) // 3] & EAST) or
                        (self.maze[((y - 1) // 3) + 1][((x - 1) // 3) + 1] & 1)
                       ) == 0:
                        row.append("empty")
                    else:
                        row.append("wall")
            self.dmaze.append(row)

    def display(self, theme: dict, show_solution: bool = True) -> None:
        self.dmaze.clear()
        solution_coords, solution_path = self.solve()
        self.display_maze(show_solution, solution_coords)
        MAX_Y = 3 * self.height + 1
        MAX_X = 3 * self.width + 1

        for y in range(MAX_Y):
            for x in range(MAX_X):
                cell = self.dmaze[y][x]
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
