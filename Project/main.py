import tkinter as tk
from board import Board
from dice import Dice
import math
from tkinter import Canvas, simpledialog
from player import Player

CELL = 40
GRID = 15
W = H = GRID * CELL

def make_square_centers(columns, rows, left, top, cell_w, cell_h):
    centers = []
    for row in range(rows):
        for column in range(columns):
            cx = left + column * cell_w // 2
            cy = top + row * cell_h + cell_h // 2
            centers.append((cx, cy))
    return centers


def make_circle_centers(cx, cy, radius, count):
    centers = []
    for i in range(count):
        angle = 2 * math .pi* i / count
        x = cx + int(radius * math * math.cos(angle))
        y = cy + int(radius * math * math.sin(angle))
        centers.append((x, y))
    return centers


def main():
    root = tk.Tk()
    root.withdraw()
    num_players = simpledialog.askinteger( title="Number of players", prompt="Enter number of players (2-4):", minvalue=2, maxvalue=4, parent=root)
    if not num_players:
        root.destroy()
        return

    root.deiconify()
    canvas = tk.Canvas(root, width=W, height=H, bg="#1a1a1a", highlightthickness=0)
    canvas.pack()
    board = Board(canvas)
    dice = Dice(root, canvas, x=20, y=10)
    columns, rows = 10, 10
    cell_w, cell_h = 60, 40
    left, top = 20, 60
    square_centers = make_square_centers(columns, rows, left, top, cell_w, cell_h)

    colors = ['red', 'green', 'blue', 'yellow']
    players = []
    for i in range(num_players):
        name = f"Player-{i}"
        create_player = Player(canvas, name, colors[i % len(colors)], 10, num_players)
        create_player.attach_board(square_centers)
        create_player.place_on_square(0, slot=i, color=colors[i])
        players.append(create_player)
    root.mainloop()

if __name__=="__main__":
    main()