import tkinter as tk

# from Project.game import start_blocks
from Project.path_data import center

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
        self.colors = color
        self.radius = radius
        self.token_id = None
        self.label_id = 1
        self.tokens = {}
        self.current_index = []
        self.square_centers = centers
        self.home_paths = {}
        self.total_slots = num_players
        self.active_player_index = 0

        self.recent_player = [None, None]
        # board-related
        self.token_indices = {f"{color}-{i + 1}": 0 for color in ['red', 'green', 'blue', 'yellow'] for i in range(4)}  # self.color returns single color
        self.start_blocks = {"red": (-121.0, 85.0), "green": (159.0, -115.0), "yellow": (79.0, 365.0),"blue": (359.0, 165.0)}
        self.start_indices = {color: self.nearest_index(row, col) for color, (row, col) in self.start_blocks.items()}


    def nearest_index(self, target_x, target_y):
        return min(range(len(self.square_centers)),
                   key=lambda i: (self.square_centers[i][0] - target_x) ** 2 + (self.square_centers[i][1] - target_y) ** 2)


    def place_home_tokens(self, home_center):
        cx, cy = home_center[self.colors]
        offsets = [(0, 0), (40, 2), (0, 41), (38, 42)]
        for i, (ox, oy) in enumerate(offsets, start=1):
            x = cx + ox
            y = cy + oy
            token_id = self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius,
                                    fill=self.colors, outline="black", width=3)
            self.tokens[f"{self.colors}-{i}"] = token_id
            self.home_paths[f"{self.colors}-{i}"] = (cx, cy) # Save this to check player in the home path

    
    def enter_path(self, token_name, start_index):
        token_id = self.tokens[token_name]
        player_color, active_player = token_name.split('-')
        self.label_id = active_player
        start_box = self.start_blocks[player_color]
        x, y = start_box
        print(self.nearest_index(x, y))
        self.canvas.move(token_id, start_box[0], start_box[1])
        print(f"{token_name} entered path at index {start_index}")


    def show_active_player(self, change):
        color, active_player = self.recent_player
        print("WTF no 2: ", active_player, self.recent_player)
        token_id = self.tokens[active_player]
        if change == 0:
            self.canvas.itemconfig(token_id, fill="gold", outline="gold", width=3)
        else:
            self.canvas.itemconfig(token_id, fill=f"{color}", outline="gold", width=3)

    
    def switch_token(self):
        # Rotate to next player
        color, active_player = self.recent_player
        self.show_active_player(0) # Return player back to color
        print("WTF: ", int(self.label_id) + 1)
        self.active_token_index = (int(self.label_id) + 1) % len(self.tokens)
        print("Check: ", self.active_token_index)
        self.label_id = active_player
        self.recent_player = [color, f"{color}-{self.active_token_index}"]
        print(f"Switched to {self.recent_player} player")
        self.show_active_player(1)


    def move_steps(self, token_name, steps, wrap=False, delay=500):
        if token_name not in self.tokens:
            raise ValueError(f"No token named {token_name} found for {self.colors}")
        token_id = self.tokens[token_name]
        current_index = self.token_indices.get(token_name)

        def step_animation(step_count, current_index):
            new_index = current_index + 1
            if wrap:
                new_index %= len(self.square_centers)
            else:
                new_index = min(new_index, len(self.square_centers) - 1)

            start = self.home_paths[token_name]
            x1, y1, x2, y2 = self.canvas.coords(token_id)
            if (x2 - self.radius) == start[0] and (y2 - self.radius) == start[1]:
                # print("current index: ", self.square_centers[current_index], self.tokens)
                print("Player can't move at home. We need a six")
                return

            cx, cy = self.square_centers[new_index]
            cx_old = (x1 + x2) / 2
            cy_old = (y1 + y2) / 2
            dx = cx - cx_old
            dy = cy - cy_old

            self.canvas.move(token_id, dx, dy)
            self.token_indices[token_name] = new_index

            if step_count < steps[0]:
                self.canvas.after(delay, step_animation, step_count + 1, new_index)
            else:
                print(f"{token_name} finished moving to index {new_index}")

        # Start animation
        step_animation(1, current_index)

    def leave_board(self):
        for token_id in self.tokens.values():
            self.canvas.delete(token_id)
        self.tokens.clear()
        self.token_indices.clear()


'''
    def move_steps(self, token_name, steps, wrap=False, delay=500):

        if token_name not in self.tokens:
            raise ValueError(f"No token named {token_name} found for {self.colors}")
        token_id = self.tokens[token_name]
        current_index = self.token_indices.get(token_name)

        def step_animation(step_count, current_index):
            new_index = current_index + 1
            if wrap:
                new_index %= len(self.square_centers)
            else:
                new_index = min(new_index, len(self.square_centers) - 1)

            start = self.home_paths[token_name]
            x1, y1, x2, y2 = self.canvas.coords(token_id)
            if (x2 - self.radius) == start[0] and  (y2 - self.radius) == start[1]:
                # print("current index: ", self.square_centers[current_index], self.tokens)
                print("Player can't move at home. We need a six")
                return

            cx, cy = self.square_centers[new_index]
            cx_old = (x1 + x2) / 2
            cy_old = (y1 + y2) / 2
            dx = cx - cx_old
            dy = cy - cy_old

            self.canvas.move(token_id, dx, dy)
            self.token_indices[token_name] = new_index

            if step_count < steps[0]:
                self.canvas.after(delay, step_animation, step_count + 1, new_index)
            else:
                print(f"{token_name} finished moving to index {new_index}")
        step_animation(1, current_index)

'''

'''

     def handle_roll(self, player_color, dice_value):
         if dice_value == 6:
             token_name = f"{player_color}-1"
             if self.token_indices.get(token_name) is None:
                 self.enter_path(token_name)
                 return

         for token_name in self.tokens:
             if token_name.startswith(player_color) and self.token_indices.get(token_name):
                 self.move_steps(token_name, dice_value)
                 break

         self.next_path()
     '''

