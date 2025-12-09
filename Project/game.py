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
        self.dice_roll_number = [None, None]
        self.button = tk.Button(self.root, text="Roll Dice", command=self.roll, bg="darkblue", fg="white")
        self.canvas.create_window(20, 2, window=self.button, anchor="nw")
        self.switch_button = tk.Button(self.root, text="Switch", command=self.switch_player, bg="darkred", fg="white")
        self.canvas.create_window(160, 2, window=self.switch_button, anchor="nw")
        self.move_button = tk.Button(self.root, text=f"move {self.player_data[1]}", command=self.handle_roll,
                                     bg=f"{self.active_color}", fg="white")
        self.canvas.create_window(20, 35, window=self.move_button, anchor="nw")
        self.highlight_active_players()


    def roll(self):
        self.button.config(state="disabled", bg="gray")
        self.dice_roll_number = self.dice.roll()
        color, token_name = self.player_data
        self.players[color].recent_player = [color, token_name]
        self.player_data = [color, token_name]
        self.check_token_at_base()


    def switch_player(self):
        player_color = self.player_data[0]
        self.players[player_color].switch_token()
        change_no = self.players[player_color].player_no
        self.move_button.config(text=f"move player-{change_no + 1}")
        self.player_data[1] = f"{player_color}-{change_no}"


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
            six_index = 0
        dice = self.dice_roll_number[six_index]

        for token in player.tokens:
            if player.token_position[token][0] == "base" and dice != 6:
                all_player_base += 1

        if all_player_base == len(player.tokens):
            self.switch_next_color()
            return
        return six_index


    def handle_roll(self):
        if not self.dice_roll_number:
            return

        color, token_name = self.player_data
        player = self.players[color]
        current_state, current_index = player.token_position[token_name]
        move_successful = False
        six_index = self.check_token_at_base()
        dice = self.dice_roll_number[six_index]
        if current_state == "base":
            if dice == 6:
                start_index = player.start_index_on_main[color]
                player.enter_path(token_name, start_index)
                move_successful = True
            else:
                print(f"{token_name} cannot move out of base without rolling a 6.")
        else:
            player.move_steps(token_name, dice, on_complete=self.move_finished(six_index))
            print(f"{token_name} moved {dice} steps.")
            move_successful = True

        if move_successful and current_state == "base":
            self.move_finished(six_index)


    def move_finished(self, index):
        if self.dice_roll_number:
            self.dice_roll_number.pop(index)

        if not self.dice_roll_number:
            self.switch_next_color()
        else:
            print(f"One move done. Next die: {self.dice_roll_number[0]}")
            self.highlight_active_players()


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


    def check_for_kick(self, current_color, current_token_name):
        player = self.players[current_color]
        state, index = player.token_position[current_token_name]

        if state != "main":
            return
        safe_indices = [1, 14, 28, 42]

        if index in safe_indices:
            print(f"Token {current_token_name} is on a safe spot. No kick possible {index}.")
            return
        for other_color, other_player in self.players.items():
            if other_color == current_color:
                continue

            for token_name in other_player.tokens:
                token_state, token_index = other_player.token_position[token_name]

                if token_state == "main" and token_index == index:
                    print(f"KICK! {current_token_name} kicked {token_name} back to base.")

                    base_coords = other_color.home_paths[token_name]
                    other_player.move_token_visual(token_name, base_coords)
                    other_player.token_position[token_name] = ("base", 0)

