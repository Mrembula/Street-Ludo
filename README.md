Street Ludo
Video Demo: "https://youtu.be/PypDqb7D_7Q"


Description:
Street Ludo is a graphical, turn-based multiplayer board game built using Python and the Tkinter library.
It brings the classic Ludo experience to the desktop with a custom "Street" aesthetic.
The game supports 2 to 4 players, featuring automated movement animations, token kicking logic, stacking mechanics, and a dynamic win-detection system.
The project was designed to demonstrate object-oriented programming (OOP) principles, handling complex game states, and managing real-time GUI updates in Python.

Features
Dynamic Player Count: At the start of the game, players can choose between 2 and 4 participants via a dialog box.
Double Dice System: Unlike traditional Ludo, this version uses two dice, allowing for more strategic movement and "doubles" bonuses.
Animated Movement: Tokens move cell-by-cell with a configurable delay, providing a smooth visual experience.
Kicking & Stacking: If a player lands on an opponent, the opponent's token is sent back to the base. If they land on their own token, they form a "stack" that moves together.
Active Highlighting: The game uses a "Gold" highlight system to clearly show which player is currently active and which token is selected for movement.

Project Structure
project.py
This is the main entry point of the application. It contains the main() function which initializes the Tkinter root, handles the initial player count selection, and sets up the Game environment.
It also contains the core helper functions required for the project's logic, such as coordinate conversion and base position mapping.

game.py
The "brain" of the project. This file contains the Game class, which manages the turn order, dice roll results, and the rules of Ludo.
It coordinates between the dice, the board, and the players. Key methods include:
    check_win_condition: Monitors if a player has successfully moved all tokens to the center.
    switch_next_color: Handles the transition between players and resets visual states.
    check_for_kick: Implements the "capturing" logic when tokens overlap.

player.py
Defines the Player class. Each player object maintains the state of its four tokens (names, positions, and whether they are "home").
It also handles the step_animation logic, which recursively moves tokens across the canvas.

board.py
Responsible for the visual layout. It uses Tkinter's Canvas to draw the 15x15 grid, the home bases, and the colored paths.
It calculates the pixel coordinates for every cell on the board so that tokens can be placed accurately.

dice.py
A utility class that manages the dice images and the randomization logic. It handles the visual update of the dice faces on the screen.

test_project.py
Contains the unit tests for the functions defined in project.py. It uses the pytest framework to ensure that coordinate calculations and grid mappings are mathematically accurate.

How to Run
Install Dependencies: Please do review the requirements.txt file for necessary libraries. Primarily, you will need Python 3.x and Tkinter.:
Execute the Game: project.py

python project.py
Play: Enter the number of players, roll the dice, and use the "Switch" button to select different tokens if you have multiple pieces on the board.

Design Choices
One of the biggest challenges was managing the turn-based logic when a player wins. Originally, removing a player from a list while iterating caused index errors.
I solved this by implementing a force_turn_switch method that recalculates the turn_order list and manually jumps the index to the next valid player color.
Another major choice was the "Gold" highlighting system, which was implemented to solve user confusion regarding which piece would move when the "Move" button was clicked.
