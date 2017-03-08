import tkinter as tk
from gates import *


class Circuit:

    def __init__(self, cav):
        self.cav = cav

    def check_placement(self, x, y):
        """ Fonction permettant de savoir si la porte peut
        être placée dans la zone. """
        pass

    def check_area(self, x, y):
        """ Fonction permettant de savoir si la porte est placée dans
        la zone du circuit. """
        pass

    def correct_position(self, x, y):
        """ Fonction corrigeant la position de la porte si sa
        position dépasse la zone du circuit. """
        pass

    def placement(self, x, y):
        """ Fonction affichant la porte
        et remplissant la structure des données. """
        pass

    def display_gate(self):
        """ Fonction affichant la porte et effectuant les binding
        de celle-ci avec les fonctionns correspondantes. """
        pass

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

    def fname(arg):
        pass
