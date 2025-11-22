import tkinter as tk
from tkinter import Canvas

CELL = 40
# GRID = 15
# W = H = GRID * CELL

class Board:
    def __init__(self, canvas):
        self.canvas = canvas
        self.draw_board()


    def draw_cell(self, column, row , color, outline="#222"):
        x0, y0 = column * CELL, row * CELL
        x1, y1 = x0 + CELL, y0 + CELL
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=outline)

    def game_blocks(self):
            # Block around the game
        for row in range(0, 6):
            for column in range(6, 9):
                self.draw_cell(column, row, 'white')
        for row in range(9, 15):
            for column in range(6, 9):
                self.draw_cell(column, row, 'white')
        for column in range(0, 6):
            for row in range(6, 9):
                self.draw_cell(column, row, 'white')
        for column in range(9, 15):
            for row in range(6, 9):
                self.draw_cell(column, row, 'white')

    def start_block(self):
        # This is also considered stand by (No kicking zone)
        self.draw_cell(1, 6 , 'red')
        self.draw_cell(8, 1, 'green')
        self.draw_cell(6, 13, 'yellow')
        self.draw_cell(13, 8, 'blue')

    def seven_blocks(self):
        # seven box count (Nothing happens, but was just there)
        self.draw_cell(8, 11, 'blue')
        self.draw_cell(11, 6, 'green')
        self.draw_cell(6, 3, 'red')
        self.draw_cell( 3, 8, 'yellow')

    def home_block(self):
        for row in range(4, 6):
            for column in range(4, 6):
                self.draw_cell(column, row, 'red')
        for row in range(4, 6):
            for column in range(9, 11):
                self.draw_cell(column, row, 'green')
        for row in range(9, 11):
            for column in range(4, 6):
                self.draw_cell(column, row, 'yellow')
        for row in range(9, 11):
            for column in range(9, 11):
                self.draw_cell(column, row, 'blue')


    def draw_board(self):
        self.game_blocks()
        self.home_block()
        # Also considered as start block
        self.start_block()
        # Seven block box
        self.seven_blocks()

        # Center diamond
        cx = cy = 7.5 * CELL
        row = 2.5 * CELL
        points = [cx, cy-row, cx+row, cy, cx, cy+row, cx-row, cy]
        self.canvas.create_polygon(points, fill="lightblue", outline="black")

