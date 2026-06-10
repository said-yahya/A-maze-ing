import random
NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int,
                 entry: tuple = (1, 0), exit: tuple = (13, 10)) -> None:
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

    def generate(self) -> None:
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
                    (x, y) = self.backtracking[-1]

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

    def solve(self) -> list[tuple[int, int]]:

        start = self.entry
        end = self.exit
        stack = [start]
        visited = set([start])
        parent = {}

        while stack:
            current = stack.pop()

            if current == end:
                break

            x, y = current
            cell_walls = self.maze[y][x]

            neighbors = []
            if not (cell_walls & NORTH) and y > 0: neighbors.append((x, y - 1))
            if not (cell_walls & EAST) and x < self.width - 1: neighbors.append((x + 1, y))
            if not (cell_walls & SOUTH) and y < self.height - 1: neighbors.append((x, y + 1))
            if not (cell_walls & WEST) and x > 0: neighbors.append((x - 1, y))

            for nxt in neighbors:
                if nxt not in visited and nxt not in self.ft_banner_coordinates:
                    visited.add(nxt)
                    parent[nxt] = curr
                    stack.append(nxt)
            
            path = []
        curr = end
        while curr != start:
            if curr not in parent:
                return []
            path.append(curr)
            curr = parent[curr]
        path.append(start)
        return path[::-1]

    def display_maze(self) -> None:
        MAX_Y = 3 * self.height + 1
        MAX_X = 3 * self.width + 1
        if (self.height >= 6 and self.width >= 8):
            ft_banner: list[tuple[int]] = self.banner()
        entry_points: list[tuple[int]] = self.entry_point()
        exit_points: list[tuple[int]] = self.exit_point()
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

    def display(self, color: str = "47") -> None:
        self.dmaze.clear()
        self.display_maze()
        color = f"\x1b[{color}m"
        MAX_Y = 3 * self.height + 1
        MAX_X = 3 * self.width + 1
        for y in range(MAX_Y):
            for x in range(MAX_X):
                if self.dmaze[y][x] == "wall":
                    print(f"{color}  \x1b[0m", end="")
                elif self.dmaze[y][x] == "banner":
                    print("\x1b[41m  \x1b[0m", end="")
                elif self.dmaze[y][x] == "entry":
                    print("\x1b[42m  \x1b[0m", end="")
                elif self.dmaze[y][x] == "exit":
                    print("\x1b[43m  \x1b[0m", end="")
                elif self.dmaze[y][x] == "empty":
                    print("\x1b[49m  \x1b[0m", end="")
            print("")
