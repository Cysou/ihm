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
        gate_a = self.cav.create_rectangle(1075, 250, 1125, 280, fill="red",
                                           tags=("gate_and", 1))
        gate_o = self.cav.create_rectangle(1075, 330, 1125, 360, fill="blue",
                                           tags=("gate_or", 1))
        gate_xo = self.cav.create_rectangle(1075, 410, 1125, 440,
                                            fill="seagreen",
                                            tags=("gate_xor", 1))
        gate_n = self.cav.create_rectangle(1075, 490, 1125, 520,
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
        if sens == 5:
            sens = 1
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
        gate_key = self.cav.gettags(gate_id)[0]
        lengthx = dico_gates[gate_key][0] // 2
        lengthy = dico_gates[gate_key][1] // 2
        self.coord_move = [event.x, event.y]
        if ((x1_circuit + lengthx < event.x < x2_circuit - lengthx) and
           (y1_circuit + lengthy < event.y < y2_circuit - lengthy)):
            if int(sens) % 2 != 0:
                self.cav.coords(gate_id, event.x - lengthx, event.y - lengthy,
                                event.x + lengthx, event.y + lengthy)
            else:
                self.cav.coords(gate_id, event.x - lengthy, event.y - lengthx,
                                event.x + lengthy, event.y + lengthx)

    def move_gate(self, event, id_gate, sens):
        """ Fonction permettant le déplacement de la porte et des fils. """
        x = event.x
        y = event.y
        gate_key = self.cav.gettags(id_gate)[0]
        x, y = self.circuit.correct_position(x, y, gate_key, sens)
        mv_x = x - self.coord_move[0]
        mv_y = y - self.coord_move[1]
        self.cav.move(id_gate, mv_x, mv_y)
        self.coord_move = [x, y]

    def end_move_gate(self):
        """ Fonction finalisant le déplacement de la porte
        et changeant la structure de données. """
        pass
