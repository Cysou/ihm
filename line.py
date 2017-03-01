import tkinter as tk
from const import *
from grid import *


class Line:

    def __init__(self, cav, grid):
        self.cav = cav
        self.grid = grid
        self.base_ligne = []
        self.last_diff = 0
        self.max_delete = 0
        self.sens = 0

    def init_line(self, event):
        """ Fonction initialisant le traçage
        de la ligne lors du click souris. """
        x, y = self.grid.find_closest(event.x, event.y)
        self.base_ligne = [x, y]
        self.make_line(x, y, "")

    def init_delete(self, event):
        """ Fonction initialisant la suppression de la ligne. """
        x, y = self.grid.find_closest(event.x, event.y)
        self.delete_line(x, y)

    def make_line(self, x, y, tag):
        """ Fonction permettant de tracer une ligne. """
        x_coord = x // grid_squares
        y_coord = y // grid_squares
        if self.grid.detect_grid(x, y):
            if self.grid.matrice[y_coord][x_coord] == 0:
                self.grid.matrice[y_coord][x_coord] = 1
                i = -1
                id_square = self.cav.find_overlapping(x, y, x, y)[i]
                while self.cav.gettags(id_square)[0] != "square":
                    i -= 1
                    id_square = self.cav.find_overlapping(x, y, x, y)[i]
                self.cav.itemconfig(id_square, fill="black",
                                    tags=("square", tag))

    def delete_line(self, x, y):
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

    def draw_line(self, event):
        """ Fonction gérant le dessin de la ligne de façon dynamique. """
        x, y = self.grid.find_closest(event.x, event.y)
        x_diff = abs(self.base_ligne[0] - x)
        y_diff = abs(self.base_ligne[1] - y)
        if x_diff >= grid_squares and self.sens != 2:
            self.sens = 1
        elif y_diff >= grid_squares and self.sens != 1:
            self.sens = 2

        # Trace en x
        if self.sens == 1:
            y = self.base_ligne[1]
            if x_diff > self.last_diff:
                self.max_delete = x
                i = x
                while i > self.base_ligne[0]:
                    self.make_line(i, y, "right")
                    i -= grid_squares
                while i < self.base_ligne[0]:
                    self.make_line(i, y, "left")
                    i += grid_squares
            elif x_diff < self.last_diff:
                if x >= self.base_ligne[0]:
                    i = x + grid_squares
                    while i <= self.max_delete:
                        self.delete_line(i, y)
                        i += grid_squares
                elif x <= self.base_ligne[0]:
                    i = x - grid_squares
                    while i >= self.max_delete:
                        self.delete_line(i, y)
                        i -= grid_squares
                    if x == (self.base_ligne[0] - grid_squares):
                        self.delete_line(x, y)
            self.last_diff = abs(self.base_ligne[0] - x)

        # Trace en y
        elif self.sens == 2:
            x = self.base_ligne[0]
            if y_diff > self.last_diff:
                self.max_delete = y
                i = y
                while i > self.base_ligne[1]:
                    self.make_line(x, i, "up")
                    i -= grid_squares
                while i < self.base_ligne[1]:
                    self.make_line(x, i, "down")
                    i += grid_squares
            elif y_diff < self.last_diff:
                if y >= self.base_ligne[1]:
                    i = y + grid_squares
                    while i <= self.max_delete:
                        self.delete_line(x, i)
                        i += grid_squares
                elif y <= self.base_ligne[1]:
                    i = y - grid_squares
                    while i >= self.max_delete:
                        self.delete_line(x, i)
                        i -= grid_squares
                    if y == (self.base_ligne[1] - grid_squares):
                        self.delete_line(x, y)
            self.last_diff = abs(self.base_ligne[1] - y)

    def end_line(self, event):
        """ Fonction réinitialisant les variables
        après avoir fini de tracer une ligne. """
        self.base_ligne = []
        self.last_diff = 0
        self.max_delete = 0
        self.sens = 0
