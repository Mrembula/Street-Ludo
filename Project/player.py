import tkinter as tk
from tkinter import simpledialog
from typing import List, Tuple, Optional
from PIL import Image, ImageTk

class Player:
    def __init__(self, canvas: tk.Canvas, name, color="red", radius=10, num_players=0):
        self.canvas = canvas
        self.name = name
        self.color = color
        self.radius = radius
        self.token_image = None
        self.token_id = None
        self.label_id = None
        self.all_player = {}
        self.total_slots = num_players

        # board-related
        self.square_centers: Optional[List[Tuple[int, int]]] = None
        self.current_index: Optional[int] = None

    def attach_board(self, centers: List[Tuple[int, int]]):
        self.square_centers = centers

    # Positioning players as the start
    def _compute_offset(self, slot):# -> Tuple[int, int]:
        oy1 = 93
        oy2 = 297
        spacing = self.radius * 2 + 4
        start = (spacing * 3) / 2
        ox = int(start + slot * spacing) + 70
        if self.color == "red":
            return (ox + 15, oy1) # 190
        elif self.color == "green":
            return (ox + 190, oy1) # 340
        elif self.color == "blue":
            return (ox + 165, oy2) # 364
        elif self.color == "yellow":
            return (ox - 60, oy2)
        else:
            return (0, 0)

    def place_on_square(self, index, slot=0, color=None):
        cell = 20;
        for i in range(1, 5):
            if self.square_centers is None:
                raise RuntimeError("Board centers not attached. Call attach_board(...) first.")
            if not (0 <= index < len(self.square_centers)):
                raise IndexError("Square index out of range.")
            self.current_index = index
            cx, cy = self.square_centers[index]
            ox, oy = self._compute_offset(slot)
            x = (cx + (cell * i)) + (ox + (cell * i)) if i <= 2 else (cx + (cell * i - cell) + ox)
            y = (cy + i) + (oy + i) if i <= 2 else (cy + i) + (oy + (cell * i - cell))
            if i == 4: x += 18; y -= 20
            self.token_id = self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, fill=self.color, outline="black", width=3)
            self.all_player[f"{color}-{i}"] = [x , y]

    def move_steps(self, steps, board_size: int, slot=0, total_slots=1, wrap=True):
        if self.current_index is None:
            self.current_index = 0
        new_index = self.current_index + steps
        if wrap:
            new_index %= board_size
        else:
            new_index = min(new_index, board_size - 1)
        self.place_on_square(new_index, slot=slot)
        return new_index

    def create_token_at(self, x, y):
        if self.token_id:
            coords = self.canvas.coords(self.token_id)
            print("coords: ", coords)
            if coords:
                if len(coords) == 2:
                    self.canvas.coords(self.token_id, x, y)
                else:
                    self.canvas.coords(self.token_id, x - self.radius, y - self.radius, x + self.radius, y + self.radius)
            else:
                self.canvas.delete(self.token_id)
                self.token_id = None
        if self.label_id:
            print(2)
            self.canvas.coords(self.label_id, x, y + self.radius + 8)

        if not self.token_id:
            print(3)
            self.token_id = self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, fill=self.color, outline="black", width=3)

    def leave_board(self):
        if self.token_id:
            self.canvas.delete(self.token_id)
            self.token_id = None
        if self.label_id:
            self.canvas.delete(self.label_id)
            self.label_id = None
        self.current_index = None

'''
    @classmethod
    def create_players_from_dialog(cls, canvas: tk.Canvas, board_centers: List[Tuple[int, int]], default_colors: Optional[List[str]] = None, radius: int = 12, start_index: int = 0) -> List["Player"]:
        """Show popup to ask number of players, create and place them on the board."""
        parent = canvas.winfo_toplevel()
        num = simpledialog.askinteger("Players", "Enter number of players (1-8):", parent=parent, minvalue=1, maxvalue=8, initialvalue=4)
        if not num:
            return []

        palette = default_colors or ["red", "blue", "green", "yellow", "orange", "purple", "cyan", "magenta"]
        players: List[Player] = []
        for i in range(num):
            color = palette[i % len(palette)]
            p = cls(canvas, name=f"P{i+1}", color=color, radius=radius)
            p.attach_board(board_centers)
            p.place_on_square(start_index, slot=i, total_slots=num)
            players.append(p)
        return players
        
        
    
        #if self.token_image:
        #   self.token_id = self.canvas.create_image(x, y, image=self.token_image, anchor="center")
        #else:
        #   self.label_id = self.canvas.create_text(x, y + self.radius + 8, text=self.name[0].upper(), fill="white", font=("TkDefaultFont", 8))

'''