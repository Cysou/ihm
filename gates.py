import tkinter as tk
from circuit import *
from const import *


class Gate:

    def __init__(self, cav, circuit):
        self.cav = cav
        self.circuit = circuit
        self.circuit.gates = self

    def create(self):
        """ Fonction initialisant la création des portes. """
        self.cav.create_rectangle(width - gates_window_width,
                                  height - gates_window_height, width, height,
                                  fill="grey50")
        gate_a = self.cav.create_rectangle(1075, 250, 1125, 280, fill="red",
                                           tags=("gate_and", 1))
        self.cav.tag_bind(gate_a, "<ButtonRelease-1>", self.release)

    def release(self, event):
        """ Fonction initialisant le placement de la porte lorsque l'on
        relache le click gauche de la souris. """
        gate_key = self.cav.gettags("current")[0]
        sens = self.cav.gettags("current")[1]
        x = event.x
        y = event.y
        self.circuit.check_placement(x, y, gate_key, sens)

    def rotate(self, event, id_gate):
        """ Foncion permettant de faire tourner une porte à 90°. """
        coord = self.cav.coords(id_gate)
        tag = self.cav.gettags("current")
        sens = int(tag[1]) + 1
        if sens == 5:
            sens = 1
        x = (coord[0] + coord[2]) // 2
        y = (coord[1] + coord[3]) // 2
        self.delete_gate(event, id_gate)
        if not self.grid.check_placement(x, y, tag[0], sens):
            x, y = self.grid.find_closest(x, y)
            self.grid.placement(x, y, tag[0], tag[1])

    def delete_gate(self, event, id_gate):
        """ Fonction supprimant une porte. """
        self.grid.delete_matrice(id_gate)
        self.delete_ee(id_gate)
        self.cav.delete(id_gate)

    def move(self, event, id_gate, sens):
        gate_key = self.cav.gettags(id_gate)[0]
        if int(sens) % 2 != 0:
            newx = event.x - (grid_squares * dico_gates[gate_key][0] // 2)
            newy = event.y - (grid_squares * dico_gates[gate_key][1] // 2)
            self.cav.coords(id_gate, newx, newy,
                            newx + grid_squares * dico_gates[gate_key][0],
                            newy + grid_squares * dico_gates[gate_key][1])
        else:
            newx = event.x - (grid_squares * dico_gates[gate_key][1] // 2)
            newy = event.y - (grid_squares * dico_gates[gate_key][0] // 2)
            self.cav.coords(id_gate, newx, newy,
                            newx + grid_squares * dico_gates[gate_key][1],
                            newy + grid_squares * dico_gates[gate_key][0])
        self.delete_ee(id_gate)

    def enter_exit(self, x, y):
        """ Fonction plaçant les entrées et la sortie de la porte. """
        x1 = x * grid_squares
        y1 = y * grid_squares
        x2 = x1 + grid_squares
        y2 = y1 + grid_squares
        self.cav.create_rectangle(x1, y1, x2, y2, fill="yellow", tags="ee")

    def delete_ee(self, id_gate):
        self.cav.delete(self.cav.find_above(id_gate))
        self.cav.delete(self.cav.find_above(id_gate))
        self.cav.delete(self.cav.find_above(id_gate))
