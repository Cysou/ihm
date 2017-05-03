import tkinter as tk
from const import *
from gates import *
from wire import *


class Circuit:

    def __init__(self, cav):
        self.cav = cav
        self.gates = None
        self.wire = None

        # Dicos utilisés pour la structure de données.
        self.struct_gate = {}
        self.struct_sensor = {}
        self.struct_motor = {}
        self.struct_wire = {}
        self.struct_val = {}

    def check_placement(self, x, y, gate_key, sens):
        """
        Permet de savoir si la porte peut
        être placée dans la zone.
        """
        if self.check_area(x, y):
            x, y = self.correct_position(x, y, gate_key, sens)
            self.placement(x, y, gate_key, sens)
            return True
        return False

    def check_area(self, x, y):
        """
        Permet de savoir si la porte est placée dans
        la zone du circuit.
        """
        return ((x1_circuit <= x <= x2_circuit) and
                (y1_circuit <= y <= y2_circuit))

    def correct_position(self, x, y, gate_key, sens):
        """
        Corrige la position de la porte si sa
        position dépasse la zone du circuit.
        """
        if (int(sens) % 2 != 0):
            lengthx = dico_gates[gate_key][0] // 2
            lengthy = dico_gates[gate_key][1] // 2
        else:
            lengthx = dico_gates[gate_key][1] // 2
            lengthy = dico_gates[gate_key][0] // 2
        new_x = x
        new_y = y
        if (x < (x1_circuit + lengthx)):
            new_x = x1_circuit + lengthx
        elif (x > (x2_circuit - lengthx)):
            new_x = x2_circuit - lengthx

        if (y < (y1_circuit + lengthy)):
            new_y = y1_circuit + lengthy
        elif (y > (y2_circuit - lengthy)):
            new_y = y2_circuit - lengthy

        return (new_x, new_y)

    def placement(self, x, y, gate_key, sens):
        """
        Affiche la porte
        et remplie la structure des données.
        """
        gate_id = self.display_gate(x, y, gate_key, sens)
        self.struct_gate[gate_id] = [[], [], []]
        self.struct_val[gate_id] = -1

    def display_gate(self, x, y, gate_key, sens):
        """
        Affiche la porte et effectue les binding
        de celle-ci avec les fonctionns correspondantes.
        """
        x1 = dico_gates[gate_key][0] // 2
        y1 = dico_gates[gate_key][1] // 2
        if (int(sens) % 2) != 0:
            gate_id = self.cav.create_rectangle(x - x1, y - y1, x + x1, y + y1,
                                                fill=dico_gates[gate_key][2],
                                                tags=(gate_key, sens))
        else:
            gate_id = self.cav.create_rectangle(x - y1, y - x1, x + y1, y + x1,
                                                fill=dico_gates[gate_key][2],
                                                tags=(gate_key, sens))
        self.bindings(gate_id, gate_key, sens)
        return gate_id

    def bindings(self, gate_id, gate_key, sens):
        """
        Effectue les bindings des portes.
        """
        self.cav.tag_bind(gate_id, "<Button-3>",
                          lambda event: self.gates.init_move_gate(event,
                                                                  gate_id,
                                                                  sens))
        self.cav.tag_bind(gate_id, "<B3-Motion>",
                          lambda event: self.gates.move_gate(event,
                                                             gate_id, sens))
        self.cav.tag_bind(gate_id, "<Button-1>",
                          lambda event: self.detect_click(event,
                                                          gate_id,
                                                          gate_key, sens))
        self.cav.tag_bind(gate_id, "<B1-Motion>",
                          lambda event: self.wire.move_wire(event))
        self.cav.tag_bind(gate_id, "<ButtonRelease-1>",
                          lambda event: self.wire.end_wire(event))
        self.cav.tag_bind(gate_id, "<ButtonRelease-3>",
                          lambda event: self.gates.end_move_gate())
        # self.cav.tag_bind(gate_id, "<Control-Button-1>",
        #                   lambda event: self.gates.rotate(event, gate_id))
        self.cav.tag_bind(gate_id, "<Control-Button-3>",
                          lambda event: self.gates.delete_gate(event, gate_id))

    def fill_structure(self, id_wire):
        """
        Remplie la structure des données.
        """
        wire_id = self.wire.begin_wire[0]
        l_tags = self.wire.tags_io_wire
        l_id = self.wire.id_extremites_wire
        self.struct_wire[wire_id] = l_id
        i = 0
        while (i < 2):
            if (self.cav.gettags(l_id[i])[0] in
               ["gate_and", "gate_or", "gate_xor", "gate_not"]):
                if (l_tags[i] == "output"):
                    self.struct_gate[l_id[i]][l_tags[2]].append(wire_id)
                else:
                    self.struct_gate[l_id[i]][2].append(wire_id)
            elif (self.wire.tags_io_wire[i] == "input"):
                self.struct_sensor[l_id[i]].append(wire_id)
            else:
                self.struct_motor[l_id[i]].append(wire_id)
            i += 1
        print("\nCapteurs: ", self.struct_sensor)
        print("\nMoteurs: ", self.struct_motor)
        print("\nFils: ", self.struct_wire)
        print("\nPortes: ", self.struct_gate)

    def init(self):
        """
        Initialise la partie du circuit lors du lancement.
        """
        self.cav.create_rectangle(x1_circuit, y1_circuit,
                                  x2_circuit, y2_circuit,
                                  fill="grey60")
        self.init_sensor()
        self.init_motor()

    def init_sensor(self):
        """
        Initialise et affiche les capteurs.
        Effectue également les bindings.
        """
        placement = (y2_circuit - y1_circuit) // 5
        y1 = y1_circuit + placement - (sensor_height // 2)
        x1 = 0
        for i in range(0, 4):
            ids = self.cav.create_rectangle(x1, y1, x1 + sensor_width,
                                            y1 + sensor_height,
                                            fill="deeppink", tags="sensor")
            self.cav.tag_bind(ids, "<Button-1>",
                              lambda event, y1=y1: self.wire.init_wire(event, x1 + sensor_width,
                                                                       y1 + (sensor_height // 2)))
            self.cav.tag_bind(ids, "<B1-Motion>",
                              lambda event: self.wire.move_wire(event))
            self.cav.tag_bind(ids, "<ButtonRelease-1>",
                              lambda event: self.wire.end_wire(event))
            self.struct_sensor[ids] = []
            self.struct_val[ids] = 1
            y1 += placement

    def init_motor(self):
        """
        Initialise et affiche les moteurs.
        Effectue également les bindings.
        """
        placement = (y2_circuit - y1_circuit) // 5
        y1 = y1_circuit + placement - (motor_height // 2)
        x1 = x2_circuit - motor_width
        for i in range(0, 4):
            idm = self.cav.create_rectangle(x1, y1, x1 + motor_width,
                                            y1 + motor_height,
                                            fill="yellow", tags="motor")
            self.cav.tag_bind(idm, "<Button-1>",
                              lambda event, y1=y1: self.wire.init_wire(event, x1,
                                                                       y1 + (motor_height // 2)))
            self.cav.tag_bind(idm, "<B1-Motion>",
                              lambda event: self.wire.move_wire(event))
            self.cav.tag_bind(idm, "<ButtonRelease-1>",
                              lambda event: self.wire.end_wire(event))
            self.struct_motor[idm] = []
            self.struct_val[idm] = 0
            y1 += placement

    def detect_click(self, event, gate_id, gate_key, sens):
        """
        Permet de savoir sur quelle partie
        de la porte on click, et ainsi de savoir
        s'il s'agitd'une entrée ou d'un sortie.
        Initie ensuite le traçage du fil.
        """
        gate_coords = self.cav.coords(gate_id)
        if (int(sens) % 2 != 0):
            lengthx = dico_gates[gate_key][0] // 2
            lengthy = dico_gates[gate_key][1] // 2
            position = self.detect_click_hor(event, gate_coords, gate_key,
                                             lengthx, lengthy)
            if (position == 1):
                self.wire.init_wire(event, gate_coords[2],
                                    gate_coords[1] + lengthy)
            elif (position == 2):
                self.wire.init_wire(event, gate_coords[0],
                                    gate_coords[1] + (lengthy // 2))
                self.wire.tags_io_wire.append(position-2)
            else:
                self.wire.init_wire(event, gate_coords[0],
                                    gate_coords[3] - (lengthy // 2))
                self.wire.tags_io_wire.append(position-2)
        else:
            lengthx = dico_gates[gate_key][1] // 2
            lengthy = dico_gates[gate_key][0] // 2
            position = self.detect_click_vert(event, gate_coords, gate_key,
                                              lengthx, lengthy)
            if (position == 1):
                self.wire.init_wire(event, gate_coords[0] + lengthx,
                                    gate_coords[1])
            elif (position == 2):
                self.wire.init_wire(event, gate_coords[0] + (lengthx // 2),
                                    gate_coords[3])
                self.wire.tags_io_wire.append(position-2)
            else:
                self.wire.init_wire(event, gate_coords[2] - (lengthx // 2),
                                    gate_coords[3])
                self.wire.tags_io_wire.append(position-2)

    def detect_click_hor(self, event, gate_coords, gate_key, lengthx, lengthy):
        """
        Détecte sur quelle partie de la porte le click a été
        effectué lorsque celle-ci est horizontale.
        """
        x = event.x
        y = event.y
        if (self.wire.tags_io_wire[0] != ""):
            placement = 1
        else:
            placement = 0
        if (x >= (gate_coords[0] + lengthx)):
            self.wire.tags_io_wire[placement] = "input"
            return 1
        elif ((x < (gate_coords[0] + lengthx)) and
              (y <= (gate_coords[1] + lengthy))):
            self.wire.tags_io_wire[placement] = "output"
            return 2
        else:
            self.wire.tags_io_wire[placement] = "output"
            return 3

    def detect_click_vert(self, event, coords, gate_key, lengthx, lengthy):
        """
        Détecte sur quelle partie de la porte le click a été
        effectué lorsque celle-ci est verticale.
        """
        x = event.x
        y = event.y
        if (self.wire.tags_io_wire[0] != ""):
            placement = 1
        else:
            placement = 0
        if (y <= (coords[1] + lengthy)):
            self.wire.tags_io_wire[placement] = "input"
            return 1
        elif ((y > (coords[1] + lengthy)) and (x <= (coords[0] + lengthx))):
            self.wire.tags_io_wire[placement] = "output"
            return 2
        else:
            self.wire.tags_io_wire[placement] = "output"
            return 3

    def read_structure(self):
        """
        Permet la lecture de la structure
        de donnée pour le robot.
        """
        for motor in self.struct_motor:
            l_entrees_motor = []
            for wire in self.struct_motor[motor]:
                l_id = self.struct_wire[wire]
                if (l_id[0] != motor):
                    if (self.cav.gettags(l_id[0])[0] in ["gate_and", "gate_or", "gate_xor", "gate_not"]):
                        self.calc_gate(l_id[0])
                    l_entrees_motor.append(l_id[0])
                else:
                    if (self.cav.gettags(l_id[1])[0] in ["gate_and", "gate_or", "gate_xor", "gate_not"]):
                        self.calc_gate(l_id[1])
                    l_entrees_motor.append(l_id[1])
            self.struct_val[motor] = self.ou(l_entrees_motor)
            print(motor, self.struct_val[motor])

    def calc_gate(self, gate_id):
        """
        Calcule la valeure résultante d'une porte.
        """
        entree1 = self.struct_gate[gate_id][0]
        entree2 = self.struct_gate[gate_id][1]
        val_entree = []
        for i in range(2):
            res = []
            entree = self.struct_gate[gate_id][i]
            for wire in entree:
                l_id = self.struct_wire[wire]
                if (l_id[0] != gate_id):
                    if (self.cav.gettags(l_id[0])[0] in ["gate_and", "gate_or", "gate_xor", "gate_not"]):
                        self.calc_gate(l_id[0])
                    res.append(l_id[0])
                else:
                    if (self.cav.gettags(l_id[1])[0] in ["gate_and", "gate_or", "gate_xor", "gate_not"]):
                        self.calc_gate(l_id[1])
                    res.append(l_id[1])
            val_entree.append(self.ou(res))
        self.struct_val[gate_id] = self.ope_gate(gate_id, val_entree[0], val_entree[1])

    def ou(self, l_id):
        for i in range(len(l_id)):
            if (self.struct_val[l_id[i]] == 1):
                return 1
        return 0

    def ope_gate(self, gate_id, val_entree1, val_entree2):
        tag = self.cav.gettags(gate_id)[0]
        if (tag == "gate_and"):
            return (val_entree1 and val_entree2)
        elif (tag == "gate_or"):
            return (val_entree1 or val_entree2)
        elif (tag == "gate_xor"):
            if val_entree1 and val_entree2:
                return 0
            return (val_entree1 or val_entree2)
        elif (tag == "gate_not"):
            return (not val_entree1)
