import tkinter as tk
from const import *
from gates import *


class Circuit:

    def __init__(self, cav):
        self.cav = cav
        self.gates = None

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
        if int(sens) % 2 != 0:
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

        self.cav.tag_bind(gate_id, "<Button-1>",
                          lambda event: self.gates.init_move_gate(event,
                                                                  gate_id,
                                                                  sens))
        self.cav.tag_bind(gate_id, "<B1-Motion>",
                          lambda event: self.gates.move_gate(event,
                                                             gate_id, sens))
        self.cav.tag_bind(gate_id, "<ButtonRelease-1>",
                          lambda event: self.gates.end_move_gate(event))
        self.cav.tag_bind(gate_id, "<Button-3>",
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

    def init_sensor(self):
        """ Fonction initialisant et affichant les capteurs.
        Effectue également les bindings. """
        self.cav.create_rectangle(0, 185, 20, 205,
                                  fill="deeppink", tags="capteur")
        self.cav.create_rectangle(0, 305, 20, 325,
                                  fill="deeppink", tags="capteur")
        self.cav.create_rectangle(0, 425, 20, 445,
                                  fill="deeppink", tags="capteur")
        self.cav.create_rectangle(0, 545, 20, 565,
                                  fill="deeppink", tags="capteur")

    def intit_motor(self):
        """ Fonction initialisant et affichant les moteurs.
        Effectue également les bindings """
        pass

    def init_wire(self, x, y, x1, y1):
        """ Fonction créant et affichant les fils. """
        pass

    def move_wire(self, x, y):
        """ Fonction supprimant et recréant le fil
        à chaque mouvement de la souris. """
        pass

    def end_wire(self):
        """ Fonction simulant un event pour vérifier que le fil fini
        bien sur une entrée/sortie. """
        pass
