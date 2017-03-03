import tkinter as tk
from PIL import Image, ImageTk
from const import *
from grid import *

# Mettre tags pour wires (point, triple_n|s|e|w, simple_n|s|e|w, double_h|v
# corner_nw|ne|se|sw, quad, bridge_h|v)

class Wire:

    def __init__(self, cav, grid):
        self.cav = cav
        self.grid = grid
        self.idd_actual = []
        self.first = None
        self.second = None
        self.direction = None
        self.img = {}
        self.load_img()

    def load_img(self):
        for name in ("vertical", "horizontal", "double"):
            path = "wire/img/wire_" + name + ".png"
            pilimg = Image.open(path)
            tkimg = ImageTk.PhotoImage(pilimg)
            self.img[name] = tkimg

    # Create
    def init_wire(self, event):
        """ Fonction initialisant le traçage
        de la ligne lors du click souris. """
        x, y = self.grid.find_closest(event.x, event.y)
        self.first = [x, y]
        self.second = [x, y]

    def make_wire(self, x, y, direction):
        """ Fonction permettant de tracer une ligne. """
        if self.grid.detect_grid(x, y):
            i = y // grid_squares
            j = x // grid_squares
            if self.grid.matrice[i][j] == 0:
                self.grid.matrice[i][j] = "wire"
                self.idd_actual.append(self.cav.create_image(x + (grid_squares//2), y + (grid_squares//2), image=self.img[direction]))

    def multiple_make_wire(self, x, y):
        """ Fonction permettant de tracer une ligne. """
        if self.direction == "vertical":
            y0 = self.first[1]
            y0, y = self.ascend(y0, y)
            while y0 <= y:
                self.make_wire(self.first[0], y0, "vertical")
                y0 += grid_squares
        elif self.direction == "horizontal":
            x0 = self.first[0]
            x0, x = self.ascend(x0, x)
            while x0 <= x:
                self.make_wire(x0, self.first[1], "horizontal")
                x0 += grid_squares
        else:
            print("ERREUR")

    def ascend(self, a, b):
        if a < b:
            return a, b
        else:
            return b, a

    def draw_wire(self, event):
        """ Fonction gérant le dessin de la ligne de façon dynamique. """
        x, y = self.grid.find_closest(event.x, event.y)
        if x != self.first[0] or y != self.first[1]:
            if x != self.second[0] or y != self.second[1]:
                self.delete_actual()
                self.update_direction(x, y)
                self.second = [x, y]
                self.multiple_make_wire(x, y)
        else:
            self.direction = None
            self.delete_actual()
            self.make_wire(x, y, "double")

    def update_direction(self, x, y):
        if abs(self.first[0] - x) < abs(self.first[1] - y):
            self.direction = "vertical"
        else:
            self.direction = "horizontal"

    def end_wire(self, event):
        self.idd_actual = []
        self.first = None
        self.second = None
        self.direction = None

    def delete_actual(self):
        if self.direction == "vertical":
            b = self.first[1] // grid_squares
            c = self.second[1] // grid_squares
            b, c = self.ascend(b, c)
            d = self.first[0] // grid_squares
            for a in range(b, c+1):
                if self.grid.detect_grid_ij(d, a):
                    if self.grid.matrice[a][d][:4] == "wire":
                        self.grid.matrice[a][d] = 0
        elif self.direction == "horizontal":
            b = self.first[0] // grid_squares
            c = self.second[0] // grid_squares
            b, c = self.ascend(b, c)
            d = self.first[1] // grid_squares
            for a in range(b, c+1):
                if self.grid.detect_grid_ij(a, d):
                    if self.grid.matrice[d][a][:4] == "wire":
                        self.grid.matrice[d][a] = 0
        else:
            i = self.first[1] // grid_squares
            j = self.first[0] // grid_squares
            self.grid.matrice[i][j] = 0

        for idd in self.idd_actual:
            self.cav.delete(idd)

    # Delete
    def init_delete(self, event):
        """ Fonction initialisant la suppression de la ligne. """
        x, y = self.grid.find_closest(event.x, event.y)
        self.delete_wire(x, y)

    def delete_wire(self, x, y):
        """ Fonction permettant de supprimer une ligne. """
        x_coord = x // grid_squares
        y_coord = y // grid_squares
        if self.grid.detect_grid(x, y):
            if self.grid.matrice[y_coord][x_coord] == 1:
                self.grid.matrice[y_coord][x_coord] = 0
                i = -1
                id_square = self.cav.find_overlapping(x, y, x, y)[i]
                while self.cav.gettags(id_square)[0] != "square":
                    i -= 1
                    id_square = self.cav.find_overlapping(x, y, x, y)[i]
                self.cav.itemconfig(id_square, fill="white", tags="square")
