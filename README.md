# Sudoku Solver — Mini Project (Python + Tkinter)

A simple, GUI-based Sudoku Solver built using Python and Tkinter, made
as a 2nd-year B.Tech Computer Science mini-project. It demonstrates the
**Backtracking algorithm** applied to a real, well-known problem.

---

## 1. Project Overview

This application displays a standard 9×9 Sudoku grid in a window.
The user can type numbers into the grid manually, then use the buttons
to solve the puzzle, check whether it is valid, load a ready-made
example, or generate a brand-new random puzzle.

The actual solving is done using a classic **Backtracking** algorithm
— a "trial and error with undo" technique commonly taught in DSA
courses.

---

## 2. Features

| Feature                  | Description                                                            |
|---------------------------|------------------------------------------------------------------------|
| **Solve**                | Instantly solves the puzzle using backtracking and shows the time taken. |
| **Clear**                | Empties the whole grid.                                                |
| **Load Example Puzzle**  | Loads one of 3 built-in example puzzles (cycles through them).         |
| **Check Validity**       | Checks the current grid for rule violations (duplicate numbers) without solving it. |
| **Generate Random Puzzle** | Creates a brand-new random puzzle using simple randomized backtracking. |
| **Step-by-Step Solve**   | Animates the backtracking process cell-by-cell so you can *watch* the algorithm work, including its "wrong guesses" being undone. |
| Color-coded cells         | Numbers you type stay **black**; numbers filled in by the algorithm turn **blue**. |
| Conflict highlighting     | Cells that break Sudoku rules are highlighted in **red**.              |
| Input validation          | Only digits 1–9 can be typed; anything else is blocked automatically. |
| Solving time display      | Shows how long the backtracking algorithm took, in seconds.            |

---

## 3. Folder Structure

```
sudoku_solver/
│
├── main.py     -> Entry point. Run this file to start the app.
├── gui.py      -> All Tkinter GUI code (grid, buttons, screen updates).
├── solver.py   -> All Sudoku logic (backtracking algorithm, validity
│                  checks, random puzzle generation, example puzzles).
└── README.md   -> This file.
```

Keeping the "logic" (`solver.py`) separate from the "interface"
(`gui.py`) is a basic good programming practice — it means the solving
algorithm could even be tested or reused without any GUI at all.

---

## 4. How to Run the Project

**Requirements:** Python 3.x (Tkinter comes built-in with most Python
installations — no extra installation/pip packages are needed).

1. Download/copy all three files (`main.py`, `gui.py`, `solver.py`)
   into the same folder.
2. Open a terminal in that folder.
3. Run:

   ```
   python main.py
   ```

   (On some systems you may need to type `python3 main.py` instead.)

4. The Sudoku Solver window will open. Type numbers into the grid, or
   click **Load Example Puzzle** / **Generate Random Puzzle** to begin.

---

## 5. Algorithm Explanation — Backtracking

Backtracking is a "smart brute-force" search technique. The idea, in
simple steps:

1. Find the next **empty cell** in the grid (scanning left-to-right,
   top-to-bottom).
2. Try placing each number from **1 to 9** in that cell.
3. For each number, check whether it is **valid**:
   - it must not already appear in the same **row**
   - it must not already appear in the same **column**
   - it must not already appear in the same **3×3 box**
4. If the number is valid, place it and **recursively** try to solve
   the rest of the grid with the next empty cell.
5. If that recursive attempt eventually fails (no number works for
   some later cell), **undo** the number just placed (set the cell
   back to empty) and try the **next** number in the current cell.
6. If none of the numbers 1–9 work for the current cell, this means an
   earlier decision was wrong — return `False` so the *previous*
   recursive call also backtracks and tries its next option.
7. The whole process stops when either:
   - every cell is filled validly → **solved**, or
   - every possibility has been exhausted → **no solution exists**.

This is exactly what `solve_sudoku()` in `solver.py` implements. The
function `solve_sudoku_with_history()` does the same thing but also
records every place/undo step into a list, which `gui.py` then plays
back slowly on screen for the **Step-by-Step Solve** feature.

### Why backtracking works for Sudoku
Sudoku has a limited number of rules (row, column, box), so instead of
trying *all* 9⁸¹ possible grids, backtracking quickly throws away any
partial grid that already breaks a rule — drastically cutting down the
number of possibilities it actually has to check.

### Other logic in `solver.py`
- `is_valid()` — checks the 3 Sudoku rules for one number/cell.
- `get_conflicting_cells()` — used by the **Check Validity** button; scans
  the whole grid (even if incomplete) for duplicate numbers.
- `generate_full_solution()` / `generate_random_puzzle()` — used by
  **Generate Random Puzzle**; builds a complete random solved grid using
  backtracking with shuffled number order, then removes some cells.
  (Note: this simple method does not guarantee a *unique* solution —
  a true puzzle generator needs extra uniqueness checks, which is
  outside the scope of this mini-project.)

---

## 6. Future Improvements

These are good next steps if extending this project further (e.g. for
a final-year project or to learn more advanced concepts):

- **Unique-solution puzzle generator** — verify that a generated puzzle
  has exactly one solution before removing more cells.
- **Difficulty levels** (Easy/Medium/Hard) based on number of given clues.
- **Save/Load puzzles** to/from a text or JSON file.
- **Undo/Redo** for manual user input.
- **Hint button** — reveal just one correct number instead of solving everything.
- **Smarter solving** using constraint propagation (e.g. the "Most
  Constrained Variable" heuristic) to make Step-by-Step Solve faster
  and more "human-like".
- **Mobile/web version** using HTML, CSS and JavaScript instead of Tkinter.
- **Sound/animation polish** for a more engaging step-by-step demo.

---

## 7. Credits / Notes for Viva

- Language: Python 3
- GUI Library: Tkinter (built into Python, no installation needed)
- Algorithm: Backtracking (recursive)
- No external Sudoku-solving libraries, databases, or AI/ML libraries were used —
  everything is implemented from scratch for learning purposes.
