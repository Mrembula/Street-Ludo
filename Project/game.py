from player import  Player
import tkinter as tk

# home_centers = {"red": (181, 175),"green": (380, 175),"blue": (379, 379), "yellow": (178, 379)}
# start_blocks = {"red": (1, 6),"green": (8, 1),"yellow": (6, 13),"blue": (13, 8)}

class Game:
    def __init__(self, root, canvas, board, dice, colors, square_centers, color, active_player):
        self.root = root
        self.canvas = canvas
        self.board = board
        self.dice = dice
        self.active_color = color
        self.square_centers = square_centers
        self.player_data = [color, active_player]
        self.players = {color: Player(canvas, f"{color}", color, 10, len(colors), square_centers) for color in colors}

        # Place tokens in home
        self.players[color].recent_player = self.player_data
        self.turn_order = list(colors)
        self.current_turn = 0
        self.next_turn = 0
        self.dice_roll_number = (None, None)
        self.players = {color: Player(canvas, f"{color}", color, 10, len(colors), square_centers) for color in colors}
        self.players[color].recent_player = self.player_data
        self.button = tk.Button(self.root, text="Roll Dice", command=self.roll, bg="darkblue", fg="white")
        self.canvas.create_window(20, 2, window=self.button, anchor="nw")
        self.switch_button = tk.Button(self.root, text="Switch", command=self.switch_player, bg="darkred", fg="white")
        self.canvas.create_window(160, 2, window=self.switch_button, anchor="nw")
        self.move_button = tk.Button(self.root, text=f"move {self.player_data[1]}", command=self.handle_roll, bg=f"{self.active_color}", fg="white")
        self.canvas.create_window(20, 35, window=self.move_button, anchor="nw")
        self.highlight_active_players()

    def switch_player(self):
        self.players[self.player_data[0]].switch_token()
        change_no =self.players[self.player_data[0]].player_no
        self.move_button.config(text=f"move player-{change_no + 1}")


    def roll(self):
        self.dice_roll_number = self.dice.roll()
        color, token_name = self.player_data
        self.players[color].recent_player = [color, token_name]
        self.player_data = [color, token_name]
        self.switch_next_color()


    def highlight_active_players(self) :
        for token_name, token_id in self.players[self.active_color].tokens.items():
            if token_name.startswith(self.active_color) and self.next_turn == self.current_turn:
                self.canvas.itemconfig(token_id, fill="gold", outline="gold", width=3)
            else:
                self.canvas.itemconfig(token_id, fill=f"{self.active_color}", outline="black", width=3)
        self.players[self.active_color].show_active_player(3)


    def handle_roll(self):
        color, token_name = self.player_data
        for dice in self.dice_roll_number:
            if self.players[color].token_position[token_name][0] == "base":
                if dice == 6:
                    self.players[color].enter_path(token_name)
                else:
                    # create a move button when pressed steps will be happening
                    self.highlight_active_players()
            else:
                self.players[color].move_steps(token_name, dice)


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
        self.move_button.config(bg=self.active_color)