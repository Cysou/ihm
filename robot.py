import tkinter as tk
from const import *
from grid import *


class Robot:

    def __init__(self, cav, grid):
        self.cav = cav
        self.grid = grid

    def detect_gates(self):
        x = grid_width // grid_squares
        y = 0
        while y < (grid_height // grid_squares):
            if self.grid.matrice[y][x] == "mt":
                self.check_wire(x, y)
                pass

    def check_wire(self, x, y):
        pass
