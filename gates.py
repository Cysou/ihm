import tkinter as tk
from circuit import *
from const import *


class Gate:

    def __init__(self, cav, circuit):
        self.cav = cav
        self.circuit = circuit
        self.circuit.gates = self
        self.coord_move = []

    def create(self):
        """ Fonction initialisant la création des portes. """
        self.cav.create_rectangle(width - gates_window_width,
                                  height - gates_window_height, width, height,
                                  fill="grey50")
        gate_a = self.cav.create_rectangle(1075, 280, 1125, 310, fill="red",
                                           tags=("gate_and", 1))
        gate_o = self.cav.create_rectangle(1075, 360, 1125, 390, fill="blue",
                                           tags=("gate_or", 1))
        gate_xo = self.cav.create_rectangle(1075, 440, 1125, 470,
                                            fill="seagreen",
                                            tags=("gate_xor", 1))
        gate_n = self.cav.create_rectangle(1075, 520, 1125, 550,
                                           fill="purple",
                                           tags=("gate_not", 1))
        self.cav.tag_bind(gate_a, "<ButtonRelease-1>", self.release)
        self.cav.tag_bind(gate_o, "<ButtonRelease-1>", self.release)
        self.cav.tag_bind(gate_xo, "<ButtonRelease-1>", self.release)
        self.cav.tag_bind(gate_n, "<ButtonRelease-1>", self.release)

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
        x = (coord[0] + coord[2]) // 2
        y = (coord[1] + coord[3]) // 2
        self.delete_gate(event, id_gate)
        if not self.circuit.check_placement(x, y, tag[0], sens):
            self.circuit.placement(x, y, tag[0], tag[1])

    def delete_gate(self, event, id_gate):
        """ Fonction supprimant une porte. """
        self.cav.delete(id_gate)

    def init_move_gate(self, event, gate_id, sens):
        """ Fonction initialisant le déplacement d'une porte en
        plaçant le curseur au centre de celle-ci. """
        self.coord_move.append(event.x - self.cav.coords(gate_id)[0])
        self.coord_move.append(event.y - self.cav.coords(gate_id)[1])
        self.cav.lift(gate_id)

    def move_gate(self, event, gate_id, sens):
        """ Fonction permettant le déplacement de la porte et des fils. """
        gate_key = self.cav.gettags(gate_id)[0]
        if (int(sens) % 2 != 0):
            lengthx = dico_gates[gate_key][0]
            lengthy = dico_gates[gate_key][1]
        else:
            lengthx = dico_gates[gate_key][1]
            lengthy = dico_gates[gate_key][0]
        x1 = event.x - self.coord_move[0]
        y1 = event.y - self.coord_move[1]
        x2 = x1 + lengthx
        y2 = y1 + lengthy

        if (x1 < x1_circuit):
            x1 = x1_circuit
            x2 = x1 + lengthx
        elif (x2 > x2_circuit):
            x2 = x2_circuit
            x1 = x2 - lengthx

        if (y1 < y1_circuit):
            y1 = y1_circuit
            y2 = y1 + lengthy
        elif (y2 > y2_circuit):
            y2 = y2_circuit
            y1 = y2 - lengthy
        self.cav.coords(gate_id, x1, y1, x1 + lengthx, y1 + lengthy)

    def end_move_gate(self):
        """ Fonction finalisant le déplacement de la porte
        et changeant la structure de données. """
        self.coord_move = []
        self.circuit.fill_structure()
