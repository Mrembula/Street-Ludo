import tkinter as tk
from typing import List
from player import Player
from dice import Dice
from board import Board
# Import the new path data


CELL = 40
GRID = 15
W = H = GRID * CELL

def make_square_centers(columns, rows, left, top, cell_w, cell_h):
    centers = []
    for row in range(rows):
        for column in range(columns):
            cx = left + column * cell_w // 2
            cy = top + row * cell_h + cell_h // 2
            centers.append((cx, cy))
    return centers



class Game:
    def __init__(self, root: tk.Tk, canvas: tk.Canvas, num_players: int):
        self.root = root
        self.canvas = canvas
        self.num_players = num_players
        self.current_player_index = 0
        self.last_roll_value = None

        # Start Game
        self.colors = ['red', 'green', 'blue', 'yellow']
        self.current_player_index = 0
        self.last_roll_value = None

        # 1. Initialize game
        self.board = Board(canvas)

        # 2. Initialize Component
        dice = Dice(root, canvas, x=20, y=10)
        # 3. Initialize Players
        self.players: List[Player] = self._initialize_players()

        # Start the game
        self.start_game()

    def _initialize_players(self) -> List[Player]:
        """Creates Player objects, attaches the main path, and places tokens in the home base."""
        players = []
        for i in range(self.num_players):
            color = self.colors[i]
            # Player needs to know its home stretch path
            home_path = self.board.get_home_stretch_paths(color, [])
            print("Home path for", home_path)

            # The player now needs the main path AND their home path
            p = Player(self.canvas, name=f"{color.capitalize()} Player", color=color,
                       main_path=self.main_path, home_path=home_path)

            # Place all 4 tokens in their respective home bases
            p.initialize_home_tokens()
            players.append(p)
        return players

    def start_game(self):
        # Optionally display who starts
        print(f"Game started! {self.players[self.current_player_index].name} starts.")

    def handle_roll(self):
        """Called when the Roll Dice button is clicked."""
        current_player = self.players[self.current_player_index]

        # 1. Roll the dice
        roll_value = self.dice.roll()
        self.last_roll_value = roll_value
        print(f"{current_player.name} rolled a {roll_value}.")

        # 2. Check for valid moves
        # (Placeholder - this is where the main game logic starts)
        valid_moves = self.find_valid_moves(current_player, roll_value)

        if valid_moves:
            print("Please select a token to move.")
            # Logic to enable token clicking and wait for selection goes here
        else:
            print("No valid moves. Passing turn.")
            self.next_turn()

    def find_valid_moves(self, player: Player, roll: int) -> List[int]:
        """Determine which tokens can be moved."""
        # TODO: Implement complex rules (getting out of home, kicking, reaching goal)
        return []  # Placeholder

    def move_token(self, token_id: int):
        """Handles the movement of a specific token after it has been selected."""
        # TODO: Implement token movement
        self.next_turn()

    def next_turn(self):
        """Advance to the next player's turn."""
        self.current_player_index = (self.current_player_index + 1) % self.num_players
        next_player = self.players[self.current_player_index]
        print(f"It is now {next_player.name}'s turn.")
        # Re-enable the Dice button if you disabled it after a roll
        # (You'll need to add a method to Dice to control its button state)








'''
class Game:
    def __init__(self, root: tk.Tk, canvas: tk.Canvas, num_players: int):
        self.root = root
        self.canvas = canvas
        self.num_players = num_players
        self.current_player_index = 0
        self.last_roll_value = None

        # Start Game
        self.colors =  ['red', 'green', 'blue', 'yellow']
        self.current_player_index = 0
        self.last_roll_value = None

        #1. Initialize game
        self.board = Board(canvas)

        #2. Initialize Component
        dice = Dice(root, canvas, x=20, y=10)

        self.players: list[Player] = self._initialize_players()

        def _initialize_players():
            players = []
            for i in range(self.num_players):
                color = self.color[i]
                home_path = self.home_scretch_path.get(color, [])

                p = Player(self.canvas, name=f"{color.capitalize()} Player", color=color,
                           main_path=self.main_path, home_path=home_path)
                p.initialize_home_tokens()
                players.append(p)
            print(players)
            return players


        def start_game(self):
            print(f"Game started! {self.players[self.current_player_index].name} starts.")

        def handle_roll(self):
            current_player = self.players[self.current_player_index]

            # 1. Roll the dice
            roll_value = self.dice.roll()
            self.last_roll_value = roll_value
            print(f"{current_player.name} rolled a {roll_value}.")
            valid_moves = self.find_valid_moves(current_player, roll_value)

            if valid_moves:
                print("Please select a token to move.")
            else:
                print("No valid moves. Passing turn.")
                self.next_turn()

        def find_valid_moves(self, player: Player, roll: int):
            return []  # Placeholder

        def move_token(self, token_id: int):
            # TODO: Implement token movement
            self.next_turn()

        def next_turn(self):
            self.current_player_index = (self.current_player_index + 1) % self.num_players
            next_player = self.players[self.current_player_index]
            print(f"It is now {next_player.name}'s turn.")
'''