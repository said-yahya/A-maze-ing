import random
NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8



class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int = None) -> None:
        self.width: int = width
        self.height: int = height
        self.chooser: random.Random = random.Random(seed)
        self.maze: list[list[int]] = []
        self.dmaze: list[list[str]] = []

        for i in range(height):
            row: list[int] = []
            for j in range(width):
                row.append(15)
            self.maze.append(row)


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
        else:
            raise ValueError("Something going wrong during wall breaking!")
        

    def generate(self) -> None:
        pass

    
    def banner(self) -> list[tuple[int]]:
        x: int = 0
        y: int = 0
        if self.width % 2 == 0:
            x = self.width / 2
        else:
            x = self.width // 2
        if self.height % 2 == 0:
            y = self.height / 2
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


    def display_maze(self) -> None:
        MAX_Y = 3 * self.height + 1
        MAX_X = 3 * self.width + 1
        if (self.height >= 7 and self.width >= 9):
            ft_banner: list[tuple[int]] = self.banner()
        for y in range(MAX_Y):
            row: list[str] = []
            for x in range(MAX_X):
                if (y == 0 or y == (MAX_Y - 1) or x == 0 or x == (MAX_X - 1)):
                    row.append("wall")
                elif (self.height >= 7 and self.width >= 9) and (x, y) in ft_banner:
                    row.append("banner")
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
        color = f"\x1b[{color}m"
        self.display_maze()
        MAX_Y = 3 * self.height + 1
        MAX_X = 3 * self.width + 1
        for y in range(MAX_Y):
            for x in range(MAX_X):
                if self.dmaze[y][x] == "wall":
                    print(f"{color} \x1b[0m", end="")
                elif self.dmaze[y][x] == "banner":
                    print(f"\x1b[41m \x1b[0m", end="")
                elif self.dmaze[y][x] == "empty":
                    print(f"\x1b[49m \x1b[0m", end="")
            print("")