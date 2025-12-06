CELL = 40
GRID_SIZE = 15


class Board:
    def __init__(self, canvas):
        self.canvas = canvas
        self.main_path_coords = []  # The circular track
        self.home_paths = {}  # The colored paths into the center
        self.draw_board()
        self.home_block()
        self.construct_path_logic()

    def draw_cell(self, col, row, color, outline="#222"):
        x0, y0 = col * CELL, row * CELL
        x1, y1 = x0 + CELL, y0 + CELL
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=outline)
        return (x0 + x1) / 2, (y0 + y1) / 2  # Return center

    def draw_board(self):
        # Draw the Cross (White cells + Home Streaks)
        # Vertical column 6-8
        for row in range(15):
            for col in range(6, 9):
                color = 'white'
                # Home Streaks
                if col == 7:
                    if 1 <= row <= 5: color = 'green'
                    if 9 <= row <= 13: color = 'yellow'
                self.draw_cell(col, row, color)

        # Horizontal rows 6-8
        for col in range(15):
            for row in range(6, 9):
                # Skip the center overlap we already drew or will draw
                if 6 <= col <= 8: continue
                color = 'white'
                # Home Streaks
                if row == 7:
                    if 1 <= col <= 5: color = 'red'
                    if 9 <= col <= 13: color = 'blue'
                self.draw_cell(col, row, color)

        # Draw Start Safe Zones/ standby
        self.draw_cell(1, 6, 'red')
        self.draw_cell(8, 1, 'green')
        self.draw_cell(6, 13, 'yellow')
        self.draw_cell(13, 8, 'blue')

        # Seven box count
        self.draw_cell(8, 11, 'blue')
        self.draw_cell(11, 6, 'green')
        self.draw_cell(6, 3, 'red')
        self.draw_cell(3, 8, 'yellow')


    def get_coord(self, col, row):
        return col * CELL + CELL // 2, row * CELL + CELL // 2

    def construct_path_logic(self):
        path = [(c, 6) for c in range(0, 6)] # 1. Red's bottom track (moves right)
        path += [(6, r) for r in range(5, -1, -1)] # 2. Green's left track (moves up)
        path += [(7, 0), (8, 0)] # 3. Green's top track (moves right)
        path += [(8, r) for r in range(1, 6)] # 4. Green's right track (moves down)
        path += [(c, 6) for c in range(9, 15)] # 5. Blue's top track (moves right)
        path += [(14, 7), (14, 8)] # 6. Blue's right track (moves down)
        path += [(c, 8) for c in range(14, 8, -1)] # 7. Blue's bottom track (moves left)
        path += [(8, r) for r in range(9, 15)] # 8. Yellow's right track (moves down)
        path += [(7, 14), (6, 14)] # 9. Yellow's bottom track (moves left)
        path += [(6, r) for r in range(14, 8, -1)] # 10. Yellow's left track (moves up)
        path += [(c, 8) for c in range(5, -1, -1)] # 11. Red's bottom track (moves left)
        path += [(0, 7)]  # (0, 6) is already index0  12. Red's left track (moves up)

        # Convert to pixels
        self.main_path_coords = [self.get_coord(c, r) for c, r in path]

        # Home Streaks (Final paths to center)
        self.home_paths['red'] = [self.get_coord(c, 7) for c in range(1, 6)]
        self.home_paths['green'] = [self.get_coord(7, r) for r in range(1, 6)]
        self.home_paths['blue'] = [self.get_coord(c, 7) for c in range(13, 8, -1)]
        self.home_paths['yellow'] = [self.get_coord(7, r) for r in range(13, 8, -1)]

        # Center diamond
        cx = cy = 7.5 * CELL
        row = 2.5 * CELL
        points = [cx, cy - row, cx + row, cy, cx, cy + row, cx - row, cy]
        self.canvas.create_polygon(points, fill="lightblue", outline="black")


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