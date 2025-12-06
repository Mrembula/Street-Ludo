import random
import tkinter as tk
from PIL import Image,  ImageTk


class Dice:
    def __init__(self, root, canvas, x=540, y=20):
        self.root = root
        self.canvas = canvas
        self.x = x
        self.y = y

        self.dice1_images = []
        for i in range(1, 7):
            img = Image.open(f"Project/assets/dice_one/dice-six-faces-{i}.png")
            img = img.resize((25, 27), Image.Resampling.LANCZOS)
            self.dice1_images.append(ImageTk.PhotoImage(img))

        self.dice2_images = []
        for i in range(1, 7):
            img = Image.open(f"Project/assets/dice_two/dice-six-faces-{i}.png")
            img = img.resize((30, 30), Image.Resampling.LANCZOS)
            self.dice2_images.append(ImageTk.PhotoImage(img))

        self.dice1_id = self.canvas.create_image(self.x + 85, self.y - 6, image=self.dice1_images[0], anchor="nw")
        self.dice2_id = self.canvas.create_image(self.x + 110, self.y - 7, image=self.dice2_images[0], anchor="nw")


    def roll(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        self.canvas.itemconfig(self.dice1_id, image=self.dice1_images[d1 - 1])
        self.canvas.itemconfig(self.dice2_id, image=self.dice2_images[d2 - 1])
        return d1, d2
