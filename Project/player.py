import tkinter as tk

# Remove: from board import Board

CELL = 40
GRID = 15
W = H = GRID * CELL

base_coords = {"red": [(4, 4), (5, 4), (4, 5), (5, 5)], "green": [(10, 4), (9, 4), (9, 5), (10, 5)],
             "blue": [(9, 9), (10, 9), (9, 10), (10, 10)], "yellow": [(4, 9), (5, 9), (4, 10), (5, 10)]}

# Bit of glitch on the player movement. Counts twice on some steps. Got worse without getting better
def index_to_coord(index, cols=GRID, cell_size=CELL):
    row = index // cols
    col = index % cols
    x = col * cell_size + cell_size // 2
    y = row * cell_size + cell_size // 2
    return x, y


class Player:
    def __init__(self, canvas: tk.Canvas, board, name, color="red", radius=10, num_players=0, centers=None):
        self.canvas = canvas
        self.board = board  # 2. Store the passed board instance
        self.radius = radius
        self.token_id = None
        self.all_player = {}
        self.tokens = {}
        self.current_index = []
        self.square_centers = centers
        self.home_paths = {}
        self.total_slots = num_players
        self.active_token_index = 0
        self.player_no = 1
        self.token_position = {}
        self.recent_player = [color, name]
        # board-related
        self.stacks = {f"{color}-{i}": [] for i in range(4)}
        self.token_indices = {f"{color}-{i + 1}": 0 for color in ['red', 'green', 'blue', 'yellow'] for i in range(4)}
        self.start_index_on_main = {"red": 1, "green": 14, "blue": 28, "yellow": 42}
        self.home_entry_index = {"red": 50, "green": 12, "blue": 25, "yellow": 38}
        self.place_home_tokens()


    def place_home_tokens(self):
        color = self.recent_player[0]
        coords = base_coords[color]

        for i, (c, r) in enumerate(coords):
            cx, cy = self.board.get_coord(c, r)
            token_name = f"{color}-{i}"
            # Draw token
            self.draw_token(token_name, (cx, cy))
            self.tokens[token_name] = self.token_id
            self.home_paths[token_name] = (cx, cy)
            self.token_position[token_name] = ("base", 0)


    def draw_token(self, token_name, center_coords):
        cx, cy = center_coords
        self.token_id = self.canvas.create_oval(cx - self.radius, cy - self.radius, cx + self.radius, cy + self.radius, fill=self.recent_player[0], outline="black", width=2)


    def enter_path(self, token_name, start_index):
        player_color, self.player_no = self.recent_player[1].split('-')
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
        color, active_player = self.recent_player

        # Reset current visual highlight
        old_token_id = self.tokens[active_player]
        if old_token_id:
            self.canvas.itemconfig(old_token_id, fill=color, outline="black", width=2)

        # Extract current index (e.g., 'red-0' -> 0)
        current_idx = int(active_player.split('-')[-1])
        found_next = False

        for _ in range(len(self.tokens)):
            current_idx = (current_idx + 1) % len(self.tokens)
            next_name = f"{color}-{current_idx}"
            state, _ = self.token_position[next_name]

            # Only switch to tokens that are actually out on the board
            if state == "main":
                self.player_no = current_idx
                self.recent_player = [color, next_name]
                found_next = True
                break

        if not found_next:
            print("No other active tokens on the main path.")

        self.show_active_player(2)


    def move_token_visual(self, token_name, target_coord):
        token_id = self.tokens[token_name]
        cx, cy = target_coord
        self.canvas.coords(token_id, cx - self.radius, cy - self.radius, cx + self.radius, cy + self.radius)

        for follower_name in self.stacks.get(token_name, []):
            follower_id = self.tokens[follower_name]
            self.canvas.coords(follower_id, cx - self.radius, cy - self.radius, cx + self.radius, cy + self.radius)

        # self.update_stack_positions(token_name, new_state, new index)


    def update_stack_positions(self, token_name, state, index):
        self.token_position[token_name] = (state, index)
        for follower in self.stacks.get(token_name, []):
            self.token_position[follower] = (state, index)


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
        color = self.recent_player[0]
        path_length = len(self.board.main_path_coords)
        home_entry = self.home_entry_index[color]

        if current_state == "main":
            # Check if this specific step enters the home streak
            if current_index == home_entry:
                self.token_position[token_name] = ("finish", -1)
                # Continue animation in the 'finish' state immediately
                self.step_animation(token_name, remaining_steps, delay, on_complete)
                return

            next_index = (current_index + 1) % path_length
            target = self.board.main_path_coords[next_index]
            self.token_position[token_name] = ("main", next_index)
            self.move_token_visual(token_name, target)

        elif current_state == "finish":
            target_path = self.board.home_paths[color]
            next_idx_home = current_index + 1

            if next_idx_home < len(target_path):
                target = target_path[next_idx_home]
                self.token_position[token_name] = ("finish", next_idx_home)
                self.move_token_visual(token_name, target)

                # Check if this was the last possible cell (The Center)
                if next_idx_home == len(target_path) - 1:
                    self.token_position[token_name] = ("finished", 0)
                    self.canvas.itemconfig(self.tokens[token_name], fill="gray")
                    remaining_steps = 1  # Force stop after this step
            else:
                remaining_steps = 1  # Safety stop

        # Schedule next step
        self.canvas.after(delay, self.step_animation, token_name, remaining_steps - 1, delay, on_complete)