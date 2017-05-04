import tkinter as tk
from const import *
from gates import *
from wire import *
from robot import *


class Circuit:

    def __init__(self, cav):
        self.cav = cav
        self.gates = None
        self.wire = None
        self.robot = None

        # Dictionnaires utilisés pour la structure de données.
        self.struct_gate = {}
        self.struct_sensor = {}
        self.struct_motor = {}
        self.struct_wire = {}

        # Dictionnaire utilisé pour conserver
        # les valeurs de chaque objets.
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

        # On récupère les coordonnées à utiliser selon le sens
        # de la porte (verticale ou horizontale).
        if (int(sens) % 2 != 0):
            lengthx = dico_gates[gate_key][0] // 2
            lengthy = dico_gates[gate_key][1] // 2
        else:
            lengthx = dico_gates[gate_key][1] // 2
            lengthy = dico_gates[gate_key][0] // 2
        new_x = x
        new_y = y

        # On ajuste les coordonnées de la porte
        # si elle dépasse un peu du circuit.
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
        if (gate_key != "gate_not"):

            # Initialisation de la structure
            # de la porte (entrée1, entrée2, sortie)
            self.struct_gate[gate_id] = [[], [], []]
        else:

            # Initialisation de la structure
            # de l'inverseur (entrée, sortie)
            self.struct_gate[gate_id] = [[], []]
        self.struct_val[gate_id] = 0

    def display_gate(self, x, y, gate_key, sens):
        """
        Affiche la porte et effectue les binding
        de celle-ci avec les fonctionns correspondantes.
        """
        x1 = dico_gates[gate_key][0] // 2
        y1 = dico_gates[gate_key][1] // 2

        # Affiche selon son sens.
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

        # Fonction de rotation pas opérationnelle
        # avec les fils et la base de donnée.

        # self.cav.tag_bind(gate_id, "<Control-Button-1>",
        #                   lambda event: self.gates.rotate(event, gate_id))

        self.cav.tag_bind(gate_id, "<Control-Button-3>",
                          lambda event: self.empty_structure(event, gate_id))

    def fill_structure(self, id_wire):
        """
        Remplie la structure des données.
        """

        # On récupère l'id du fil qui vient d'être créé
        # ainsi que la liste des types des objets qu'il relie,
        # et leurs id.
        wire_id = self.wire.begin_wire[0]
        l_tags = self.wire.tags_io_wire
        l_id = self.wire.id_extremites_wire

        # Remplissage de la structure de données du fil.
        self.struct_wire[wire_id] = l_id

        # Pour chaque objet relié par le fil:
        for i in range(2):

            # S'il s'agit d'une porte on remplie
            # la partie de la structure correspondante.
            if (self.cav.gettags(l_id[i])[0] in
               ["gate_and", "gate_or", "gate_xor"]):
                if (l_tags[i] == "output"):
                    self.struct_gate[l_id[i]][l_tags[2]].append(wire_id)
                else:
                    self.struct_gate[l_id[i]][2].append(wire_id)

            # S'il s'agit d'un inverseur on remplie
            # la partie de la structure correspondante.
            elif (self.cav.gettags(l_id[i])[0] == "gate_not"):
                if (l_tags[i] == "output"):
                    self.struct_gate[l_id[i]][0].append(wire_id)
                else:
                    self.struct_gate[l_id[i]][1].append(wire_id)

            # S'il s'agit d'un capteur on remplie
            # la partie de la structure correspondante.
            elif (self.wire.tags_io_wire[i] == "input"):
                self.struct_sensor[l_id[i]].append(wire_id)

            # Sinon on remplie la partie
            # de la structure du moteur.
            else:
                self.struct_motor[l_id[i]].append(wire_id)

        # Affichage pour tests.
        print("\nCapteurs: ", self.struct_sensor)
        print("\nMoteurs: ", self.struct_motor)
        print("\nFils: ", self.struct_wire)
        print("\nPortes\n: ", self.struct_gate)

    def empty_structure(self, event, obj_id):
        """
        Enlève un élément de la structure
        de données ainsi que ses associations.
        Supprime également l'élément du canvas.
        """
        tag = self.cav.gettags(obj_id)[0]
        if (tag == "line"):
            self.empty_wire_structure(obj_id)

        elif (tag in ["gate_and", "gate_or", "gate_xor", "gate_not"]):
            self.empty_gate_structure(obj_id)

    def empty_wire_structure(self, wire_id):
        """
        Enlève un fil de la structure
        de données ainsi que ses associations.
        Supprime également le fil du canvas.
        """
        # Si on veut supprimer un fil,
        # pour chacun des objets auquel il est relié:
        for objects in self.struct_wire[wire_id]:

            # Si l'un des objets est une porte,
            # on cherche où il était relié (entrée1, entrée2 ou sortie)
            # et on supprime l'id du fil dans
            # cette partie de la structure de donnée.
            if (self.cav.gettags(objects)[0] in ["gate_and", "gate_or", "gate_xor", "gate_not"]):
                for io in self.struct_gate[objects]:
                    if (wire_id in io):
                        io.remove(wire_id)

            # Sinon on supprime l'id du fil dans
            # la partie de la structure de donnée
            # correspondante (capteur ou moteur).
            elif (self.cav.gettags(objects)[0] == "sensor"):
                self.struct_sensor[objects].remove(wire_id)
            else:
                self.struct_motor[objects].remove(wire_id)

        # On supprime les données de la structure du fil
        # puis on supprime le fil.
        del self.struct_wire[wire_id]
        self.cav.delete(wire_id)

    def empty_gate_structure(self, gate_id):
        """
        Enlève une porte de la structure
        de données ainsi que ses associations.
        Supprime également la porte du canvas.
        """

        # Si on veut supprimer une porte,
        # on supprime en premier lieu les
        # fils reliés à toutes les entrées/sorties
        # de la porte.
        for io in self.struct_gate[gate_id]:
            while (0 < len(io)):
                self.empty_wire_structure(io[0])

        # Puis on supprime les données de la structure
        # de la porte ainsi que la porte.
        del self.struct_gate[gate_id]
        self.cav.delete(gate_id)

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
        for i in range(4):
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
        s'il s'agit d'une entrée ou d'un sortie.
        Initie ensuite le traçage du fil.
        """

        # Différents cas selon le sens de la porte.
        gate_coords = self.cav.coords(gate_id)
        if (int(sens) % 2 != 0):
            lengthx = dico_gates[gate_key][0] // 2
            lengthy = dico_gates[gate_key][1] // 2
            position = self.detect_click_hor(event, gate_coords, gate_key,
                                             lengthx, lengthy)
            if (position == 1):
                x = gate_coords[2]
                y = gate_coords[1] + lengthy
            elif (gate_key != "gate_not"):
                if (position == 2):
                    x = gate_coords[0]
                    y = gate_coords[1] + (lengthy // 2)
                    self.wire.tags_io_wire.append(position-2)
                else:
                    x = gate_coords[0]
                    y = gate_coords[3] - (lengthy // 2)
                    self.wire.tags_io_wire.append(position-2)
            else:
                if (position == 2):
                    x = gate_coords[2]
                    y = gate_coords[1] + lengthy
                else:
                    x = gate_coords[0]
                    y = gate_coords[1] + lengthy

        else:
            lengthx = dico_gates[gate_key][1] // 2
            lengthy = dico_gates[gate_key][0] // 2
            position = self.detect_click_vert(event, gate_coords, gate_key,
                                              lengthx, lengthy)
            if (position == 1):
                x = gate_coords[0] + lengthx
                y = gate_coords[1]
            elif (gate_key != "gate_not"):
                if (position == 2):
                    x = gate_coords[0] + (lengthx // 2)
                    y = gate_coords[3]
                    self.wire.tags_io_wire.append(position-2)
                else:
                    x = gate_coords[2] - (lengthx // 2)
                    y = gate_coords[3]
                    self.wire.tags_io_wire.append(position-2)
            else:
                if (position == 2):
                    x = gate_coords[0] + lengthx
                    y = gate_coords[1]
                else:
                    x = gate_coords[0] + lengthx
                    y = gate_coords[3]
        self.wire.init_wire(event, x, y)

    def detect_click_hor(self, event, gate_coords, gate_key, lengthx, lengthy):
        """
        Détecte sur quelle partie de la porte le click a été
        effectué lorsque celle-ci est horizontale.
        """
        x = event.x
        y = event.y

        # Définie où placer l'information input/output
        # dans la liste associée selon s'il s'agit
        # du début ou de la fin du fil.
        if (self.wire.tags_io_wire[0] != ""):
            placement = 1
        else:
            placement = 0

        # Place l'information input/output dans la liste
        # selon les coordonnées du curseur.
        if (gate_key != "gate_not"):
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
        else:
            if (x >= (gate_coords[0] + lengthx)):
                self.wire.tags_io_wire[placement] = "input"
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

        # Définie où placer l'information input/output
        # dans la liste associée selon s'il s'agit
        # du début ou de la fin du fil.
        if (self.wire.tags_io_wire[0] != ""):
            placement = 1
        else:
            placement = 0

        # Place l'information input/output dans la liste
        # selon les coordonnées du curseur.
        if (gate_key == "gate_not"):
            if (y <= (coords[1] + lengthy)):
                self.wire.tags_io_wire[placement] = "input"
                return 1
            elif ((y > (coords[1] + lengthy)) and (x <= (coords[0] + lengthx))):
                self.wire.tags_io_wire[placement] = "output"
                return 2
            else:
                self.wire.tags_io_wire[placement] = "output"
                return 3
        else:
            if (y <= (coords[1] + lengthy)):
                self.wire.tags_io_wire[placement] = "input"
                return 2
            else:
                self.wire.tags_io_wire[placement] = "output"
                return 3
