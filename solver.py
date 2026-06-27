"""
This file contains all the "logic" of the project -- nothing about
the screen/buttons is here, only the Sudoku rules and the Backtracking
algorithm.
"""

import random
GRID_SIZE = 9   # a standard sudoku grid is 9 rows x 9 columns
BOX_SIZE = 3    # each mini box inside the grid is 3 x 3

# BASIC HELPER FUNCTIONS

def find_empty_cell(grid):
    """
    Scans the grid from top-left to bottom-right and returns the
    (row, col) of the first empty cell (a cell with value 0).
    If there is no empty cell, it returns None -- which means the
    grid is completely filled.
    """
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                return row, col
    return None

def is_valid(grid, row, col, num):
    """
    Checks whether placing 'num' at position (row, col) would break
    any of the three Sudoku rules:
        - the number must not already be in the same row
        - not already be in the same column
        - not already be in the same 3x3 box
    Returns True if it is safe to place the number, False otherwise.
    """

    # Rule 1: check the row
    for c in range(GRID_SIZE):
        if grid[row][c] == num:
            return False

    # Rule 2: check the column
    for r in range(GRID_SIZE):
        if grid[r][col] == num:
            return False

    # Rule 3: check the 3x3 box that (row, col) belongs to
    box_row_start = (row // BOX_SIZE) * BOX_SIZE
    box_col_start = (col // BOX_SIZE) * BOX_SIZE
    for r in range(box_row_start, box_row_start + BOX_SIZE):
        for c in range(box_col_start, box_col_start + BOX_SIZE):
            if grid[r][c] == num:
                return False
    return True  # passed all three checks, so it is safe

# THE MAIN BACKTRACKING SOLVER

def solve_sudoku(grid):
    """
    Solves the given 9x9 grid IN PLACE using backtracking.
    Returns:
        True  -> if the puzzle was solved (the grid itself is updated)
        False -> if the puzzle has no possible solution
    """

    empty_cell = find_empty_cell(grid)

    # Base case: no empty cell left means the puzzle is already solved
    if empty_cell is None:
        return True

    row, col = empty_cell

    # Try every number from 1 to 9 in this empty cell
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num  # Step 1: tentatively place the number
           
            # Step 2: recursively try to solve the rest of the grid
            if solve_sudoku(grid):
                return True

            # Step 3 (BACKTRACK): if we reach here, placing 'num' did not lead to a solution, so undo it and try the next number
            grid[row][col] = 0
    # If no number (1-9) worked for this cell, this path is a dead end
    return False

def solve_sudoku_with_history(grid):
    """
    Does exactly the same job as solve_sudoku(), but it also records
    every single step (every number placed and every number removed)
    in a list called 'history'.
    """
    history = []

    def backtrack():
        empty_cell = find_empty_cell(grid)
        if empty_cell is None:
            return True
        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(grid, row, col, num):
                grid[row][col] = num
                history.append((row, col, num))     # record placing the number
                if backtrack():
                    return True
                grid[row][col] = 0
                history.append((row, col, 0))        # record undoing the number
        return False
    solved = backtrack()
    return solved, history

# CHECKING VALIDITY OF A (POSSIBLY INCOMPLETE) GRID
def get_conflicting_cells(grid):
    """
    Looks at the CURRENT grid (which may be only partially filled,
    e.g. numbers typed in by the user) and finds any cells that break
    the Sudoku rules -- i.e. the same number repeated in a row, column
    or 3x3 box. Empty cells (0) are simply ignored.
    """
    conflicts = set()

    # ---- check every row ----
    for row in range(GRID_SIZE):
        seen_at = {}  # maps number -> column where it was first seen
        for col in range(GRID_SIZE):
            value = grid[row][col]
            if value == 0:
                continue
            if value in seen_at:
                conflicts.add((row, col))
                conflicts.add((row, seen_at[value]))
            else:
                seen_at[value] = col

    # ---- check every column ----
    for col in range(GRID_SIZE):
        seen_at = {}  # maps number -> row where it was first seen
        for row in range(GRID_SIZE):
            value = grid[row][col]
            if value == 0:
                continue
            if value in seen_at:
                conflicts.add((row, col))
                conflicts.add((seen_at[value], col))
            else:
                seen_at[value] = row

    # ---- check every 3x3 box ----
    for box_row in range(0, GRID_SIZE, BOX_SIZE):
        for box_col in range(0, GRID_SIZE, BOX_SIZE):
            seen_at = {}  # maps number -> (row, col) where first seen
            for r in range(box_row, box_row + BOX_SIZE):
                for c in range(box_col, box_col + BOX_SIZE):
                    value = grid[r][c]
                    if value == 0:
                        continue
                    if value in seen_at:
                        conflicts.add((r, c))
                        conflicts.add(seen_at[value])
                    else:
                        seen_at[value] = (r, c)

    return list(conflicts)

# RANDOM PUZZLE GENERATION 


def generate_full_solution():
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def fill():
        empty_cell = find_empty_cell(grid)
        if empty_cell is None:
            return True
        row, col = empty_cell
        numbers = list(range(1, 10))
        random.shuffle(numbers)  # try numbers in random order
        for num in numbers:
            if is_valid(grid, row, col, num):
                grid[row][col] = num
                if fill():
                    return True
                grid[row][col] = 0
        return False+
    fill()
    return grid


def generate_random_puzzle(num_cells_to_remove=45):
    """
    Generates a random sudoku PUZZLE (not a fully solved grid) using
    simple logic suitable for a mini-project:
        1. Generate a complete, randomly filled, valid grid.
        2. Randomly pick a number of cells and empty them out (set to 0).
   """
    grid = generate_full_solution()

    all_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
    random.shuffle(all_cells)

    cells_to_clear = all_cells[:num_cells_to_remove]
    for row, col in cells_to_clear:
        grid[row][col] = 0

    return grid


# A FEW READY-MADE EXAMPLE PUZZLES (for the "Load Example Puzzle" button)


EXAMPLE_PUZZLES = [
    [[5, 3, 0, 0, 7, 0, 0, 0, 0],
     [6, 0, 0, 1, 9, 5, 0, 0, 0],
     [0, 9, 8, 0, 0, 0, 0, 6, 0],
     [8, 0, 0, 0, 6, 0, 0, 0, 3],
     [4, 0, 0, 8, 0, 3, 0, 0, 1],
     [7, 0, 0, 0, 2, 0, 0, 0, 6],
     [0, 6, 0, 0, 0, 0, 2, 8, 0],
     [0, 0, 0, 4, 1, 9, 0, 0, 5],
     [0, 0, 0, 0, 8, 0, 0, 7, 9]],

    [[0, 0, 0, 2, 6, 0, 7, 0, 1],
     [6, 8, 0, 0, 7, 0, 0, 9, 0],
     [1, 9, 0, 0, 0, 4, 5, 0, 0],
     [8, 2, 0, 1, 0, 0, 0, 4, 0],
     [0, 0, 4, 6, 0, 2, 9, 0, 0],
     [0, 5, 0, 0, 0, 3, 0, 2, 8],
     [0, 0, 9, 3, 0, 0, 0, 7, 4],
     [0, 4, 0, 0, 5, 0, 0, 3, 6],
     [7, 0, 3, 0, 1, 8, 0, 0, 0]],

    [[1, 0, 0, 4, 8, 9, 0, 0, 6],
     [7, 3, 0, 0, 0, 0, 0, 4, 0],
     [0, 0, 0, 0, 0, 1, 2, 9, 5],
     [0, 0, 7, 1, 2, 0, 6, 0, 0],
     [5, 0, 0, 7, 0, 3, 0, 0, 8],
     [0, 0, 6, 0, 9, 5, 7, 0, 0],
     [9, 1, 4, 6, 0, 0, 0, 0, 0],
     [0, 2, 0, 0, 0, 0, 0, 3, 7],
     [8, 0, 0, 5, 1, 2, 0, 0, 4]],
]
