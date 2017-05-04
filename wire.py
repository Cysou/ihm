import tkinter as tk
from const import *


class Wire:

        def __init__(self, cav, circuit):
            self.cav = cav
            self.circuit = circuit
            self.circuit.wire = self

            # Liste utilisée pour connaître les types des objets
            # reliés (entrées/sorties) lors de la création du fil.
            self.tags_io_wire = ["", ""]

            # Liste conservant l'id du fil en cours de traçage
            # ainsi que les coordonnées de son point de départ.
            self.begin_wire = []

            # Liste qui récupère les id des objets reliés par un fil
            # afin de remplir la structure de données.
            self.id_extremites_wire = []

        def init_wire(self, event, x, y):
            """
            Initie la création des fils.
            """
            # On récupère le premier objet n'étant pas un fil.
            self.id_extremites_wire = [self.cav.find_overlapping(x, y,
                                                                 x, y)[-1]]
            tag = self.cav.gettags(self.id_extremites_wire[0])[0]
            i = -1
            while tag == "line":
                self.id_extremites_wire = [self.cav.find_overlapping(x, y,
                                                                     x, y)[i]]
                tag = self.cav.gettags(self.id_extremites_wire[0])[0]
                i -= 1

            # On regarde si ce n'est pas un moteur ou un capteur.
            if (tag == "motor"):
                self.tags_io_wire[0] = "output"
            elif (tag == "sensor"):
                self.tags_io_wire[0] = "input"

            # On commence à tracer le fil.
            wire_id = self.cav.create_line(x, y, x, y, tags="line",
                                           activefill='red')
            self.begin_wire = [wire_id, x, y]

        def move_wire(self, event):
            """
            Supprime et recrée le fil
            à chaque mouvement de la souris
            tant que le clic gauche est maintenue.
            """
            wire_id = self.begin_wire[0]
            x = event.x
            y = event.y
            self.create_wire(x, y)

        def end_wire(self, event):
            """
            Vérifie que le fil fini
            bien sur une entrée/sortie
            Une fois le clic gauche relâché.
            """
            # Si on ne relâche pas le fil dans le vide:
            ident = self.cav.find_overlapping(event.x, event.y,
                                              event.x, event.y)
            if (len(ident) > 2):

                # On récupère l'objet juste en dessous du fil.
                # Ainsi que son tags et ses coordonnées.
                self.id_extremites_wire.append(ident[-2])
                tag = self.cav.gettags(self.id_extremites_wire[1])[0]
                coords = self.cav.coords(self.id_extremites_wire[1])

                # S'il s'agit d'un moteur ou d'un capteur on ajuste
                # les coordonnées du points final du fil affin que
                # celui-ci ne déborde pas sur l'objet.
                if (tag == "motor"):
                    self.tags_io_wire[1] = "output"
                    x = coords[0]
                    y = coords[1] + motor_height // 2
                    self.create_wire(x, y)
                elif (tag == "sensor"):
                    self.tags_io_wire[1] = "input"
                    x = coords[2]
                    y = coords[1] + sensor_height // 2
                    self.create_wire(x, y)

                # Mais s'il s'agit d'une porte, on vérifie
                # d'abord si elle est placée horizontalement ou verticalement.
                elif (tag in ["gate_and", "gate_or", "gate_xor", "gate_not"]):
                    sens = self.cav.gettags(self.id_extremites_wire[1])[1]
                    if (int(sens) % 2 != 0):
                        lengthx = dico_gates[tag][0] // 2
                        lengthy = dico_gates[tag][1] // 2
                        io = self.circuit.detect_click_hor(event, coords,
                                                           tag, lengthx,
                                                           lengthy)

                        # On ajuste les coordonnées en fonction de la zone
                        # de la porte on a relâché le fil
                        # (entrée1/entrée2/sortie) avant de le créer.
                        if (io == 1):
                            x = coords[2]
                            y = coords[1] + lengthy
                        elif (tag != "gate_not"):
                            if (io == 2):
                                x = coords[0]
                                y = coords[1] + lengthy // 2
                                self.tags_io_wire.append(io-2)
                            elif (io == 3):
                                x = coords[0]
                                y = coords[3] - lengthy // 2
                                self.tags_io_wire.append(io-2)
                        else:
                            if (io == 2):
                                x = coords[2]
                                y = coords[1] + lengthy
                            else:
                                x = coords[0]
                                y = coords[1] + lengthy
                        self.create_wire(x, y)
                    else:
                        lengthx = dico_gates[tag][1] // 2
                        lengthy = dico_gates[tag][0] // 2
                        io = self.circuit.detect_click_vert(event, coords,
                                                            tag, lengthx,
                                                            lengthy)

                        # On ajuste les coordonnées en fonction de la zone
                        # de la porte on a relâché le fil
                        # (entrée1/entrée2/sortie) avant de le créer.
                        if (io == 1):
                            x = coords[0] + lengthx
                            y = coords[1] - 1
                        elif (tag != "gate_not"):
                            if (io == 2):
                                x = coords[0] + lengthx
                                y = coords[3] + 1
                                self.tags_io_wire.append(io-2)
                            elif (io == 3):
                                x = coords[2] - lengthx // 2
                                y = coords[3] + 1
                                self.tags_io_wire.append(io-2)
                        else:
                            if (io == 2):
                                x = coords[0] + lengthx
                                y = coords[1]
                            else:
                                x = coords[0] + lengthx
                                y = coords[3]
                        self.create_wire(x, y)
                self.check_wire()

            # Si on relâche le fil dans le vide,
            # on le supprime et on ré-initialise
            # les listes si nécessaire.
            else:
                if ((event.x <= x2_circuit) and (event.y >= y1_circuit)):
                    self.tags_io_wire = ["", ""]
                    self.id_extremites_wire = []
                self.cav.delete(self.begin_wire[0])
            self.begin_wire = []

        def check_wire(self):
            """
            Vérifie la validité du fil.
            S'il n'est pas relié à un couple
            entrée/sortie, il est supprimé.
            """
            wire_id = self.begin_wire[0]
            if (self.tags_io_wire[0] != self.tags_io_wire[1]):
                if (self.id_extremites_wire[0] == self.id_extremites_wire[1]):
                    self.cav.delete(self.begin_wire[0])
                else:
                    self.circuit.fill_structure(wire_id)
                    self.cav.tag_bind(wire_id, "<Enter>", self.wire_lift)
                    self.cav.tag_bind(wire_id, "<Control-Button-3>",
                                      lambda event: self.circuit.empty_structure(event, wire_id))
            elif (self.tags_io_wire[0] == "input"):
                # Pour pop-up signalant l'invalidité du fil.
                self.cav.delete(self.begin_wire[0])
            elif (self.tags_io_wire[0] == "output"):
                # Pour pop-up signalant l'invalidité du fil.
                self.cav.delete(self.begin_wire[0])
            self.tags_io_wire = ["", ""]
            self.id_extremites_wire = []

        def create_wire(self, x, y):
            """
            Crée le fil de manière brisée.
            """
            wire_id = self.begin_wire[0]
            wire_coord = self.cav.coords(wire_id)

            if (x < x1_circuit):
                x = x1_circuit
            elif (x > x2_circuit):
                x = x2_circuit

            if (y < y1_circuit):
                y = y1_circuit
            elif (y > y2_circuit):
                y = y2_circuit

            self.cav.coords(wire_id, wire_coord[0], wire_coord[1],
                            (wire_coord[0] + x) / 2,
                            wire_coord[1],
                            (wire_coord[0] + x) / 2, y, x, y)

        def move_wire_gate(self, gate_id, gate_key, x1, y1):
            """
            Déplace les fils d'une porte lorsque
            celle-ci bouge pour qu'ils la suivent.
            """
            for i in range(3):
                io = self.circuit.struct_gate[gate_id][i]
                for wire in io:
                    if (self.circuit.struct_wire[wire][1] == gate_id):
                        self.begin_wire.append(wire)
                        self.create_wire(x1 + dico_wire[gate_key][i][0],
                                              y1 + dico_wire[gate_key][i][1])
                        self.begin_wire = []
                    else:
                        self.begin_wire.append(wire)
                        l_coord = self.cav.coords(wire)
                        self.cav.coords(wire, x1 + dico_wire[gate_key][i][0],
                                        y1 + dico_wire[gate_key][i][1],
                                        l_coord[-2], l_coord[-1])
                        self.create_wire(l_coord[-2], l_coord[-1])
                        self.begin_wire = []
                if (gate_key == "gate_not" and i == 1):
                    break

        def wire_lift(self, event):
            """
            Met le fil sélectionné au-dessus des objets.
            """
            self.cav.lift(self.cav.find_withtag("current"))
