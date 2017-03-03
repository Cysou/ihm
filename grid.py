import tkinter as tk
from const import *
from gates import *
from wire import *
from robot import *


class Grid:

    def __init__(self, cav, gate, wire, robot):
        self.matrice = []
        self.create_matrice()
        self.cav = cav
        self.gate = gate
        self.wire = wire
        self.robot = robot

    def create_matrice(self):
        """ Fonction créant la matrice associée à la grille. """
        j = grid_height // grid_squares
        while j > 0:
            self.matrice.append([0]*(grid_width // grid_squares))
            j -= 1

    def create(self):
        """ Fonction créant la grille. """
        x1 = 0
        y1 = 0
        x2 = grid_squares
        y2 = grid_squares
        while (y2 <= grid_height):
            if y1 % 110 == 0 and y1 != 0 and x1 == 0:
                self.cav.create_rectangle(x1, y1, x2, y2,
                                          outline="grey60",
                                          fill="grey60",
                                          tags="capteur")
                self.matrice[y1 // grid_squares][x1 // grid_squares] = "cpt"
            elif y1 % 110 == 0 and y1 != 0 and x2 == grid_width:
                self.cav.create_rectangle(x1, y1, x2, y2,
                                          outline="grey60",
                                          fill="deeppink",
                                          tags="moteur")
                self.matrice[y1 // grid_squares][x1 // grid_squares] = "mt"
            else:
                self.cav.create_rectangle(x1, y1, x2, y2,
                                          outline="grey60",
                                          fill="white",
                                          tags="square")
            if x2 >= grid_width:
                x1 = 0
                y1 += grid_squares
                x2 = grid_squares
                y2 += grid_squares
            else:
                x1 += grid_squares
                x2 += grid_squares
        self.cav.tag_bind("square", "<Button-1>", self.wire.init_wire)
        self.cav.tag_bind("square", "<B1-Motion>", self.wire.draw_wire)
        self.cav.tag_bind("square", "<ButtonRelease-1>", self.wire.end_wire)
        self.cav.tag_bind("square", "<Button-3>", self.wire.init_delete)
        self.cav.tag_bind("square", "<B3-Motion>", self.wire.init_delete)

    def placement(self, x, y, gate_key, sens):
        """ Fonction permettant de placer la porte sur la grille. """
        color = dico_gates[gate_key][3]
        if int(sens) % 2 != 0:
            lengthx = dico_gates[gate_key][0]//2
            lengthy = dico_gates[gate_key][1]//2
            id_gate = self.cav.create_rectangle(x - lengthx * grid_squares,
                                                y - lengthy * grid_squares,
                                                x + (lengthx + 1)*grid_squares,
                                                y + (lengthy + 1)*grid_squares,
                                                fill=color,
                                                tags=(gate_key, sens))
        else:
            lengthx = dico_gates[gate_key][1]//2
            lengthy = dico_gates[gate_key][0]//2
            id_gate = self.cav.create_rectangle(x - lengthx * grid_squares,
                                                y - lengthy * grid_squares,
                                                x + (lengthx + 1)*grid_squares,
                                                y + (lengthy + 1)*grid_squares,
                                                fill=color,
                                                tags=(gate_key, sens))
        cav.tag_bind(id_gate, "<Button-3>",
                     lambda event: self.gate.rotate(event, id_gate))
        cav.tag_bind(id_gate, "<Control-Button-3>",
                     lambda event: self.gate.delete_gate(event, id_gate))
        self.fill_matrice(x, y, lengthx, lengthy,
                          dico_gates[gate_key][2], sens)

    def find_closest(self, x, y):
        """ Fonction permettant de trouver les coordonnées du point
        haut/gauche du carré dans lequel on a relaché le click gauche.
        (Ce carré sera le centre de la porte) """
        i = 0
        while i <= x - grid_squares:
            i += grid_squares
        j = 0
        while j <= y - grid_squares:
            j += grid_squares
        return i, j

    def fill_matrice(self, x, y, lengthx, lengthy, gate_name, sens):
        """ Fonction remplissant la matrice associée à la grille
        lorsqu'une porte est placée. """
        i = -lengthx
        x_matrice = x // grid_squares
        y_matrice = y // grid_squares
        while i <= lengthx:
            j = -lengthy
            while j <= lengthy:
                self.matrice[y_matrice + j][x_matrice + i] = gate_name
                j += 1
            i += 1
        if int(sens) % 4 == 0:
            self.matrice[y_matrice - lengthy][x_matrice - lengthx] = "enter0"
            self.matrice[y_matrice - lengthy][x_matrice + lengthx] = "enter0"
            self.matrice[y_matrice + lengthy][x_matrice] = "exit0"
            self.gate.enter_exit(x_matrice - lengthx, y_matrice - lengthy)
            self.gate.enter_exit(x_matrice + lengthx, y_matrice - lengthy)
            self.gate.enter_exit(x_matrice, y_matrice + lengthy)
        elif int(sens) % 2 == 0:
            self.matrice[y_matrice + lengthy][x_matrice - lengthx] = "enter0"
            self.matrice[y_matrice + lengthy][x_matrice + lengthx] = "enter0"
            self.matrice[y_matrice - lengthy][x_matrice] = "exit0"
            self.gate.enter_exit(x_matrice - lengthx, y_matrice + lengthy)
            self.gate.enter_exit(x_matrice + lengthx, y_matrice + lengthy)
            self.gate.enter_exit(x_matrice, y_matrice - lengthy)
        elif int(sens) % 3 == 0:
            self.matrice[y_matrice - lengthy][x_matrice + lengthx] = "enter0"
            self.matrice[y_matrice + lengthy][x_matrice + lengthx] = "enter0"
            self.matrice[y_matrice][x_matrice - lengthx] = "exit0"
            self.gate.enter_exit(x_matrice + lengthx, y_matrice - lengthy)
            self.gate.enter_exit(x_matrice + lengthx, y_matrice + lengthy)
            self.gate.enter_exit(x_matrice - lengthx, y_matrice)
        else:
            self.matrice[y_matrice - lengthy][x_matrice - lengthx] = "enter0"
            self.matrice[y_matrice + lengthy][x_matrice - lengthx] = "enter0"
            self.matrice[y_matrice][x_matrice + lengthx] = "exit0"
            self.gate.enter_exit(x_matrice - lengthx, y_matrice - lengthy)
            self.gate.enter_exit(x_matrice - lengthx, y_matrice + lengthy)
            self.gate.enter_exit(x_matrice + lengthx, y_matrice)
        print(self.matrice)

    def check_placement(self, x, y, gate_key, sens):
        """ Fonction vérifiant si le placement de la porte est valide. """
        if self.detect_grid(x, y):
            x, y = self.find_closest(x, y)
            x, y = self.check_overlapping(x, y, gate_key, sens)
            if self.place_is_free(x, y, gate_key, sens):
                self.placement(x, y, gate_key, sens)
                return True
        return False

    def check_overlapping(self, x, y, gate_key, sens):
        """ Fonction replaçant correctement la porte si celle-ci
        a été placée aux extrémités de la grille et qu'elle dépasse. """
        if int(sens) % 2 != 0:
            x_gate = grid_squares * (dico_gates[gate_key][0]//2)
            y_gate = grid_squares * (dico_gates[gate_key][1]//2)
        else:
            x_gate = grid_squares * (dico_gates[gate_key][1]//2)
            y_gate = grid_squares * (dico_gates[gate_key][0]//2)
        limx = grid_width - (grid_squares + x_gate)
        limy = grid_height - (grid_squares + y_gate)
        new_x = x
        new_y = y
        if x < x_gate:
            new_x = x_gate
        elif x > limx:
            new_x = limx

        if y < y_gate:
            new_y = y_gate
        elif y > limy:
            new_y = limy

        return (new_x, new_y)

    def place_is_free(self, x, y, gate_key, sens):
        """ Fonction indiquant si les cases, où la porte
        va être placée, sont prises. """
        if int(sens) % 2 != 0:
            lengthx = dico_gates[gate_key][0]//2
            lengthy = dico_gates[gate_key][1]//2
        else:
            lengthx = dico_gates[gate_key][1]//2
            lengthy = dico_gates[gate_key][0]//2
        x_matrice = x // grid_squares
        y_matrice = y // grid_squares
        i = -lengthx
        while i <= lengthx:
            j = -lengthy
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
        return (x1 <= x < x2) and (y1 <= y < y2)

    def detect_grid_ij(self, i, j):
        """ Fonction permettant de savoir si i, j
        dans la matrice ou pas. """
        x1 = 0
        y1 = 0
        x2 = len(self.matrice[0])
        y2 = len(self.matrice)
        return (x1 <= i < x2) and (y1 <= j < y2)

    def delete_matrice(self, id_gate):
        """ Fonction supprimant la porte dans la matrice. """
        coord = self.cav.coords(id_gate)
        i = int(coord[0])
        while i < coord[2]:
            j = int(coord[1])
            while j < coord[3]:
                self.matrice[j//grid_squares][i//grid_squares] = 0
                j += grid_squares
            i += grid_squares


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Grille")
    root.resizable(width="false", height="false")

    cav = tk.Canvas(root, width=grid_width, height=height, bg="white")
    cav.pack()

    grid = Grid(cav, None, None, None)

    gate = Gate(cav, grid)
    wire = Wire(cav, grid)
    robot = Robot(cav, grid)
    grid.gate = gate
    grid.wire = wire
    grid.robot = robot
    grid.create()

    c1 = cav.create_rectangle(100, 640, 150, 670, fill="red",
                              tags=("gate_and", "1"))
    c2 = cav.create_rectangle(170, 640, 220, 670, fill="blue",
                              tags=("gate_or", "1"))
    c3 = cav.create_rectangle(240, 640, 290, 670, fill="seagreen",
                              tags=("gate_xor", "1"))
    c4 = cav.create_rectangle(310, 640, 360, 670, fill="purple",
                              tags=("gate_not", "1"))
    cav.tag_bind(c1, "<ButtonRelease-1>", gate.release)
    cav.tag_bind(c2, "<ButtonRelease-1>", gate.release)
    cav.tag_bind(c3, "<ButtonRelease-1>", gate.release)
    cav.tag_bind(c4, "<ButtonRelease-1>", gate.release)

    root.mainloop()
