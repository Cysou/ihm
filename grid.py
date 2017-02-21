import tkinter as tk
from const import *


class Grid:

    def __init__(self, cav):
        self.matrice = []
        self.create_matrice()
        self.cav = cav

    def create_matrice(self):
        """ Fonction créant la matrice associée à la grille. """
        j = grid_height//grid_squares
        while j > 0:
            self.matrice.append([0]*(grid_width//grid_squares))
            j -= 1

    def create(self):
        """ Fonction créant la grille. """
        x1 = 0
        y1 = 0
        x2 = grid_squares
        y2 = grid_squares
        while (y2 <= grid_height):
            self.cav.create_rectangle(x1, y1, x2, y2, outline="grey60",
                                      tags="square")
            if x2 >= grid_width:
                x1 = 0
                y1 += grid_squares
                x2 = grid_squares
                y2 += grid_squares
            else:
                x1 += grid_squares
                x2 += grid_squares

    def placement(self, x, y, gate):
        """ Fonction permettant de placer la porte sur la grille. """
        lengthx = dico_gates[gate][0]//2
        lengthy = dico_gates[gate][1]//2
        self.cav.create_rectangle(x - lengthx * grid_squares,
                                  y - lengthy * grid_squares,
                                  x + lengthx * grid_squares,
                                  y + (lengthy + 1) * grid_squares,
                                  fill="gate")
        self.fill_matrice(x, y, lengthx, lengthy, gate[2])

    def find_closest(self, x, y):
        """ Fonction permettant de trouver les coordonnées du point haut/gauche
        du carré dans lequel on a relaché le click gauche.
        (Ce carré sera le centre de la porte) """
        i = 0
        while i <= x - grid_squares:
            i += grid_squares
        j = 0
        while j <= y - grid_squares:
            j += grid_squares
        return i, j

    def fill_matrice(self, x, y, lengthx, lengthy, gate_name):
        """ Fonction remplissant la matrice associée à la grille
        lorsqu'une porte est placée. """
        i = -lengthx
        j = -lengthy
        x_matrice = x // grid_squares
        y_matrice = y // grid_squares
        while i <= lengthx:
            while j <= lengthy:
                self.matrice[y_matrice + j][x_matrice + i] = gate_name
                j += 1
            i += 1

    def check_placement(self, x, y, gate_key):
        """ Fonction vérifiant si le placement de la porte est valide. """
        if self.detect_grid(x, y):
            x, y = self.find_closest(x, y)
            x, y = self.check_overlapping(x, y, gate_key)
            if place_is_free(x, y, gate_key):
                placement(x, y, gate_key)

    def check_overlapping(self, x, y, gate_key):
        """ Fonction replaçant correctement la porte si celle-ci
        a été placée aux extrémités de la grille et qu'elle dépasse. """
        x_gate = grid_squares * (dico_gates[gate_key][0]//2)
        y_gate = grid_squares * (dico_gates[gate_key][1]//2)
        new_x = x
        new_y = y
        if x < x_gate:
            new_x = x_gate
        elif x == (grid_width - (grid_squares + x_gate)):
            new_x -= x_gate

        if y == 0:
            new_y = y_gate
        elif y == (grid_height - (grid_squares + y_gate)):
            new_y -= y_gate

        return (new_x, new_y)

    def place_is_free(self, x, y, gate_key):
        """ Fonction indiquant si les cases, où la porte
        va être placée, sont prises. """
        x_matrice = x // grid_squares
        y_matrice = y // grid_squares
        lengthx = dico_gates[gate_key][0]//2
        lengthy = dico_gates[gate_key][1]//2
        i = -lengthx
        j = -lengthy
        while i <= lengthx:
            while j <= lengthy:
                if self.matrice[y_matrice + j][x_matrice + i] != 0:
                    return False
                j += 1
            i += 1
        return True

    def detect_grid(self, x, y):
        """ Fonction permettant de savoir si on place bien
        la porte dans la grille ou pas. """
        x1 = 0
        y1 = 0
        x2 = grid_width
        y2 = grid_height
        return (x1 < x < x2) and (y1 < y < y2)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Grille")
    root.resizable(width="false", height="false")

    cav = tk.Canvas(root, width=grid_width, height=grid_height, bg="white")
    cav.pack()

    grid = Grid(cav)
    grid.create()

    root.mainloop()
