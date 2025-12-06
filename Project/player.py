import tkinter as tk
from board import Board

CELL = 40
GRID = 15
W = H = GRID * CELL

def index_to_coord(index, cols=GRID, cell_size=CELL):
    row = index // cols
    col = index % cols
    x = col * cell_size + cell_size // 2
    y = row * cell_size + cell_size // 2
    return x, y

class Player:
    def __init__(self, canvas: tk.Canvas, name, color="red", radius=10, num_players=0, centers=None):
        self.canvas = canvas
        self.name = name
        self.color = color
        self.radius = radius
        self.token_id = None
        self.label_id = None
        self.all_player = {}
        self.tokens = {}
        self.current_index = []
        self.square_centers = centers
        self.home_paths = {}
        self.total_slots = num_players
        self.active_token_index = 0
        self.player_no = 1
        self.token_position = {}
        self.board = Board(canvas)
        self.recent_player = [None, None]
        # board-related
        self.token_indices = {f"{color}-{i + 1}": 0 for color in ['red', 'green', 'blue', 'yellow'] for i in range(4)}  # self.color returns single color
        self.start_index_on_main = {"red": 1, "green": 14, "blue": 28, "yellow": 42}
        self.home_entry_index = {"red": 50, "green": 12, "blue": 25, "yellow": 38}
        self.place_home_tokens()

    def place_home_tokens(self):
        # Coordinates for the 4 tokens in the base
        base_coords = {"red": [(4, 4), (5, 4), (4, 5), (5, 5)], "green": [(10, 4), (9, 4), (9, 5), (10, 5)],
            "blue": [(9, 9), (10, 9), (9, 10), (10, 10)], "yellow": [(4, 9), (5, 9), (4, 10), (5, 10)]}
        coords = base_coords[self.color]
        for i, (c, r) in enumerate(coords):
            cx, cy = self.board.get_coord(c, r)
            token_name = f"{self.color}-{i}"
            # Draw token
            print(cx, cy)
            token_id = self.canvas.create_oval(cx - self.radius, cy - self.radius, cx + self.radius, cy + self.radius, fill=self.color, outline="black", width=3)
            self.tokens[token_name] = token_id
            self.home_paths[token_name] = (cx, cy)
            self.token_position[token_name] = ("base", 0)

        print(self.tokens)
    

    def enter_path(self, token_name, start_index):
        player_color, self.player_no = token_name.split('-')
        target_position = self.board.main_path_coords[start_index]
        self.move_token_visual(token_name, target_position)
        self.token_position[token_name] = ("main", start_index)


    def show_active_player(self, change):
        color, active_player = self.recent_player
        token_id = self.tokens[active_player]
        if change == 1:
            fill, outline = "gold", "gold"
        elif change == 2:
            fill, outline = color, "gold"
        else:
            fill, outline = color, "black"
        self.canvas.itemconfig(token_id, fill=fill, outline=outline, width=3)

    def switch_token(self):
        # Rotate to next player
        color, active_player = self.recent_player
        self.show_active_player(1) # Return player back to color
        self.active_token_index = (self.player_no + 1) % len(self.tokens)
        self.player_no = self.active_token_index
        self.recent_player = [color, f"{color}-{self.active_token_index}"]
        self.show_active_player(2)

    def move_token_visual(self, token_name, target_coord):
        token_id = self.tokens[token_name]
        cx, cy = target_coord
        self.canvas.coords(token_id, cx - self.radius, cy - self.radius, cx + self.radius, cy + self.radius)


    def move_steps(self, token_name, steps, on_complete=None):
        current_state, _ = self.token_position[token_name]
        if current_state == "base":
            if on_complete:
                on_complete()
            return
        self.step_animation(token_name, steps, 600, on_complete)


    def step_animation(self, token_name, remaining_steps, delay, on_complete):
        if remaining_steps <= 0:
            if on_complete:
                on_complete()
            return
        current_state, current_index = self.token_position[token_name]
        if current_state == "main":
            if current_state == self.home_entry_index:
                target_path = self.board.home_paths[self.color]
                cx, cy = target_path[0]
                self.move_token_visual(token_name, (cx, cy))
                self.token_position[token_name] = ("finish", 0)
            else:
                next_index = (current_index + 1) % 52
                cx, cy = self.board.main_path_coords[next_index]
                self.token_position[token_name] = ("main", next_index)
        elif current_state == "finish":
            target_path = self.board.home_paths[self.color]
            next_index = current_index
            if next_index < len(target_path):
                cx, cy = target_path[next_index]
                self.move_token_visual(token_name, (cx, cy))
                self.token_position[token_name] = ("finish", next_index)
            else:
                remaining_steps = 1
        self.canvas.after(delay, self.step_animation, token_name, remaining_steps - 1, delay, on_complete)




    '''
    def leave_board(self):
        for token_id in self.tokens.values():
            self.canvas.delete(token_id)
        self.tokens.clear()
        self.token_indices.clear()
    '''