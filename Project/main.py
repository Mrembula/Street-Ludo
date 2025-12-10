import tkinter as tk
from board import Board
from dice import Dice
from game import Game
from tkinter import simpledialog


CELL = 40
GRID = 15
# W = H = 640, 640

def create_square_centers(columns=15, rows=15, left=0, top=-40, cell_w=40, cell_h=40):
    centers = []
    for row in range(rows):
        for column in range(columns):
            cx = left + column * cell_w  + cell_w // 2
            cy = top + row * cell_h + cell_h  + cell_h // 2
            centers.append((cx, cy))
    return centers

def main():
    root = tk.Tk()
    root.title("Street Ludo")
    canvas = tk.Canvas(root, width=600, height=600, bg="#1a1a1a", highlightthickness=0)
    canvas.pack()
    root.withdraw()
    num_players = simpledialog.askinteger(title="Number of players", prompt="Enter number of players (2-4):",
                                minvalue=2, maxvalue=4, parent=root)
    if not num_players:
        root.destroy()
        return

    root.deiconify()
    board = Board(canvas)
    dice = Dice(root, canvas, x=20, y=10)

    columns, rows = 10, 10
    cell_w, cell_h = 60, 40
    left, top = 20, 60

    square_centers = create_square_centers(columns, rows, left, top, cell_w, cell_h)

    all_colors = ['red', 'green', 'blue', 'yellow']
    active_colors = all_colors[:num_players]

    game = Game(root, canvas, board, dice, active_colors, square_centers, active_colors[0], f'{active_colors[0]}-1')
    root.mainloop()

if __name__ == "__main__":
    main()

    '''
    canvas.create_oval(600 // 2 - 5, 600 // 2 - 5, 600 // 2 + 5, 600 // 2 + 5, fill="yellow", outline="black", width=2)

    for cx, cy in create_square_centers(15, 15, left=0, top=-40, cell_w=40, cell_h=40):
        canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="blue")
    '''