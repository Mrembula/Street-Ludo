import tkinter as tk
import random
from PIL import Image,  ImageTk


class Dice:
    def __init__(self, root):
        self.dice1_image = []
        for i in range(1, 7):
            dice = Image.open(f"Project/assets/dice_one/dice-six-faces-{i}.png")
            dice = dice.resize((25, 27), Image.Resampling.LANCZOS)
            self.dice1_image.append(ImageTk.PhotoImage(dice))

        self.dice2_image = []
        for i in range(1, 7):
            dice = Image.open(f"Project/assets/dice_two/dice-six-faces-{i}.png")
            dice = dice.resize((30, 30), Image.Resampling.LANCZOS)
            self.dice2_image.append(ImageTk.PhotoImage(dice))

        self.canvas = tk.Canvas(root, width=75, height=40, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(side="right")

        self.dice1 = self.canvas.create_image(25, 20, image=self.dice1_image[0])
        self.dice2 = self.canvas.create_image(54, 20, image=self.dice2_image[0])

        self.button = tk.Button(root, text="Roll Dice", command=self.roll, bg="darkblue", fg="white",)
        self.button.pack(side="right", padx=5)


    def roll(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)

        self.canvas.itemconfig(self.dice1, image=self.dice1_image[d1 -1])
        self.canvas.itemconfig(self.dice2, image=self.dice2_image[d2 - 1])

        return d1, d2
