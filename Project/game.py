# from PIL.ImageDraw2 import Font
from player import Player
import tkinter as tk

class Game:
    def __init__(self, root, canvas, board, dice, colors, square_centers, color, active_player):
        self.root = root
        self.canvas = canvas
        self.board = board
        self.dice = dice
        self.active_color = color
        self.square_centers = square_centers
        self.player_data = [color, active_player]
        self.players = {color: Player(canvas, board, f"{color}", color, 10, len(colors), square_centers) for color in colors}
        self.players[color].recent_player = self.player_data
        self.turn_order = list(colors)
        self.current_turn = 0
        self.next_turn = 0
        self.doubles_rolled = 0
        self.dice_roll_number = [None, None]
        self.button = tk.Button(self.root, text="Roll Dice", command=self.roll, bg="darkblue", fg="white")
        self.canvas.create_window(20, 2, window=self.button, anchor="nw")
        self.switch_button = tk.Button(self.root, text="Switch", command=self.switch_player, bg="darkred", fg="white")
        self.canvas.create_window(160, 2, window=self.switch_button, anchor="nw")
        self.move_button = tk.Button(self.root, text=f"move {self.player_data[1]}", command=self.handle_roll,
                                     bg=f"{self.active_color}", fg="white")
        self.canvas.create_window(20, 35, window=self.move_button, anchor="nw")
        self.enter_button = tk.Button(self.root, text="Enter player", command=self.handle_entry,
                                              bg=f"{self.active_color}",state="disabled",  fg="white", anchor="nw")
        self.canvas.create_window(125, 35, window=self.enter_button, anchor="nw")
        self.highlight_active_players()


    def roll(self):
        self.button.config(state="disabled", bg="gray")
        # self.move_button.config(state="disabled")
        self.dice_roll_number = self.dice.roll()

        if self.dice_roll_number == [6, 6]:
            self.doubles_rolled += 1
            # print(f"Doubles 6 rolled! ({self.dice_roll_number[0]}) Extra turn granted.")
        else:
            self.doubles_rolled = 0

        color, token_name = self.player_data
        self.players[color].recent_player = [color, token_name]
        self.player_data = [color, token_name]
        self.check_token_at_base()
        if 6 in self.dice_roll_number:
            self.enter_button.config(state="normal", bg=self.active_color)


    def switch_player(self):
        player_color = self.player_data[0]
        self.players[player_color].switch_token()

        new_token_name = self.players[player_color].recent_player[1]
        self.move_button.config(text=f"move {new_token_name}")
        self.player_data[1] = new_token_name


    def highlight_active_players(self):
        for token_name, token_id in self.players[self.active_color].tokens.items():
            if token_name.startswith(self.active_color) and self.next_turn == self.current_turn:
                self.canvas.itemconfig(token_id, fill="gold", outline="gold", width=3)
            else:
                self.canvas.itemconfig(token_id, fill=f"{self.active_color}", outline="black", width=3)
        self.players[self.active_color].show_active_player(3)


    def check_token_at_base(self):
        all_player_base = 0
        player = self.players[self.player_data[0]]

        if 6 in self.dice_roll_number:
            six_index = self.dice_roll_number.index(6)
        else:
            six_index = -1
        dice = self.dice_roll_number[six_index]

        for token in player.tokens:
            if player.token_position[token][0] == "base" and dice != 6:
                all_player_base += 1

        if all_player_base == len(player.tokens):
            self.switch_next_color()
            return
        return six_index


    def handle_entry(self):
        color, token_name = self.player_data
        player = self.players[color]
        six_index = self.check_token_at_base()

        token_to_enter = None
        for token_name in player.tokens:
            token_state, _ = player.token_position[token_name]
            if token_state == "base":
                token_to_enter = token_name

        if not token_to_enter:
            # print("No tokens in base to enter.")
            return

        if token_to_enter != token_name:
            # print(f"Switching to {token_to_enter} for entry")
            player.show_active_player(3)
            player.recent_player = [color, token_to_enter]
            self.player_data = [color, token_to_enter]
            token_name = token_to_enter
            player.show_active_player(2)

        start_index = player.start_index_on_main[color]
        self.player_data = [color, token_name]
        player.enter_path(token_name, start_index)
        # print(f"{token_name} entered the path from base.")
        self.move_finished(six_index)


    def handle_roll(self):
        if not self.dice_roll_number:
            return

        color, token_name = self.player_data
        player = self.players[color]
        six_index = self.check_token_at_base()
        dice = self.dice_roll_number[six_index]
        current_state, current_index = player.token_position[token_name]
        print(current_state, current_index)
        can_move_active =  current_state != "finished" or current_state == "main"

        if not can_move_active:
            movable_token = None

            if not movable_token:
                for token_name in player.tokens:
                    state, _ = player.token_position[token_name]
                    if state in ["main", "finish"]:
                        movable_token = token_name
                        break

            if movable_token:
                # print(f"Auto-switching active token to {movable_token}...")
                player.show_active_player(3)
                self.player_data = [color, movable_token]
                player.recent_player = self.player_data
                player.show_active_player(2)
                token_name = movable_token
                current_state, current_index = player.token_position[token_name]

            else:
                # print(f"No movable tokens for dice {dice}. Consuming roll.")
                self.dice_roll_number.pop(six_index)
                self.move_button.config(state="normal")
                self.highlight_active_players()
                return

        if current_state in ["main", "finish"]:
            # Normal move with animation (uses callback)
            player.move_steps(token_name, dice, on_complete=lambda: self.move_finished(six_index))
            # print(f"{token_name} moved {dice} steps.")
        # self.move_button.config(state="disabled")


    def move_finished(self, index):
        # player = self.players[self.player_data[0]]
        color, token_name = self.player_data
        kick_occurred = self.check_for_kick(color, token_name)

        if self.check_win():
            center_x, center_y = 300, 300
            self.canvas.create_text(center_x, center_y, text=f"{self.active_color.upper()} WINS!",
                                    Font=("Arial", 24, "bold"), fill="black")

            self.button.config(state="disabled")
            self.move_button.config(state="disabled")
            self.switch_button.config(state="disabled")

        if self.dice_roll_number:
            self.dice_roll_number.pop(index)

        if kick_occurred or self.doubles_rolled > 0:
            # print("Play again due to kick or doubles.")

            if not self.dice_roll_number:
                self.button.config(state="normal", bg="darkblue")
                return

        if not self.dice_roll_number:
            self.switch_next_color()
        else:
            # print(f"One move done. Next die: {self.dice_roll_number[0]}")
            self.highlight_active_players()
        if self.dice_roll_number and self.dice_roll_number[0] != 6:
            self.enter_button.config(state="disabled", bg="gray")
        self.check_for_stacking(color, token_name)
        # kick_occurred = self.check_for_kick(color, token_name)


    def switch_next_color(self):
        self.current_turn = self.turn_order.index(self.player_data[0])
        self.next_turn = (self.current_turn + 1) % len(self.turn_order)
        next_color = self.turn_order[self.next_turn]
        self.highlight_active_players()
        self.active_color = next_color
        self.player_data = [self.active_color, f"{self.active_color}-1"]
        self.players[next_color].recent_player = self.player_data
        self.next_turn = self.current_turn
        self.highlight_active_players()
        self.move_button.config(bg=self.active_color, text=f"move {self.active_color}-1")
        self.button.config(state="normal", bg="darkblue")


    def check_for_stacking(self, color, leader_name):
        player = self.players[color]
        state, index = player.token_position[leader_name]
        if state != "main":
            return

        safe_indices = list(player.start_index_on_main.values())

        if index in safe_indices:
            if player.stacks[leader_name]:
                # print(f"Safe Zone! {leader_name} stacking is splitting")
                for follower in player.stacks[leader_name]:
                    player.token_position[follower] = ("main", index)
                player.stacks[leader_name] = []
            return

        for other_token in player.tokens:
            if other_token == leader_name:
                continue
            other_state, other_index = player.token_position[other_token]
            is_already_follower = any(other_token in s for s in player.stacks.values())

            if other_state == "main" and other_index == index and not is_already_follower:
                # print(f"STACKING! {other_token} is stacking with {leader_name} at index {index}.")
                player.stacks[leader_name].append(other_token)
                player.token_position[other_token] = ("stacked", index)


    def check_win(self):
        player = self.players[self.active_color]
        finished_count = 0
        for token_name in player.tokens:
            state, _ = player.token_position[token_name]
            if state == "finished":
                finished_count += 1

        if finished_count == 4:
            return  True
        return False


    def check_for_kick(self, current_color, current_token_name):
        player = self.players[current_color]
        state, index = player.token_position[current_token_name]

        if state != "main":
            return
        # Safe Zones: Start points for all players (1, 14, 28, 42)
        safe_indices = player.start_index_on_main.values()

        if index in safe_indices:
            # print(f"Token {current_token_name} is on a safe spot. No kick possible {index}.")
            return

        kick_occurred = False
        for other_color, other_player in self.players.items():
            if other_color == current_color:
                continue # Don't kick yourself
            for token_name in other_player.tokens:
                token_state, token_index = other_player.token_position[token_name]

                if token_state == "main" and  token_index == index: # Create button for player to split a entery box
                    victim_name = token_name
                    # print(f"KICK! {current_token_name} kicked out {victim_name} at index {index}")
                    leader_base_coords = other_player.home_paths.get(victim_name)

                    if leader_base_coords:
                        other_player.move_token_visual(victim_name, leader_base_coords)
                        other_player.token_position[token_name] = ("base", 0)

                    if victim_name in other_player.stacks:
                        for follower_name in other_player.stacks[victim_name]:
                            follower_base_coords = other_player.home_paths[follower_name]

                            if follower_base_coords:
                                # print(f"Sending follower {follower_name} back to base.")
                                other_player.move_token_visual(follower_name, follower_base_coords)
                                other_player.token_position[follower_name] = ("base", 0)

                        other_player.stacks[victim_name] = []
                    kick_occurred = True

        return kick_occurred