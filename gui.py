""" 
This file builds the graphical user interface (GUI) using Tkinter.
It is responsible only for:
- drawing the 9x9 grid and the buttons
- reading what the user typed
- calling functions from solver.py to do the actual solving
- showing the results back on the screen
I have kept the GUI code separate from the solving logic (solver.py) to keep better understanding of the code.
"""

import time
import tkinter as tk
from tkinter import messagebox
import solver
GRID_SIZE = 9
BOX_SIZE = 3

# Colors used in the GUI (i kept them as simple constants so they are easy to change)
GIVEN_COLOR = "black"      # numbers typed by the user / part of the puzzle
SOLVED_COLOR = "blue"      # numbers filled in automatically by the algorithm
ERROR_COLOR = "#ffb3b3"    # light red background used to highlight conflicts
NORMAL_BG = "white"        # normal background color of a cell

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.entries = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        self.example_index = 0     # which example puzzle to load next
        self.is_animating = False  # True while "Step-by-Step Solve" is running
        # Build all the parts of the window, one by one
        self.build_title()
        self.build_grid()
        self.build_buttons()
        self.build_status_bar()
        
    def build_title(self):
        title_label = tk.Label(self.root, text="Sudoku Solver", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

    def build_grid(self):
        """
        Builds the 9x9 sudoku board. To make the 3x3 boxes visually stand out (like a real sudoku grid), we create 9 small Frames (one per 3x3 box) and place 9 Entry widgets inside each frame.
        """
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(padx=10, pady=5)

        # This "validate command" makes sure a cell can only ever contain an empty value or a single digit from 1 to 9.
        validate_command = (self.root.register(self.validate_input), "%P")

        for box_row in range(BOX_SIZE):
            for box_col in range(BOX_SIZE):
                box_frame = tk.Frame(grid_frame, borderwidth=2, relief="ridge")
                box_frame.grid(row=box_row, column=box_col, padx=2, pady=2)

                for inner_row in range(BOX_SIZE):
                    for inner_col in range(BOX_SIZE):
                        row = box_row * BOX_SIZE + inner_row
                        col = box_col * BOX_SIZE + inner_col

                        entry = tk.Entry(
                            box_frame, width=2, font=("Arial", 18),
                            justify="center", borderwidth=1, relief="solid",
                            validate="key", validatecommand=validate_command
                        )
                        entry.grid(row=inner_row, column=inner_col, padx=1, pady=1)
                        self.entries[row][col] = entry

    def build_buttons(self):
        """Creates all the action buttons required by the project."""
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=8)

        tk.Button(button_frame, text="Solve", width=16, command=self.solve_puzzle).grid(row=0, column=0, padx=4, pady=4)
        tk.Button(button_frame, text="Clear", width=16, command=self.clear_grid).grid(row=0, column=1, padx=4, pady=4)
        tk.Button(button_frame, text="Load Example Puzzle", width=20, command=self.load_example).grid(row=0, column=2, padx=4, pady=4)
        tk.Button(button_frame, text="Check Validity", width=16, command=self.check_validity).grid(row=1, column=0, padx=4, pady=4)
        tk.Button(button_frame, text="Generate Random Puzzle", width=20, command=self.generate_random).grid(row=1, column=1, padx=4, pady=4)
        tk.Button(button_frame, text="Step-by-Step Solve", width=20, command=self.step_solve).grid(row=1, column=2, padx=4, pady=4)

    def build_status_bar(self):
        """A simple label at the bottom used to show messages/errors/timing."""
        self.status_label = tk.Label(self.root, text="Enter a puzzle and click Solve, "
                                      "or try 'Load Example Puzzle'.",
                                      font=("Arial", 11), fg="darkgreen",
                                      wraplength=420, justify="center")
        self.status_label.pack(pady=8)

    def validate_input(self, new_value):
        """
        Tkinter calls this automatically every time a user types
        something into a cell. It must return True (allow the change)
        or False (reject the change).
        Allowed: empty string, or a single digit from 1 to 9.
        """
        if new_value == "":
            return True
        if len(new_value) == 1 and new_value in "123456789":
            return True
        return False

    def get_grid_from_entries(self):
        """Reads all 81 Entry widgets and returns a plain 9x9 list of ints."""
        grid = []
        for row in range(GRID_SIZE):
            row_values = []
            for col in range(GRID_SIZE):
                text = self.entries[row][col].get().strip()
                row_values.append(int(text) if text != "" else 0)
            grid.append(row_values)
        return grid

    def set_grid_to_entries(self, grid, text_color=GIVEN_COLOR):
        """Writes a 9x9 grid into the Entry widgets on screen."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                entry = self.entries[row][col]
                entry.delete(0, tk.END)
                value = grid[row][col]
                if value != 0:
                    entry.insert(0, str(value))
                entry.config(fg=text_color, bg=NORMAL_BG)

    def reset_cell_colors(self):
        """Removes any red 'conflict' highlighting from every cell."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.entries[row][col].config(bg=NORMAL_BG)

    def clear_grid(self):
        """Empties the whole board and resets colors and the status message."""
        if self.is_animating:
            return  # do not allow clearing while a step-by-step solve is running

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                entry = self.entries[row][col]
                entry.delete(0, tk.END)
                entry.config(fg=GIVEN_COLOR, bg=NORMAL_BG)

        self.set_status("Grid cleared. Enter a new puzzle.", "darkgreen")

    def load_example(self):
        """Loads one of the ready-made example puzzles from solver.py."""
        if self.is_animating:
            return

        puzzle = solver.EXAMPLE_PUZZLES[self.example_index]
        self.example_index = (self.example_index + 1) % len(solver.EXAMPLE_PUZZLES)
        self.reset_cell_colors()
        self.set_grid_to_entries(puzzle, text_color=GIVEN_COLOR)
        self.set_status("Example puzzle loaded. Click Solve or Step-by-Step Solve.",
                         "darkgreen")

    def generate_random(self):
        """Generates a brand-new random puzzle using solver.generate_random_puzzle()."""
        if self.is_animating:
            return

        puzzle = solver.generate_random_puzzle()
        self.reset_cell_colors()
        self.set_grid_to_entries(puzzle, text_color=GIVEN_COLOR)
        self.set_status("Random puzzle generated.", "darkgreen")

    def check_validity(self):
        """
        Checks the numbers currently on the board for rule violations (duplicate numbers in a row, column, or 3x3 box). This does NOT solve the puzzle -- it only checks what is already typed in.
        """
        grid = self.get_grid_from_entries()
        self.reset_cell_colors()

        conflicts = solver.get_conflicting_cells(grid)

        if conflicts:
            for row, col in conflicts:
                self.entries[row][col].config(bg=ERROR_COLOR)
            self.set_status(
                f"Invalid puzzle: {len(conflicts)} conflicting cell(s) found "
                f"(highlighted in red).", "red")
            return

        is_completely_filled = all(
            grid[r][c] != 0 for r in range(GRID_SIZE) for c in range(GRID_SIZE)
        )
        if is_completely_filled:
            self.set_status("Puzzle is completely filled and valid. Great job!", "darkgreen")
        else:
            self.set_status("No conflicts found so far. Puzzle is valid (but incomplete).", "darkgreen")

    def solve_puzzle(self):
        if self.is_animating:
            return

        grid = self.get_grid_from_entries()
        self.reset_cell_colors()

        # Step 1: make sure what the user typed does not already break the rules
        conflicts = solver.get_conflicting_cells(grid)
        if conflicts:
            for row, col in conflicts:
                self.entries[row][col].config(bg=ERROR_COLOR)
            self.set_status("Cannot solve: puzzle has conflicting numbers (shown in red).",
                             "red")
            return

        # Step 2: remember which cells were already filled by the user.
        # These stay black; whatever the algorithm fills in will turn blue.
        given_cells = {
            (r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] != 0
        }

        # Step 3: run the backtracking solver and measure how long it took
        start_time = time.time()
        solved = solver.solve_sudoku(grid)
        time_taken = time.time() - start_time

        if not solved:
            messagebox.showerror("No Solution", "This puzzle cannot be solved.")
            self.set_status("No solution exists for this puzzle.", "red")
            return

        # Step 4: display the result, coloring given vs. solved cells differently
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                entry = self.entries[row][col]
                entry.delete(0, tk.END)
                entry.insert(0, str(grid[row][col]))
                if (row, col) in given_cells:
                    entry.config(fg=GIVEN_COLOR)
                else:
                    entry.config(fg=SOLVED_COLOR)

        self.set_status(f"Solved successfully in {time_taken:.4f} seconds.", "darkgreen")

    def step_solve(self):
        """
        Solves the puzzle the same way as solve_puzzle(), but instead ofshowing the final answer immediately, it plays back every singlestep of the backtracking process so the user can SEE how thealgorithm works (numbers being placed, and sometimes removedagain when a wrong guess is detected).
        """
        if self.is_animating:
            return

        grid = self.get_grid_from_entries()
        self.reset_cell_colors()

        conflicts = solver.get_conflicting_cells(grid)
        if conflicts:
            for row, col in conflicts:
                self.entries[row][col].config(bg=ERROR_COLOR)
            self.set_status("Cannot solve: puzzle has conflicting numbers (shown in red).",
                             "red")
            return

        # Run the solver once to get the complete list of steps it took.
        # (The grid is solved instantly here; we then "replay" the steps
        # slowly on screen for the user to watch.)
        solved, history = solver.solve_sudoku_with_history(grid)

        if not solved:
            messagebox.showerror("No Solution", "This puzzle cannot be solved.")
            self.set_status("No solution exists for this puzzle.", "red")
            return

        self.set_status("Solving step-by-step... please watch the grid.", "darkblue")
        self.is_animating = True
        self.animate_steps(history, 0, time.time())

    def animate_steps(self, history, index, start_time):
        """
        Shows ONE step from 'history' on the screen, then schedules
        itself to run again after a short delay using self.root.after().
        This is the standard Tkinter way of creating a simple animation
        without freezing the window.
        """
        if index >= len(history):
            # All steps have been shown -- the puzzle is now fully solved
            self.is_animating = False
            time_taken = time.time() - start_time
            self.set_status(f"Step-by-step solve finished in {time_taken:.2f} seconds.",
                             "darkgreen")
            return

        row, col, value = history[index]
        entry = self.entries[row][col]
        entry.delete(0, tk.END)

        if value != 0:
            entry.insert(0, str(value))
            entry.config(fg=SOLVED_COLOR)
        # if value == 0, the cell is simply left empty (this is a backtrack /
        # "undo" step, where the algorithm removes a wrong guess)

        # Schedule the next step after a short delay (in milliseconds).
        # A smaller number here makes the animation faster.
        self.root.after(15, self.animate_steps, history, index + 1, start_time)

    def set_status(self, message, color="black"):
        """Updates the message shown at the bottom of the window."""
        self.status_label.config(text=message, fg=color)
