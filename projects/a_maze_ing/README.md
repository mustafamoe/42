*This project has been created as part of the 42 curriculum by mal-hall, idamduo.*

# A-Maze-ing

## Description
A-Maze-ing is a highly efficient maze generator and solver built in Python. The goal of this project is to create a robust, modular, and reusable application capable of generating mathematically perfect (or imperfect) mazes, exporting them, and finding optimal solutions from entry to exit points. By relying on bitmask representations for cell walls, the program achieves high performance while keeping memory overhead low.

## Instructions

### Installation
We use `uv` for fast dependency management, and provide a `Makefile` for ease of use.
1. Make sure you have python >= 3.12 installed.
2. Install the necessary dependencies (optional, mostly for dev tools):
   ```bash
   make install
   ```

### Execution
You can run the main program using the Makefile, which defaults to reading from `config.txt`:
```bash
make run
```
Or you can run it directly:
```bash
python3 a_maze_ing.py config.txt
```


## Resources
* **Recursive Backtracking**: [Wikipedia - Maze generation algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker)
* **A* Pathfinding**: [Red Blob Games - Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
* **AI Usage**: Artificial Intelligence (Google Antigravity SDK) was used extensively in pair-programming to help refactor the codebase for modularity, debug bitmask logic, heavily optimize the A* and BFS solvers to reduce Python function-call overhead, and to generate the `pyproject.toml` packaging configuration for our standalone module.

## Config File Structure
The configuration file uses a simple `KEY=VALUE` format. Comments are prefixed with `#`.
* `WIDTH` / `HEIGHT`: Dimensions of the maze (integers).
* `ENTRY` / `EXIT`: Starting and ending coordinates formatted as `x,y`.
* `OUTPUT_FILE`: Path to export the textual representation of the maze.
* `PERFECT`: `True` for a maze with no loops (one unique path), `False` to allow loops.
* `SEED`: (Optional) Integer seed for reproducible random generation.
* `ALGORITHM`: Generation algorithm (e.g., `backtracking`).
* `DISPLAY`: Display mode (`terminal`).
* `ANIMATE_GENERATION`: `True` to watch the maze generate in real-time.
* `GENERATION_DELAY`: Float representing seconds to delay between animation frames.
* `ADD_42_PATTERN`: `True` to embed the '42' logo within the maze walls.
* `SOLVER`: Pathfinding algorithm. Accepts `astar`, `bfs`, or `compare` (which runs both and benchmarks them).

## Maze Generation Algorithm
We chose the **Recursive Backtracking** algorithm.
* **Why we chose it**: It is elegant, simple to implement using a stack, and generates mazes with long, winding corridors ("high river factor") which look visually appealing and are fun to solve. It also guarantees that every cell is visited and that a path exists between any two points. For imperfect mazes, we easily adapt it by subsequently knocking down additional random walls.

## Reusable Code (mazegen package)
The maze generation and solving logic is strictly decoupled from the CLI and UI, located in the `src/mazegen/` module. This module has been packaged into `mazegen-0.1.0-py3-none-any.whl` (found at the root of the repo) which can be installed in any future project.

### Testing Reusability (Proving it works!)
To evaluate and prove that the package is fully decoupled and reusable, you can install the built `.whl` file in an entirely separate project:

```bash
# 1. Leave the repository and create a new dummy project folder
cd /tmp
mkdir test_maze_project
cd test_maze_project

# 2. Create a fresh virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install the package we just built (replace path with your actual repo path)
pip install /path/to/A_maze_ing_The_Final/mazegen-0.1.0-py3-none-any.whl
# Or if using uv: uv pip install /path/to/A_maze_ing_The_Final/mazegen-0.1.0-py3-none-any.whl

# 4. Create a test script using the package
cat << 'EOF' > test.py
from mazegen import MazeGenerator
generator = MazeGenerator(width=5, height=5, perfect=True)
maze = generator.generate()
print(f"Success! Generated a {maze.width}x{maze.height} maze from an external project!")
EOF

# 5. Run it!
python3 test.py
```

**Usage Example:**
```python
from mazegen import MazeGenerator, BFSSolver, E

# 1. Instantiate the generator and generate a 10x10 perfect maze
generator = MazeGenerator(width=10, height=10, perfect=True, seed=42)
maze = generator.generate()

# 2. Access the generated structure (bitmask walls)
if maze.grid[0][0].walls & E:
    print("East wall is present at 0,0")

# 3. Access a solution
solver = BFSSolver()
path = solver.solve(maze, (0,0), (9,9))
```

## Team and Project Management
* **Roles**: 
  * *syedahamed / adkhan*: Co-developed the bitmask grid representations, TUI interface, solver algorithms, and project architecture.
* **Planning**: We anticipated starting with a simple 2D array representation but quickly shifted to bitmasks for efficiency. The architecture evolved from a single script to a modular `src/` layout to satisfy reusability requirements.
* **What worked well**: The bitwise operations made cell lookups extremely fast and lightweight.
* **What could be improved**: Early on, tight coupling between the generator and the renderer caused issues. Decoupling them into a proper MVC pattern improved the codebase significantly.
* **Tools used**: `uv` (package management), `ruff` and `flake8` (linting), `mypy` (static typing), and a standard `Makefile` for execution shortcuts.

## Advanced Features
* **Benchmarking (`SOLVER=compare`)**: Runs both A* and BFS simultaneously, measuring path length, nodes explored, and execution time in milliseconds to declare a winner.
* **Interactive Gameplay**: When the maze renders in the terminal, you can choose "Play Maze" to navigate the generated maze yourself using WASD or Arrow keys!
* **Color Schemes**: The terminal UI supports multiple themes including "Blood Red" and "Magenta" for the pathing display.
* **42 Logo Embedding**: A special feature (`ADD_42_PATTERN=True`) safely embeds the '42' logo within the generated maze walls without breaking the maze's solvability.
