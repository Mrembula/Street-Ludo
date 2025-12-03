from player import  Player
import tkinter as tk

home_centers = {"red": (181, 175),"green": (380, 175),"blue": (379, 379), "yellow": (178, 379)}
start_blocks = {"red": (1, 6),"green": (8, 1),"yellow": (6, 13),"blue": (13, 8)}

class Game:
    def __init__(self, root, canvas, board, dice, colors, square_centers, color, activ_player):
        self.root = root
        self.canvas = canvas
        self.board = board
        self.dice = dice
        self.active_color = color
        self.square_centers = square_centers
        self.player_data = [color, activ_player]
        self.players = {color: Player(canvas, f"{color}", color, 10, len(colors), square_centers) for color in colors}
        # Place tokens in home
        for player in self.players.values():
            player.place_home_tokens(home_centers)
        self.players[color].recent_player = self.player_data
        self.turn_order = list(colors)
        self.current_player_index = None
        self.current_turn = 0
        self.next_turn = 0
        self.button = tk.Button(self.root, text="Roll Dice", command=self.roll, bg="darkblue", fg="white")
        self.canvas.create_window(20, 2, window=self.button, anchor="nw")
        self.switch_button = tk.Button(self.root, text="Switch", command=self.switch_player, bg="darkred", fg="white")
        self.canvas.create_window(160, 2, window=self.switch_button, anchor="nw")
        self.highlight_active_players()

    def switch_player(self):
        self.players[self.player_data[0]].switch_token()


    def roll(self):
        steps = self.dice.roll()
        color, token_name = self.player_data
        # self.players[color].recent_player = [color, token_name]
        self.player_data = [color, token_name]
        self.handle_roll(color, steps, token_name)
        self.highlight_active_players()
        self.switch_next_color()


    def highlight_active_players(self) :

        for token_name, token_id in self.players[self.active_color].tokens.items():
            if token_name.startswith(self.active_color) and self.next_turn == self.current_turn:
                self.canvas.itemconfig(token_id, fill="gold", outline="gold", width=3)
            else:
                self.canvas.itemconfig(token_id, fill=f"{self.active_color}", outline="black", width=3)
        self.players[self.active_color].show_active_player(3)


    def handle_roll(self, color, steps, token_name):
        if self.players[color].token_indices[token_name] == 0:
            if steps[0] == 6 or steps[1] == 6:
                start_coords = self.players[color].start_indices[color]
                self.players[color].enter_path(token_name, start_coords)
                return

        # self.players[color].move_steps(token_name, steps[0])

        for token_name in self.players[color].tokens:
            if token_name.startswith(color) and self.players[color].token_indices.get(token_name):
                self.players[color].move_steps(token_name, steps)
                break


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




'''
    def switch_token(self):
        # Rotate to next player
        color, active_player = self.player_data
        print(self.players[color].tokens)
        token_id = self.players[color].tokens[active_player]
        active_token_index = (token_id + 1) % len(self.players[color].tokens)
        print("Check: ", active_token_index)
        print(self.current_player_index)
        active_player = self.players[self.current_player_index]

        print(f"Switched to {active_player} player")
        self.players[color].show_active_player()



    def play_turn(self, color, token_name):
        steps = self.dice.roll()
        player = self.players[color]
        print(steps)
        # start_coords = player.start_indices[color]
        if self.players.token_indices[token_name] == 0:
            if steps[0] == 6 or steps[1] == 6:
                start_coords = self.players.start_indices[color]
                player.enter_path(token_name, start_coords)
            else:
                print(f"{token_name} cannot enter yet.")
        else:
            player.move_steps(token_name, steps)

        self.current_turn = (self.current_turn + 1) % len(self.turn_order)

    def next_turn(self):
        idx = self.players.index(self.active_player)
        self.active_player = self.players[(idx + 1) % len(self.players)]
        self.show_active
    '''