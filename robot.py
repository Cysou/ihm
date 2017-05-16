import tkinter as tk
from PIL import Image, ImageTk
import os
from time import sleep
from const import *


class Robot():

    def __init__(self, cav, circuit, aid):
        self.cav = cav
        self.circuit = circuit
        self.circuit.robot = self
        self.path_matrix = None
        self.matrix = None
        self.aid = aid
        self.render = None
        self.img = {}
        self.load_img()

    def read_structure(self):
        """
        Permet la lecture de la structure
        de donnée pour le robot.
        """
        for motor in self.circuit.struct_motor:
            l_entrees_motor = []
            for wire in self.circuit.struct_motor[motor]:
                l_id = self.circuit.struct_wire[wire]
                if (l_id[0] != motor):
                    if (self.cav.gettags(l_id[0])[0] in ["gate_and", "gate_or", "gate_xor", "gate_not"]):
                        self.calc_gate(l_id[0])
                    l_entrees_motor.append(l_id[0])
                else:
                    if (self.cav.gettags(l_id[1])[0] in ["gate_and", "gate_or", "gate_xor", "gate_not"]):
                        self.calc_gate(l_id[1])
                    l_entrees_motor.append(l_id[1])
            self.circuit.struct_val[motor] = self.ou(l_entrees_motor)
            # print(motor, self.circuit.struct_val[motor])
        return self.check_structure()

    def calc_gate(self, gate_id):
        """
        Calcule la valeure résultante d'une porte.
        """
        val_entree = []
        for i in range(2):
            res = []
            entree = self.circuit.struct_gate[gate_id][i]
            for wire in entree:
                l_id = self.circuit.struct_wire[wire]
                if (l_id[0] != gate_id):
                    if (self.cav.gettags(l_id[0])[0] in ["gate_and", "gate_or", "gate_xor", "gate_not"]):
                        self.calc_gate(l_id[0])
                    res.append(l_id[0])
                else:
                    if (self.cav.gettags(l_id[1])[0] in ["gate_and", "gate_or", "gate_xor", "gate_not"]):
                        self.calc_gate(l_id[1])
                    res.append(l_id[1])
            val_entree.append(self.ou(res))
            if (self.cav.gettags(gate_id)[0] == "gate_not"):
                val_entree.append(None)
                break
        self.circuit.struct_val[gate_id] = self.ope_gate(gate_id, val_entree[0], val_entree[1])

    def ou(self, l_id):
        """
        Retourne 1 si la valeur d'un des composants
        de la liste vaut 1, retourne 0 sinon.
        """
        for i in range(len(l_id)):
            if (self.circuit.struct_val[l_id[i]] == 1):
                return 1
        return 0

    def ope_gate(self, gate_id, val_entree1, val_entree2):
        """
        Fait l'opération de la porte entre les
        valeurs finales de ses deux entrées.
        """
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

    def check_structure(self):
        """
        Vérifie que seuleument un moteur est allumé à la fois.
        """
        sum_val = 0
        for motor in self.circuit.struct_motor:
            sum_val += self.circuit.struct_val[motor]
            if (sum_val >= 2):
                return False
        return True

    def detect_murs(self, robot):
        """
        Détecte les murs autour du robot et allume
        les capteurs en conséquence.
        """
        if (0 < robot[1]):
            if (self.matrix[robot[1]-1][robot[0]] == 1):
                self.circuit.struct_val[self.circuit.l_sensor[0]] = 1
            else:
                self.circuit.struct_val[self.circuit.l_sensor[0]] = 0
        else:
            self.circuit.struct_val[self.circuit.l_sensor[0]] = 1

        if (0 < robot[0] ):
            if (self.matrix[robot[1]][robot[0]-1] == 1):
                self.circuit.struct_val[self.circuit.l_sensor[1]] = 1
            else:
                self.circuit.struct_val[self.circuit.l_sensor[1]] = 0
        else:
            self.circuit.struct_val[self.circuit.l_sensor[1]] = 1

        if (robot[0] < 19):
            if (self.matrix[robot[1]][robot[0]+1] == 1):
                self.circuit.struct_val[self.circuit.l_sensor[2]] = 1
            else:
                self.circuit.struct_val[self.circuit.l_sensor[2]] = 0
        else:
            self.circuit.struct_val[self.circuit.l_sensor[2]] = 1

        if (robot[1] < 19):
            if (self.matrix[robot[1]+1][robot[0]] == 1):
                self.circuit.struct_val[self.circuit.l_sensor[3]] = 1
            else:
                self.circuit.struct_val[self.circuit.l_sensor[3]] = 0
        else:
            self.circuit.struct_val[self.circuit.l_sensor[3]] = 1

    def detect_position(self):
        """
        Détecte la position du robot dans le niveau.
        """
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                if (self.matrix[y][x] == 2):
                    return [x, y]

    def create_matrix(self):
        """
        Crée la matrice correspondante
        à la carte choisie.
        """
        with open(self.path_matrix, "r") as fd:
            matrix = []
            i = 0
            for line in fd:
                line = line.strip()
                line = line.split(" ")
                for i in range(len(line)):
                    line[i] = int(line[i])
                # print(line)
                matrix.append(line)
        self.matrix = matrix

    def move_robot(self):
        """
        Permet au robot de bouger sur la carte.
        """
        robot_position = self.detect_position()
        self.detect_murs(robot_position)
        l_val = self.circuit.struct_val
        if (self.read_structure()):
            for i in range(self.circuit.l_motor[0], self.circuit.l_motor[3]+1, 3):
                if (self.circuit.struct_val[i] == 1):
                    self.matrix[robot_position[1]][robot_position[0]] = 0
                    if ((i == self.circuit.l_motor[0]) and (l_val[self.circuit.l_sensor[3]] == 0)):
                        robot_position[1] += 1
                        self.cav.move("robot", 0, 30)
                    elif ((i == self.circuit.l_motor[1]) and (l_val[self.circuit.l_sensor[2]] == 0)):
                        robot_position[0] += 1
                        self.cav.move("robot", 30, 0)
                    elif ((i == self.circuit.l_motor[2]) and (l_val[self.circuit.l_sensor[1]] == 0)):
                        robot_position[0] -= 1
                        self.cav.move("robot", -30, 0)
                    elif ((i == self.circuit.l_motor[3]) and (l_val[self.circuit.l_sensor[0]] == 0)):
                        robot_position[1] -= 1
                        self.cav.move("robot", 0, -30)
                    self.cav.lift("robot")
                    self.cav.update()
                    if (self.matrix[robot_position[1]][robot_position[0]] == 3):
                        return True
                    self.matrix[robot_position[1]][robot_position[0]] = 2
        else:
            self.aid.create("Erreur, plusieurs moteurs sont allumés en même temps.", x2_circuit, y1_circuit + 250)
            return False

    def simulation(self):
        """
        Effectue la simulation du robot.
        """
        self.create_matrix()
        win = False
        self.cav.create_image(0, 0, anchor="nw", image=self.img["layout/img/fond_50.png"], tags="map")
        self.render.level(self.path_matrix, 250, 0, 30, False, True)
        self.cav.update()
        while (not win):
            pos_deb = self.detect_position()
            sleep(1)
            win = self.move_robot()
            if (pos_deb == self.detect_position()):
                text = "Erreur, robot bloqué à la position "+str(pos_deb)+"."
                self.aid.create(text, x2_circuit - 50, y1_circuit + motor_height)
                break
        if (win):
            self.aid.create("Gagné !! Bravo.", x2_circuit, y1_circuit + 220)
        self.cav.update()
        sleep(5)
        self.cav.delete("map")
        self.circuit.mini_map()

    def load_img(self):
            path_all="layout/img/fond_50.png"
            pilimg = Image.open(path_all)
            tkimg = ImageTk.PhotoImage(pilimg)
            self.img[path_all] = tkimg
