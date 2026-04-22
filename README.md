_This project has been created as part of the 42 curriculum by finorak, trakotos, finorako._

# A-Maze-ing

## Description

**A-Maze-ing** is a maze generator and solver written in Python with a graphical interface based on MLX.

The project can:

- generate a maze from a configuration file,
- display the generation process step by step,
- solve the maze with two different strategies,
- let the user move inside the maze after generation,
- export the maze to a text file,
- optionally display a 42-shaped block in the middle of the maze.

The project is split into reusable modules: maze data structures, generation logic, solving logic, configuration parsing, rendering, and player navigation.

## Instructions

### Requirements

- Python 3
- the local `mlx` wheel provided in the repository
- `flake8` and `mypy` if you want to run the quality checks through the Makefile

### Installation

```bash
make install
```

This creates the virtual environment and installs the dependencies listed in `requirements.txt`.

### Run

```bash
make run
```

This starts the application with `config.txt`.

You can also run it manually:

```bash
python3 a_maze_ing.py config.txt
```

### Optional checks

```bash
make flake
make lint
```

### Output validation

After exporting a maze to a text file, you can validate the encoding with:

```bash
python3 output_validator.py maze.txt
```

## Usage

### Keyboard controls

#### Main screen

- `Space`: open the maze view
- `h`: open the help window
- `q` or `Esc`: quit

#### Maze view

- `g`: generate the maze
- `s`: solve with the first solver strategy
- `d`: solve with DFS
- `w`: write the maze to the output file
- `c`: change the wall color palette
- `p`: toggle perfect / imperfect maze
- `f`: show or hide the 42 logo block
- `r`: reset and reinitialize the maze
- `h`: open the help window
- `q` or `Esc`: quit

#### Player mode

- `j`: enable player movement
- arrow keys: move through the maze
- left click: move the entry point after generation
- right click: move the exit point after generation

## Configuration file

The configuration file is a plain text file made of `KEY=VALUE` pairs.

### Format rules

- one setting per line
- comments begin with `#`
- empty lines are ignored
- spaces around keys, values, and `=` are accepted
- coordinates must be written as `x,y`
- boolean values accept `True` / `False` or `true` / `false`

### Supported keys

| Key           | Type        | Description                                             |
| ------------- | ----------- | ------------------------------------------------------- |
| `WIDTH`       | integer     | Maze width in cells                                     |
| `HEIGHT`      | integer     | Maze height in cells                                    |
| `ENTRY`       | tuple `x,y` | Starting cell                                           |
| `EXIT`        | tuple `x,y` | Ending cell                                             |
| `OUTPUT_FILE` | string      | File used when exporting the maze                       |
| `PERFECT`     | boolean     | `True` for a perfect maze, `False` to break extra walls |

### Example

```txt
WIDTH=21
HEIGHT=15
ENTRY=4,5
EXIT=5,5
OUTPUT_FILE=maze.txt
PERFECT=True
```

If the configuration is invalid, the application falls back to its internal base configuration.

## Maze generation algorithm

The maze is generated with a randomized depth-first search, also known as recursive backtracking.

### How it works

1. Start from a cell.
2. Mark it as open.
3. Pick a random closed neighbor.
4. Remove the wall between the current cell and the chosen neighbor.
5. Recurse on the neighbor.
6. Continue until every reachable cell has been visited.

When `PERFECT=False`, the generator also breaks a small number of additional walls to create loops and make the maze less strict.

### Why this algorithm was chosen

- it is simple to implement and easy to debug,
- it guarantees a fully connected maze when perfect mode is enabled,
- it produces natural-looking mazes,
- it fits well with the animated step-by-step display used by the project,
- it leaves room for an imperfect mode by adding extra wall breaks.

## Reusable parts of the code

Several parts of the project are reusable outside the graphical application:

- `src/maze/cell.py`: a standalone cell model with wall encoding and color handling,
- `src/maze/maze.py`: maze generation logic independent from the player controls,
- `src/engine/solver.py`: solving algorithms that can be reused with another front-end,
- `src/utils/parsing.py`: configuration loading and validation,
- `src/utils/maze_utils.py`: export logic for writing a maze to a file,
- `src/engine/navigator.py`: movement validation logic for a player or bot.

This separation makes it possible to reuse the data model and algorithms in another CLI, graphical front-end, or testing harness without rewriting the core logic.

## Team and project management

### Roles of the team members

The roles were distributed according to the git history and the implemented modules.

| Member   | Main contribution                                                                     |
| -------- | ------------------------------------------------------------------------------------- |
| finorak  | Core maze model, generation logic, configuration handling, documentation              |
| trakotos | Application integration, navigation, solving flow, window behavior, final refactoring |
| finorako | Project structure, configuration validation, documentation cleanup, code readability  |

### Planning and evolution

The project evolved in several steps:

1. base structure and packaging,
2. configuration parsing and validation,
3. maze data model and generation,
4. solver integration,
5. rendering and user interaction,
6. export feature and final bug fixes,
7. documentation and cleanup.

The original plan focused on generating and displaying mazes. It later expanded to include a solver, player movement, file export, help window, and a 42 logo feature.

### What worked well

- clear separation between maze data, solver, and UI,
- iterative development with frequent fixes,
- animated feedback for generation and solving,
- reusable configuration parsing and export logic,
- easy testing through the provided Makefile targets.

### What could be improved

- reduce the amount of state shared between UI and engine,
- simplify some thread and rendering interactions,
- improve naming consistency in a few modules,
- add more automated tests for generation and solving,
- document more edge cases for invalid configuration values.

### Tools used

- Git and GitHub for version control and collaboration,
- Makefile for installation and execution shortcuts,
- Python virtual environment for dependency isolation,
- MLX for the graphical interface,
- pygame-ce for audio handling,
- mypy and flake8 for static checks.

## Features

- maze generation from a text configuration file,
- perfect and imperfect maze modes,
- animated generation and solving,
- two solving strategies,
- player movement inside the maze,
- custom wall color cycling,
- entry and exit repositioning with the mouse,
- export to a maze text file,
- help window and sound effects,
- optional 42 block display in the center of the maze.

## Resources

### Technical references

- https://en.wikipedia.org/wiki/Maze_generation_algorithm
- https://en.wikipedia.org/wiki/Depth-first_search
- https://docs.python.org/3/
- https://www.pygame.org/docs/
- MLX documentation and course material used for the graphical interface

### AI usage

AI was used to help with:

- structuring and polishing this README,
- summarizing the project from the source code,
- organizing the sections required by the 42 subject,
- checking that the documentation covers the configuration format, the algorithm choice, reusable parts, and team management.

AI was not used to implement the maze logic itself in this documentation task.
