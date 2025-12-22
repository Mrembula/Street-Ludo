import tkinter as tk
from player import Player


class Game:
    def __init__(self, root, canvas, board, dice, colors, square_centers, color, active_player):
        self.root = root
        self.canvas = canvas
        self.board = board
        self.dice = dice
        self.active_color = color
        self.square_centers = square_centers
        self.player_data = [color, active_player]
        self.players = {color: Player(canvas, board, f"{color}-1", color, 10, len(colors), square_centers) for color in colors}
        self.players[color].recent_player = self.player_data
        self.turn_order = list(colors)
        self.current_turn = 0
        self.next_turn = 0
        self.doubles_rolled = 0
        self.extra_turn = False
        self.dice_roll_number = []
        # UI Buttons
        self.button = tk.Button(self.root, text="Roll Dice", command=self.roll, bg="darkblue", fg="white")
        self.canvas.create_window(20, 2, window=self.button, anchor="nw")
        self.switch_button = tk.Button(self.root, text="Switch", command=self.switch_player, bg="darkred",
                                       fg="white")
        self.canvas.create_window(160, 2, window=self.switch_button, anchor="nw")
        self.move_button = tk.Button(self.root, text=f"Move {self.player_data[1]}", command=self.handle_roll,
                                     bg=f"{self.active_color}", fg="white", state="disabled")
        self.canvas.create_window(20, 35, window=self.move_button, anchor="nw")
        self.enter_button = tk.Button(self.root, text="Enter Player", command=self.handle_entry,
                                     bg=f"{self.active_color}", state="disabled", fg="white", anchor="nw")
        self.canvas.create_window(125, 35, window=self.enter_button, anchor="nw")
        self.highlight_active_players()


    def roll(self):
        self.button.config(state="disabled", bg="gray")
        self.dice_roll_number = self.dice.roll()
        self.extra_turn = False

        # Rule: Double 6 or Doubles grants an extra turn
        if self.dice_roll_number[0] == self.dice_roll_number[1]:
            self.extra_turn = True
            if self.dice_roll_number == [6, 6]:
                self.doubles_rolled += 1

        self.move_button.config(state="normal")
        if 6 in self.dice_roll_number:
            self.enter_button.config(state="normal", bg=self.active_color)

        # Check if the player is stuck (no 6 and everyone is base/finished)
        if not self.has_movable_tokens():
            # Wait a second so user sees the dice, then switch
            self.root.after(1000, self.switch_next_color)


    def has_movable_tokens(self):
        player = self.players[self.active_color]
        has_six = 6 in self.dice_roll_number

        for token_name in player.tokens:
            state, _ = player.token_position[token_name]
            if state == "main" or state == "finish":
                return True
            if state == "base" and has_six:
                return True
        return False


    def switch_player(self):
        player = self.players[self.active_color]

        # 1. Tell the player object to cycle to the next token index (0-3)
        player.active_token_index = (player.active_token_index + 1) % 4
        new_token_name = f"{self.active_color}-{player.active_token_index + 1}"

        # 2. Update the Game's tracking data
        self.player_data[1] = new_token_name

        # 3. Update the button text so the user knows who they are moving
        self.move_button.config(text=f"Move {new_token_name}")

        # 4. Visual feedback
        self.highlight_active_players()


    def highlight_active_players(self):
        # 1. First, reset EVERY token for EVERY player to their base color
        for p_color, p_obj in self.players.items():
            for t_name, t_id in p_obj.tokens.items():
                self.canvas.itemconfig(t_id, fill=p_color, outline="black", width=2)

        # 2. Now, specifically highlight only the one active token in gold
        active_color, active_token_name = self.player_data
        active_player_obj = self.players[active_color]

        active_token_id = active_player_obj.tokens.get(active_token_name)
        if active_token_id:
            self.canvas.itemconfig(active_token_id, fill="gold", outline="gold", width=4)


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
        player = self.players[self.active_color]

        # Find the first token that is actually IN the base
        token_to_enter = None
        for t_name in player.tokens:
            if player.token_position[t_name][0] == "base":
                token_to_enter = t_name
                break

        if token_to_enter:
            self.move_button.config(state="disabled")
            self.enter_button.config(state="disabled")

            # Move it to the start
            start_idx = player.start_index_on_main[self.active_color]
            player.enter_path(token_to_enter, start_idx)

            # Find where the '6' is in the dice list and pop it
            if 6 in self.dice_roll_number:
                six_index = self.dice_roll_number.index(6)
                self.move_finished(six_index)
        else:
            print("All tokens are already out of base!")


    def handle_roll(self):
        if not self.dice_roll_number:
            return

        color, token_name = self.player_data
        player = self.players[color]
        state, index = player.token_position.get(token_name, ("base", 0))

        if state == "base":
            # ...look for ANY token that is already on the 'main' track or 'finish' track
            movable_token = None
            for t_name in player.tokens:
                t_state, _ = player.token_position[t_name]
                if t_state in ["main", "finish"]:
                    movable_token = t_name
                    break

            if movable_token:
                # Automatically switch to the movable token so the click isn't wasted
                self.player_data[1] = movable_token
                token_name = movable_token
                # state, index = player.token_position[token_name]
                # print(f"Auto-switched to {token_name} because it is on the board.")
            else:
                # No tokens are on the board!
                # If they don't have a 6, they are stuck.
                if 6 not in self.dice_roll_number:
                    # print("No movable tokens. Switching turn.")
                    self.switch_next_color()
                    return
                else:
                    # print("You must press 'Enter Player' to move a token out of base.")
                    return  # Don't pop the dice! Let them press Enter Player instead.

        # If we reached here, we have a valid token to move
        self.move_button.config(state="disabled")
        self.enter_button.config(state="disabled")

        dice_val = self.dice_roll_number[0]
        player.move_steps(token_name, dice_val, on_complete=lambda: self.move_finished(0))


    def move_finished(self, dice_index):
        if self.dice_roll_number:
            self.dice_roll_number.pop(dice_index)

        color, token_name = self.player_data

        # Check for kick
        if self.check_for_kick(color, token_name):
            self.extra_turn = True

        # Check for win
        if self.check_win():
            self.canvas.create_text(300, 300, text=f"{self.active_color.upper()} WINS!",
                                    font=("Arial", 30, "bold"), fill="white")
            return

        # Handle remaining dice or turn end
        if self.dice_roll_number:
            self.move_button.config(state="normal")
            if 6 in self.dice_roll_number:
                self.enter_button.config(state="normal")
            self.highlight_active_players()
        else:
            if self.extra_turn:
                # Award extra roll
                self.button.config(state="normal", bg="darkblue")
                self.move_button.config(state="disabled")
                self.enter_button.config(state="disabled")
            else:
                self.switch_next_color()

    def switch_next_color(self):
        # Move to next index in turn order
        current_idx = self.turn_order.index(self.active_color)
        next_idx = (current_idx + 1) % len(self.turn_order)

        self.active_color = self.turn_order[next_idx]
        # Default to the first token of the new player
        self.player_data = [self.active_color, f"{self.active_color}-1"]

        # Update buttons and UI
        self.move_button.config(bg=self.active_color, text=f"move {self.player_data[1]}")
        self.enter_button.config(bg=self.active_color)
        self.button.config(state="normal", bg="darkblue")

        # Update highlights once at the end
        self.highlight_active_players()


    def check_win(self):
        player = self.players[self.active_color]
        return all(player.token_position[t][0] == "finished" for t in player.tokens)

    def check_for_kick(self, current_color, current_token_name):
        player = self.players[current_color]
        state, index = player.token_position[current_token_name]
        if state != "main": return False

        # Safe Zones
        if index in player.start_index_on_main.values(): return False

        kick_occurred = False
        for other_color, other_player in self.players.items():
            if other_color == current_color: continue
            for t_name, (t_state, t_index) in other_player.token_position.items():
                if t_state == "main" and t_index == index:
                    # Kick it back to base
                    other_player.token_position[t_name] = ("base", 0)
                    base_coord = other_player.home_paths[t_name]
                    other_player.move_token_visual(t_name, base_coord)
                    kick_occurred = True
        return kick_occurred



    '''
    def switch_player(self):
        player = self.players[self.active_color]
        player.switch_token()
        self.player_data[1] = player.recent_player[1]
        self.move_button.config(text=f"Move {self.player_data[1]}")

    def highlight_active_players(self):
        # Clear highlights for all
        for p_color, p_obj in self.players.items():
            for t_id in p_obj.tokens.values():
                self.canvas.itemconfig(t_id, width=2, outline="black")

        # Highlight current player's tokens
        active_player = self.players[self.active_color]
        active_token_name = self.player_data[1]
        tid = active_player.tokens[active_token_name]
        self.canvas.itemconfig(tid, width=4, outline="gold")
    '''