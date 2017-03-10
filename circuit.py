import tkinter as tk
from const import *
from gates import *


class Circuit:

    def __init__(self, cav):
        self.cav = cav
        self.gates = None
        self.cav.create_rectangle(x1_circuit, y1_circuit,
                                  x2_circuit, y2_circuit,
                                  fill="grey60")

    def check_placement(self, x, y, gate_key, sens):
        """ Fonction permettant de savoir si la porte peut
        être placée dans la zone. """
        if self.check_area(x, y):
            x, y = self.correct_position(x, y, gate_key)
            self.placement(x, y, gate_key, sens)

    def check_area(self, x, y):
        """ Fonction permettant de savoir si la porte est placée dans
        la zone du circuit. """
        return ((x1_circuit <= x <= x2_circuit)
                and (y1_circuit <= y <= y2_circuit))

    def correct_position(self, x, y, gate_key):
        """ Fonction corrigeant la position de la porte si sa
        position dépasse la zone du circuit. """
        lengthx = dico_gates[gate_key][0] // 2
        lengthy = dico_gates[gate_key][1] // 2
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

    def display_gate(self, x, y, gate_key, sens):
        """ Fonction affichant la porte et effectuant les binding
        de celle-ci avec les fonctionns correspondantes. """
        x1 = dico_gates[gate_key][0] // 2
        y1 = dico_gates[gate_key][1] // 2
        self.cav.create_rectangle(x - x1, y - y1, x + x1, y + y1,
                                  fill=dico_gates[gate_key][2],
                                  tags=(gate_key, sens))

    def init_move_gate(self):
        """ Fonction initialisant le déplacement d'une porte. """
        pass

    def move_gate(self):
        """ Fonction permettant le déplacement de la porte et des fils. """
        pass

    def end_move_gate(self):
        """ Fonction finalisant le déplacement de la porte
        et changeant la structure de données. """
        pass

    def fill_structure(self):
        """ Fonction remplissant la structure des données. """
        pass

    def init(self):
        """ Fonction initialisant la parie du circuit lors du lancement. """
        pass

    def init_sensor(arg):
        """ Fonction initialisant et affichant les capteurs.
        Effectue également les bindings. """
        pass

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
