*This project has been created as part of the 42 curriculum by ysaikhuj and vaktas.*

---

# Description
**A_MAZE_ING** is a command-line utility and an installable Python library designed to generate, solve, and visualize perfect or imperfect mazes. The unique challenge of this project is the integration of a hardcoded "42" structural banner inside the maze grid, acting as an unbreachable obstacle. 

The primary goal is to master strict Object-Oriented Programming (OOP) in Python, implement clean separation of concerns, enforce absolute static type safety (`mypy --strict`), and package the resulting code into a reusable distribution module compliance with modern Python packaging standards.

---

# Instructions

### Installation
To isolate dependencies and test package integrity from source, build and install the module within a virtual environment:
```bash
# 1. Setup and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install package build tools
pip install --upgrade pip build

# 3. Build the wheel distribution package
python3 -m build

# 4. Install the newly compiled package
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### Execution

You can easily automate the execution, style validation, and cleanup steps using the provided Makefile:

```bash
make
```
Validates style compliance (flake8), checks types (mypy), and executes the maze program.

```bash
make install
```
Install project dependencies using pip package manager.

```bash
make build
```
Compiles the core source codes into a standard distributable .whl package inside the dist/ folder, copies it directly to the root directory, and forces a clean re-installation of the library using pip install --force-reinstall.

```bash
make run
```
Instantly executes the program without triggering quality gate checks.

```bash
make debug
```
Launches the main script in interactive debug mode using Python's built-in debugger (pdb), allowing step-by-step code execution, variable inspections, and breakpoint tracing directly inside your terminal.

```bash
make lint
```
Runs static analysis checks like flake8 and mypy explicitly.

```bash
make clean
```
Removes python bytecode compilation files and temporary caches.

```bash
make fclean
```
Wipes all caches and deletes all generated outputs except your configuration files.

### Configuration File Structure & Format

The program strictly validates input configurations via a plain-text configuration file (config.txt). The format requires standard KEY = VALUE assignment rules, supports trailing and inline comments starting with #, and rejects duplicates or unknown parameters.

#### Example :

```bash
WIDTH = 20                 # Must be a single integer between 1 and 100
HEIGHT = 20                # Must be a single integer between 1 and 100
ENTRY = 0, 0               # Maze starting coordinate format: x, y
EXIT = 19, 19              # Maze exit coordinate format: x, y
PERFECT = True             # 'True' for single path, 'False' to break 10% of walls
OUTPUT_FILE = output.txt   # Target filename ending strictly with .txt
SEED = 42                  # Optional: Initializer integer for deterministic generation
```



### Algorithm & Choices

#### 1. Generation Algorithm: Randomized Depth-First Search (DFS)
We chose a **Randomized Depth-First Search (DFS)** algorithm driven by an explicit backtracking array stack (`_backtracking`) to carve out the corridors.

* **Why we chose it:** It naturally guarantees a "perfect maze" (a spanning tree over the grid graph), meaning there is exactly one unique path between any two points without any loops. Aesthetic-wise, DFS creates long, winding, and complex corridors with fewer short dead-ends compared to Prim's or Kruskal's algorithms, enhancing the maze experience. It also allowed easy structural control to avoid carving inside the restricted "42" banner coordinates.

#### 2. Solving Algorithm: Breadth-First Search (BFS)
Once the maze layout is fully generated, the shortest path from the defined `ENTRY` point to the `EXIT` point is discovered using a **Breadth-First Search (BFS)** algorithm backed by a fast `collections.deque` pipeline.

* **Why we chose it:**
  Unlike DFS, which can find any random valid path, BFS explores the maze level by level (layer by layer). This mathematically guarantees that the first time the `EXIT` coordinate is popped from the queue, the path discovered is **absolutely the shortest possible path** in terms of steps. Using a queue structure ensures highly efficient $O(V + E)$ linear time complexity, allowing even large grids to resolve paths instantly without lagging the generator.


### Code Reusability

The entire core generator engine is isolated inside layout under the namespace package mazegen.

* **What is reusable and how:**
The MazeGenerator class: It operates fully independently of the CLI controller. Anyone can import this package globally on their system post-installation and spin up customized mazes using raw Python types:

```Python
from mazegen import MazeGenerator

generator = MazeGenerator(width=20, height=20, seed=123, entry=(0,0), exit=(19,19))
generator.generate(perfect=True)
generator.solve()
generator.display()
generator.output_file("output_maze.txt")
```

### Team & Project Management

#### Roles of Each Team Member
**ysaikhuj:**
* MazeGenerator class
* methods like generate(), display(), __wall_breaker() and etc.
* Makefile
* Optimization

**vaktas:** 
* Parser
* Maze Solver Algorithm
* output_file() function
* Packaging
* Control program

# Resources

**Technical References**

* ANSI Terminal Coloring: Standard baseline layouts for terminal font layouts. 
Link: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
* ANSI Escape Code DocumentationPython Packaging Standards: Modern design parameters for .toml distributions.
Link: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/


**AI Assistant Usage Declaration**
AI was utilized as a supportive architectural peer during development for the following specific workflows:

* Refactoring Code: Assisting in shifting linear check algorithms into hash-backed sets (set()) to optimize grid scanning speeds from $O(N)$ to $O(1)$ inside complex conditional gates.
* Type Safety Troubleshooting: Diagnosing complex mypy edge cases regarding nested dictionaries containing mixed types, resolving them through clean typing.Any implementations.