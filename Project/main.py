import tkinter as tk
from board import Board
from dice import Dice

CELL = 40
GRID = 15
W = H = GRID * CELL

def main():
    # Game
    root = tk.Tk()
    root.configure(bg="#1a1a1a")
    root.title("Street Ludo")
    dice = Dice(root)
    board = Board(root)
    root.mainloop()


if __name__=="__main__":
    main()
