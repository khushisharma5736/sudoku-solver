# Sudoku Solver Mini Project (Python + Tkinter)

A simple, GUI-based Sudoku Solver built using Python and Tkinter, made as a 2nd-year B.Tech Computer Science mini-project. It demonstrates the
Backtracking algorithm applied to a real, well-known problem.

---

## 1. Project Overview

This application displays a standard 9×9 Sudoku grid in a window.
The user can type numbers into the grid manually, then use the buttons to solve the puzzle, check whether it is valid, load a ready-made example, or generate a brand-new random puzzle.

The actual solving is done using a classic **Backtracking** algorithm.


## 2. Features
Solve: Instantly solves the Sudoku puzzle using the backtracking algorithm and displays the time taken.
Clear: Clears all values from the Sudoku grid.
Load Example Puzzle: Loads one of three built-in Sudoku puzzles (cycles through them).
Check Validity: Checks the current puzzle for Sudoku rule violations without solving it.
Generate Random Puzzle: Generates a new random Sudoku puzzle using randomized backtracking.
Step-by-Step Solve: Animates the solving process, showing each step of the backtracking algorithm, including backtracking when incorrect choices are made.
Color-Coded Cells: User-entered numbers appear in black, while algorithm-generated numbers appear in blue.
Conflict Highlighting: Highlights cells with rule violations in red.
Input Validation: Accepts only digits 1–9 and blocks invalid input automatically.
Solving Time Display: Displays the total time taken by the algorithm to solve the puzzle.


## 3. Folder Structure
sudoku_solver/
│
├── main.py     -> Entry point. Run this file to start the app.
├── gui.py      -> All Tkinter GUI code (grid, buttons, screen updates).
├── solver.py   -> All Sudoku logic (backtracking algorithm, validitychecks, random puzzle generation, example puzzles).
└── README.md   -> This file.


## 4. How to Run the Project

**Requirements:** Python 3.x 
1. Download/copy all three files (`main.py`, `gui.py`, `solver.py`)into the same folder.
2. Open a terminal in that folder.
3. Run:
   python main.py
4. The Sudoku Solver window will open. Type numbers into the grid, or
   click **Load Example Puzzle** / **Generate Random Puzzle** to begin.


## 5. Future Improvements

These are good next steps if extending this project further:
1. Difficulty Levels (Easy/Medium/Hard): Generates puzzles with varying difficulty based on the number of pre-filled clues, allowing users to choose how challenging the puzzle is.
2. Save/Load Puzzles: Enables users to save the current Sudoku state to a text or JSON file and load it later to continue solving.
3. Undo/Redo: Allows users to undo and redo their manual inputs, improving usability and experimentation while solving.
4. Hint Button: Provides a single correct value for an empty cell without fully solving the puzzle, helping users when they get stuck.
5. Sound/Animation Polish: Adds simple sound effects and smooth animations during step-by-step solving to make the demonstration more interactive and engaging.
