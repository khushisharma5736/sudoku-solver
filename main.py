"""
main.py

This is the ENTRY POINT of the Sudoku Solver mini-project.
Run this file (and only this file) to start the application:

    python main.py

It simply creates the main Tkinter window and hands control over to
the SudokuGUI class defined in gui.py, which builds the actual board
and buttons.
"""

import tkinter as tk
from gui import SudokuGUI


def main():
    root = tk.Tk()
    root.title("Sudoku Solver - Mini Project")
    root.resizable(False, False)  # keep the window a fixed, neat size

    app = SudokuGUI(root)  # build the whole interface

    root.mainloop()  # start the Tkinter event loop (keeps the window open)


if __name__ == "__main__":
    main()
