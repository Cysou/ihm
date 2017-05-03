import tkinter as tk
from circuit import *
from const import *


class Gate:

    def __init__(self, cav, circuit):
        self.cav = cav
        self.circuit = circuit
        self.circuit.gates = self
        self.wire = self.circuit.wire
        self.coord_move = []

    def create(self):
        """
        Initialise la création des portes.
        """
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
        """
        Initialise le placement de la porte lorsque l'on
        relache le click gauche de la souris.
        """
        gate_key = self.cav.gettags("current")[0]
        sens = self.cav.gettags("current")[1]
        x = event.x
        y = event.y
        self.circuit.check_placement(x, y, gate_key, sens)

    # def rotate(self, event, id_gate):
    #     """
    #     Permet de faire tourner une porte à 90°.
    #     """
    #     coord = self.cav.coords(id_gate)
    #     tag = self.cav.gettags("current")
    #     sens = int(tag[1]) + 1
    #     x = (coord[0] + coord[2]) // 2
    #     y = (coord[1] + coord[3]) // 2
    #     self.delete_gate(event, id_gate)
    #     if not self.circuit.check_placement(x, y, tag[0], sens):
    #         self.circuit.placement(x, y, tag[0], tag[1])

    def delete_gate(self, event, id_gate):
        """
        Supprime une porte.
        """
        self.cav.delete(id_gate)

    def init_move_gate(self, event, gate_id, sens):
        """
        Initialise le déplacement d'une porte et des fils
        y étant reliés.
        """
        self.coord_move.append(event.x - self.cav.coords(gate_id)[0])
        self.coord_move.append(event.y - self.cav.coords(gate_id)[1])
        self.coord_move.append(None)
        self.coord_move.append(None)
        self.cav.lift(gate_id)

    def move_gate(self, event, gate_id, sens):
        """
        Permet le déplacement de la porte et des fils.
        """
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

        """ /!\     Corriger le move chelou des fils    /!\ """

        if ((self.coord_move[2] is None) and (self.coord_move[3] is None)):
            self.coord_move[2] = x1
            self.coord_move[3] = y1
        for io in self.circuit.struct_gate[gate_id]:
            for wire in io:
                if (self.circuit.struct_wire[wire][1] == gate_id):
                    self.wire.begin_wire.append(wire)
                    l_coord = self.cav.coords(wire)
                    x_wire = l_coord[-2] - self.coord_move[2]
                    y_wire = l_coord[-1] - self.coord_move[3]
                    self.wire.create_wire(x1 + x_wire, y1 + y_wire)
                    self.wire.begin_wire = []
                else:
                    self.wire.begin_wire.append(wire)
                    l_coord = self.cav.coords(wire)
                    x_wire = l_coord[0] - self.coord_move[2]
                    y_wire = l_coord[1] - self.coord_move[3]
                    self.cav.coords(wire, x1 + x_wire, y1 + y_wire,
                                    l_coord[-2], l_coord[-1])
                    self.wire.create_wire(l_coord[-2], l_coord[-1])
                    self.wire.begin_wire = []
        self.coord_move[2] = x1
        self.coord_move[3] = y1
        self.circuit.read_structure()

    def end_move_gate(self):
        """
        Finalise le déplacement de la porte.
        """
        self.coord_move = []
