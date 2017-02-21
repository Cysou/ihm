import tkinter as tk
from const import *


class Gate:

    def __init__(self, grid):
        self.length_square = 10
        self.width = 1200
        self.height = 670
        self.matrice = []
        self.grid = grid
        self.cav = cav

    def creer_matrice(self):
        j = (self.height-40)//10
        while j > 0:
            self.matrice.append([0]*(self.width//10))
            j -= 1
        print(self.matrice)

    def release(self, event):
        gate_key = event.widget.find_withtag("current")[1]
        self.grid.check_placement(x, y, gate_key)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Grille")
    root.resizable(width="false", height="false")

    cav = tk.Canvas(root, width=grid_width, height=grid_height, bg="white")
    cav.pack()

    gate = Gate()

    c = cav.create_rectangle(100, 640, 150, 670, fill="red")
    cav.tag_bind(c, "<ButtonRelease-1>", gate.release)

    root.mainloop()
