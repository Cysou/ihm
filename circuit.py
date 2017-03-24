import tkinter as tk
from const import *
from gates import *


class Circuit:

    def __init__(self, cav):
        self.cav = cav
        self.gates = None
        self.tags_io_wire = []
        self.begin_wire = []

        # Dicos utilisés pour la structure de données.
        self.struct_input = {}
        self.struct_output = {}
        self.struct_wire = {}

    def check_placement(self, x, y, gate_key, sens):
        """ Fonction permettant de savoir si la porte peut
        être placée dans la zone. """
        if self.check_area(x, y):
            x, y = self.correct_position(x, y, gate_key, sens)
            self.placement(x, y, gate_key, sens)
            return True
        return False

    def check_area(self, x, y):
        """ Fonction permettant de savoir si la porte est placée dans
        la zone du circuit. """
        return ((x1_circuit <= x <= x2_circuit) and
                (y1_circuit <= y <= y2_circuit))

    def correct_position(self, x, y, gate_key, sens):
        """ Fonction corrigeant la position de la porte si sa
        position dépasse la zone du circuit. """
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
        """ Fonction affichant la porte
        et remplissant la structure des données. """
        self.display_gate(x, y, gate_key, sens)
        self.fill_structure()

    def display_gate(self, x, y, gate_key, sens):
        """ Fonction affichant la porte et effectuant les binding
        de celle-ci avec les fonctionns correspondantes. """
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

    def bindings(self, gate_id, gate_key, sens):
        """ Fonction effectuant les bindings des portes. """
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
                          lambda event: self.move_wire(event))
        self.cav.tag_bind(gate_id, "<ButtonRelease-1>",
                          lambda event: self.end_wire(event))
        self.cav.tag_bind(gate_id, "<ButtonRelease-3>",
                          lambda event: self.gates.end_move_gate())
        self.cav.tag_bind(gate_id, "<Control-Button-1>",
                          lambda event: self.gates.rotate(event, gate_id))
        self.cav.tag_bind(gate_id, "<Control-Button-3>",
                          lambda event: self.gates.delete_gate(event, gate_id))

    def fill_structure(self):
        """ Fonction remplissant la structure des données. """
        pass

    def init(self):
        """ Fonction initialisant la partie du circuit lors du lancement. """
        self.cav.create_rectangle(x1_circuit, y1_circuit,
                                  x2_circuit, y2_circuit,
                                  fill="grey60")
        self.init_sensor()
        self.intit_motor()

    def init_sensor(self):
        """ Fonction initialisant et affichant les capteurs.
        #Effectue également les bindings. """
        placement = (y2_circuit - y1_circuit) // 5
        y1 = y1_circuit + placement - (sensor_height // 2)
        x1 = 0
        for i in range(0, 4):
            ids = self.cav.create_rectangle(x1, y1, x1 + sensor_width,
                                            y1 + sensor_height,
                                            fill="deeppink", tags="sensor")
            coords = self.cav.coords(ids)
            self.cav.tag_bind(ids, "<Button-1>",
                              lambda event: self.init_wire(event, coords[2],
                                                           coords[1] + (sensor_width // 2)))
            self.cav.tag_bind(ids, "<B1-Motion>",
                              lambda event: self.move_wire(event))
            y1 += placement

    def intit_motor(self):
        """ Fonction initialisant et affichant les moteurs.
        #Effectue également les bindings """
        placement = (y2_circuit - y1_circuit) // 5
        y1 = y1_circuit + placement - (motor_height // 2)
        x1 = x2_circuit - motor_width
        for i in range(0, 4):
            idm = self.cav.create_rectangle(x1, y1, x1 + motor_width,
                                            y1 + motor_height,
                                            fill="yellow", tags="motor")
            coords = self.cav.coords(idm)
            self.cav.tag_bind(idm, "<Button-1>",
                              lambda event: self.init_wire(event, coords[0],
                                                           coords[1] + (motor_width // 2)))
            self.cav.tag_bind(idm, "<B1-Motion>",
                              lambda event: self.move_wire(event))
            y1 += placement

    def detect_click(self, event, gate_id, gate_key, sens):
        """ Fonction permettant de savoir sur quelle partie
        de la porte on click, et ainsi savoir s'il s'agit
        d'une entrée ou d'un sortie.
        Initie ensuite le tracemzent du fil. """
        gate_coords = self.cav.coords(gate_id)
        if (int(sens) % 2 != 0):
            lengthx = dico_gates[gate_key][0] // 2
            lengthy = dico_gates[gate_key][1] // 2
            position = self.detect_click_hor(event, gate_coords, gate_key,
                                             lengthx, lengthy)
            if (position == 1):
                self.init_wire(event, gate_coords[2], gate_coords[1] + lengthy)
            elif (position == 2):
                self.init_wire(event, gate_coords[0],
                               gate_coords[1] + (lengthy // 2))
            else:
                self.init_wire(event, gate_coords[0],
                               gate_coords[3] - (lengthy // 2))
        else:
            lengthx = dico_gates[gate_key][1] // 2
            lengthy = dico_gates[gate_key][0] // 2
            position = self.detect_click_vert(event, gate_coords, gate_key,
                                              lengthx, lengthy)
            if (position == 1):
                self.init_wire(event, gate_coords[0] + lengthx, gate_coords[1])
            elif (position == 2):
                self.init_wire(event, gate_coords[0] + (lengthx // 2),
                               gate_coords[3])
            else:
                self.init_wire(event, gate_coords[2] - (lengthx // 2),
                               gate_coords[3])

    def detect_click_hor(self, event, gate_coords, gate_key, lengthx, lengthy):
        """ Fonction détectant sur quelle partie de la porte le click a été
        effectué lorsque celle-ci est horizontale. """
        x = event.x
        y = event.y
        if (x >= (gate_coords[0] + lengthx)):
            self.tags_io_wire.append("input")
            return 1
        elif ((x < (gate_coords[0] + lengthx)) and
              (y <= (gate_coords[1] + lengthy))):
            self.tags_io_wire.append("output")
            return 2
        else:
            self.tags_io_wire.append("output")
            return 3

    def detect_click_vert(self, event, coords, gate_key, lengthx, lengthy):
        """ Fonction détectant sur quelle partie de la porte le click a été
        effectué lorsque celle-ci est verticale. """
        x = event.x
        y = event.y
        if (y <= (coords[1] + lengthy)):
            self.tags_io_wire.append("input")
            return 1
        elif ((y > (coords[1] + lengthy)) and (x <= (coords[0] + lengthx))):
            self.tags_io_wire.append("output")
            return 2
        else:
            self.tags_io_wire.append("output")
            return 3

    def init_wire(self, event, x, y):
        """ Fonction créant et affichant les fils et remplissant la
        structure de données. """
        wire_id = self.cav.create_line(x, y, x, y, tags="line")
        self.begin_wire = [wire_id, x, y]

    def move_wire(self, event):
        """ Fonction supprimant et recréant le fil
        à chaque mouvement de la souris. """
        wire_id = self.begin_wire[0]
        x = event.x
        y = event.y
        self.cav.coords(wire_id, self.begin_wire[1], self.begin_wire[2], x, y)
        self.create_wire()

    def end_wire(self, event):
        """ Fonction simulant un event pour vérifier que le fil fini
        bien sur une entrée/sortie. """
        ident = self.cav.find_overlapping(event.x, event.y,
                                          event.x, event.y)
        if (len(ident) > 2):
            ident = ident[-2]
            tag = self.cav.gettags(ident)[0]
            if (tag in ["motor", "input"]):
                self.tags_io_wire.append("output")
            elif (tag in ["sensor", "output"]):
                self.tags_io_wire.append("input")
            elif (tag in ["gate_and", "gate_or", "gate_xor", "gate_not"]):
                sens = self.cav.gettags(ident)[1]
                gate_coords = self.cav.coords(ident)
                if (int(sens) % 2 != 0):
                    lengthx = dico_gates[tag][0] // 2
                    lengthy = dico_gates[tag][1] // 2
                    self.detect_click_hor(event, gate_coords,
                                          tag, lengthx, lengthy)
                else:
                    lengthx = dico_gates[tag][1] // 2
                    lengthy = dico_gates[tag][0] // 2
                    self.detect_click_vert(event, gate_coords,
                                           tag, lengthx, lengthy)
            self.check_wire()
        else:
            ident = ident[-1]
            self.cav.delete(ident)
            self.tags_io_wire = []
        self.begin_wire = []

    def check_wire(self):
        """ Fonction vérifiant la validité du fil. """
        if (self.tags_io_wire[0] != self.tags_io_wire[1]):
            self.fill_structure()
        elif (self.tags_io_wire[0] == "input"):
            # Pour pop-up signalant l'invalidité du fil.
            self.cav.delete(self.begin_wire[0])
        elif (self.tags_io_wire[0] == "output"):
            # Pour pop-up signalant l'invalidité du fil.
            self.cav.delete(self.begin_wire[0])
        self.tags_io_wire = []

    def create_wire(self):
        """ Fonction créant le fil de manière brisée. """
        wire_id = self.begin_wire[0]
        wire_coord = self.cav.coords(wire_id)
        self.cav.coords(wire_id, wire_coord[0], wire_coord[1],
                        (wire_coord[0] + wire_coord[2]) / 2,
                        wire_coord[1],
                        (wire_coord[0] + wire_coord[2]) / 2,
                        wire_coord[1],
                        (wire_coord[0] + wire_coord[2]) / 2,
                        wire_coord[3],
                        (wire_coord[0] + wire_coord[2]) / 2,
                        wire_coord[3], wire_coord[2], wire_coord[3])
