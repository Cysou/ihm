import tkinter as tk
from PIL import Image, ImageTk
import os
from const import *
from entry import *
from astar import *
from aid import *

class Editor:
    """
    Classe unique.
    Gère l'editeur de niveaux
    Enregistrement, modification et suppression d'un niveau
    Fontion utile : start(*)
    """
    def __init__(self, cav, aid, button):
        self.matrix = []
        self.create_matrix()
        self.cav = cav

        self.img = {}
        self.load_img()
        self.dico_name_img = {"0000": "circle0.png",
                              "0111": "circle1.png",
                              "1011": "circle2.png",
                              "1101": "circle3.png",
                              "1110": "circle4.png",
                              "1100": "circle5.png",
                              "1001": "circle6.png",
                              "0110": "circle7.png",
                              "0011": "circle8.png",
                              "1111": "circle9.png"}
        self.idd_popup = []
        self.indicator_popup = 0

        self.layout_uncover = None

        self.pos_start = None
        self.pos_end = None
        self.idd_start = None
        self.idd_end = None

        self.hidden_circles = []

        self.bind()

        self.entry = Entry(cav)
        self.astar = Astar()
        self.aid = aid
        self.button = button

    def start(self):
        """
        Gère plusieurs cas en fontion :
        - de la premiere ouverture de l'éditeur (on crée tout)
        - si on a ouvert une map et que l'on
        veut lire le fichier et créer la map automatiquement
        En général :
        - Crée la grille, l'entrée, la sortie
        - Gère les évènements au clic de la souris pour créer les murs
        ou déplacer l'entrée/sortie
        - Gère les ouvertures de pop-up pour ouvrir une map en supprimer une
        """
        if self.indicator_popup == 0:
            self.create()
            self.create_start(*editor_pos_start)
            self.create_end(*editor_pos_end)
            self.delete_entry()
            self.create_entry()
        elif self.indicator_popup != "notouch":
            self.delete_all_circle()
            self.delete_start()
            self.delete_end()
            self.create_map()
        self.indicator_popup = 0

    def set_layout_uncover(self, func):
        self.layout_uncover = func

    def create_matrix(self):
        i = editor_grid_height//editor_grid_square
        while i > 0:
            self.matrix.append([0]*(editor_grid_width//editor_grid_square))
            i -= 1

    def load_img(self):
        for path in os.listdir("editor/img"):
            path_all="editor/img/" + path
            pilimg = Image.open(path_all)
            tkimg = ImageTk.PhotoImage(pilimg)
            self.img[path] = tkimg

    def create(self):
        x1 = editor_grid_x1
        y1 = editor_grid_y1
        x2 = editor_grid_x1 + editor_grid_square
        y2 = editor_grid_y1 + editor_grid_square
        while (y2 <= editor_grid_height + editor_grid_y1):
            self.cav.create_rectangle(x1, y1, x2, y2, outline="grey60", fill="grey95", tags="editor_square")
            if x2 >= editor_grid_width + editor_grid_x1:
                x1 = editor_grid_x1
                y1 += editor_grid_square
                x2 = editor_grid_x1 + editor_grid_square
                y2 += editor_grid_square
            else:
                x1 += editor_grid_square
                x2 += editor_grid_square

    def create_map(self):
        with open(self.indicator_popup, "r") as fd:
            i = 0
            for line in fd:
                line = line.strip()
                line = line.split(" ")
                #print(line)
                j = 0
                for circle in line:
                    if circle == "1":
                        self.first_place(i, j)
                        self.update_around(i, j)
                    elif circle == "2":
                        self.create_start(i, j)
                    elif circle == "3":
                        self.create_end(i, j)
                    j += 1
                i += 1

    def create_start(self, i, j):
        x = editor_grid_square*j + editor_grid_x1
        y = editor_grid_square*i + editor_grid_y1
        idd = self.cav.create_image(x, y, anchor="nw", image=self.img["start.png"])
        self.idd_start = idd
        self.matrix[i][j] = idd
        self.pos_start = [i, j]
        self.cav.tag_bind(idd, "<B1-Motion>", self.replace_start)

    def replace_start(self, event):
        i, j = self.get_index(event.x, event.y)
        if self.detect_grid(event.x, event.y):
            if self.matrix[i][j] == 0:
                x = editor_grid_square*j + editor_grid_x1
                y = editor_grid_square*i + editor_grid_y1
                i_old = self.pos_start[0]
                j_old = self.pos_start[1]
                self.matrix[i_old][j_old] = 0
                self.pos_start = [i, j]
                self.matrix[i][j] = self.idd_start
                self.cav.coords(self.idd_start, x, y)

    def delete_start(self):
        i = self.pos_start[0]
        j = self.pos_start[1]
        self.cav.delete(self.matrix[i][j])
        self.matrix[i][j] = 0
        self.pos_start = None
        self.idd_start = None

    def create_end(self, i, j):
        x = editor_grid_square*j + editor_grid_x1
        y = editor_grid_square*i + editor_grid_y1
        idd = self.cav.create_image(x, y, anchor="nw", image=self.img["end.png"])
        self.idd_end = idd
        self.matrix[i][j] = idd
        self.pos_end = [i, j]
        self.cav.tag_bind(idd, "<B1-Motion>", self.replace_end)

    def replace_end(self, event):
        i, j = self.get_index(event.x, event.y)
        if self.detect_grid(event.x, event.y):
            if self.matrix[i][j] == 0:
                x = editor_grid_square*j + editor_grid_x1
                y = editor_grid_square*i + editor_grid_y1
                i_old = self.pos_end[0]
                j_old = self.pos_end[1]
                self.matrix[i_old][j_old] = 0
                self.pos_end = [i, j]
                self.matrix[i][j] = self.idd_end
                self.cav.coords(self.idd_end, x, y)


    def delete_end(self):
        i = self.pos_end[0]
        j = self.pos_end[1]
        self.cav.delete(self.matrix[i][j])
        self.matrix[i][j] = 0
        self.pos_end = None
        self.idd_end = None

    def bind(self):
        self.cav.tag_bind("editor_square", "<Button-1>", self.place)
        self.cav.tag_bind("editor_square", "<Button-3>", self.remove)
        self.cav.tag_bind("editor_square", "<B1-Motion>", self.place)
        self.cav.tag_bind("editor_square", "<B3-Motion>", self.remove)

        self.cav.tag_bind("editor_circle", "<Button-1>", self.place)
        self.cav.tag_bind("editor_circle", "<Button-3>", self.remove)
        self.cav.tag_bind("editor_circle", "<B1-Motion>", self.place)
        self.cav.tag_bind("editor_circle", "<B3-Motion>", self.remove)
        self.cav.tag_bind("editor_circle", "<ButtonRelease-3>", self.delete_hidden_circles)

    def stop(self):
        self.delete_all_circle()
        self.delete_entry()
        self.delete_start()
        self.delete_end()
        self.cav.delete("editor_square")

    def delete_all_circle(self):
        N = len(self.matrix)
        i = 0
        while i < N:
            j = 0
            while j < N:
                self.delete_circle(i, j)
                j += 1
            i += 1

    def place(self, event):
        if self.detect_grid(event.x, event.y):
            x, y = self.find_closest(event.x, event.y)
            self.display_circle(x, y)

    def remove(self, event):
        if self.detect_grid(event.x, event.y):
            x, y = self.find_closest(event.x, event.y)
            self.remove_circle(x, y)

    def remove_circle(self, x, y):
        i, j = self.get_index(x, y)
        self.hide_circle(i ,j)
        self.update_around_inv(i, j)

    def get_index(self, x, y):
        return (y-editor_grid_y1)//editor_grid_square, (x-editor_grid_x1)//editor_grid_square

    def find_closest(self, x, y):
        return (((x-editor_grid_x1)//editor_grid_square) * editor_grid_square) + editor_grid_x1,\
               (((y-editor_grid_y1)//editor_grid_square) * editor_grid_square) + editor_grid_y1

    def detect_grid(self, x, y):
        x1 = editor_grid_x1
        y1 = editor_grid_y1
        x2 = editor_grid_x1 + editor_grid_width
        y2 = editor_grid_y1 + editor_grid_height
        return (x1 <= x < x2) and (y1 <= y < y2)

    def display_circle(self, x, y):
        i, j = self.get_index(x, y)
        if 0 <= i < len(self.matrix) and 0 <= j < len(self.matrix):
            if self.matrix[i][j] == 0:
                self.first_place(i, j)
                self.update_around(i, j)

    def first_place(self, i, j):
        corners = [0,0,0,0]
        li = [i-1, i, i+1, i]
        lj = [j, j-1, j, j+1]
        lc = [(1,1,0,0), (1,0,0,1), (0,0,1,1), (0,1,1,0)]
        a = 0
        N = len(self.matrix)
        while a < 4:
            if 0 <= li[a] < N and 0 <= lj[a] < N:
                if type(self.matrix[li[a]][lj[a]]) == list:
                    self.update_corners(corners, lc[a])
            a += 1
        self.matrix[i][j] = [0, corners]
        name_img = self.get_name_img(self.matrix[i][j][1])
        y = (i * editor_grid_square) + editor_grid_y1
        x = (j * editor_grid_square) + editor_grid_x1
        idd = self.cav.create_image(x, y, anchor="nw", image=self.img[name_img], tags="editor_circle")
        self.matrix[i][j][0] = idd

    def update_around(self, i, j):
        self.update(i-1, j, (0,0,1,1))
        self.update(i, j-1, (0,1,1,0))
        self.update(i+1, j, (1,1,0,0))
        self.update(i, j+1, (1,0,0,1))

    def update(self, i, j, corners):
        if 0 <= i < len(self.matrix) and 0 <= j < len(self.matrix):
            if type(self.matrix[i][j]) == list:
                self.cav.delete(self.matrix[i][j][0])
                self.update_corners(self.matrix[i][j][1], corners)
                name_img = self.get_name_img(self.matrix[i][j][1])
                y = (i * editor_grid_square) + editor_grid_y1
                x = (j * editor_grid_square) + editor_grid_x1
                idd = self.cav.create_image(x, y, anchor="nw", image=self.img[name_img], tags="editor_circle")
                self.matrix[i][j][0] = idd

    def update_corners(self, actual, corners):
        i = 0
        while i < 4:
            if actual[i] == 0:
                actual[i] += corners[i]
            i += 1

    def get_name_img(self, corners):
        string = str(corners[0]) + str(corners[1]) + str(corners[2]) + str(corners[3])
        return self.dico_name_img[string]

    def update_around_inv(self, i, j):
        if self.delete_circle(i-1, j):
            self.first_place(i-1, j)
        if self.delete_circle(i, j-1):
            self.first_place(i, j-1)
        if self.delete_circle(i+1, j):
            self.first_place(i+1, j)
        if self.delete_circle(i, j+1):
            self.first_place(i, j+1)

    def delete_circle(self, i, j):
        if 0 <= i < len(self.matrix) and 0 <= j < len(self.matrix):
            if type(self.matrix[i][j]) == list:
                self.cav.delete(self.matrix[i][j][0])
                self.matrix[i][j] = 0
                return True
        return False

    def hide_circle(self, i, j):
        if 0 <= i < len(self.matrix) and 0 <= j < len(self.matrix):
            if type(self.matrix[i][j]) == list:
                self.cav.itemconfig(self.matrix[i][j][0], state="hidden")
                self.hidden_circles.append(self.matrix[i][j][0])
                self.matrix[i][j] = 0

    def delete_hidden_circles(self, event):
        for idd in self.hidden_circles:
            self.cav.delete(idd)
        self.hidden_circles = []


    # map manager
    def map_manager_delete(self):
        self.indicator_popup = "notouch"
        self.display_delete()

    def map_manager_open(self):
        self.indicator_popup = "notouch"
        self.display_open()

    def display_delete(self):
        i = 0
        listdir = os.listdir("level/custom")
        while i < len(listdir):
            x = (width // 2) - editor_delete_gap_x
            y = editor_delete_first_y + (i * editor_delete_gap_x)
            idd = self.cav.create_text(x, y, text=listdir[i][:-4], fill="white", font=("Arial",13))
            self.idd_popup.append(idd)

            x = (width // 2) + editor_delete_gap_x
            y = editor_delete_first_y + (i * editor_delete_gap_x)
            self.button.create("delete", x+15, y, [[self.delete_map, i]])
            i += 1

    def display_open(self):
        i = 0
        listdir = os.listdir("level/custom")
        while i < len(listdir):
            x = (width // 2) - editor_open_gap_x
            y = editor_open_first_y + (i * editor_open_gap_x)
            idd = self.cav.create_text(x, y, text=listdir[i][:-4], fill="white", font=("Arial",13))
            self.idd_popup.append(idd)

            x = (width // 2) + editor_open_gap_x
            y = editor_open_first_y + (i * editor_open_gap_x)
            self.button.create("ok", x+15, y, [[self.open_map, i]])
            i += 1

    def delete_popup(self):
        for idd in self.idd_popup:
            self.cav.delete(idd)
        self.idd_popup = []

    def delete_map(self, i):
        self.button.take()
        os.remove("level/custom/" + os.listdir("level/custom")[i])
        self.delete_popup()
        self.display_delete()
        self.button.delete_taken()

    def open_map(self, i):
        self.button.take()
        self.indicator_popup = "level/custom/" + os.listdir("level/custom")[i]
        self.delete_popup()
        self.layout_uncover()
        self.button.delete_taken()

    def save_map(self):
        matrix = self.transform_matrix()
        if self.astar.search(matrix, 1, 2, 3):
            string = self.entry.get_string()
            if len(string) > 0:
                self.reset_entry()
                self.write_map(string)
            else:
                text = "Veuiller ajouter un nom"
                self.aid.create(text, 922, 222, 1176, 264)
        else:
            text = "Le robot ne peut pas passer"
            self.aid.create(text,
                     editor_grid_x1 + editor_grid_width,
                     editor_grid_y1 + editor_grid_height//1.5)

    def write_map(self, string):
            path = "level/custom/" + string + ".map"
            with open(path, "w") as fd:
                for line in self.matrix:
                    for circle in line:
                        if circle == 0:
                            fd.write("0 ")
                        elif type(circle) == list:
                            fd.write("1 ")
                        elif circle == self.idd_start:
                            fd.write("2 ")
                        elif circle == self.idd_end:
                            fd.write("3 ")
                    fd.write("\n")

    def transform_matrix(self):
        new_matrix = copy.deepcopy(self.matrix)
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if new_matrix[i][j] == 0:
                    new_matrix[i][j] = 0
                elif type(new_matrix[i][j]) == list:
                    new_matrix[i][j] = 1
                elif new_matrix[i][j] == self.idd_start:
                    new_matrix[i][j] = 2
                elif new_matrix[i][j] == self.idd_end:
                    new_matrix[i][j] = 3
        return new_matrix

    # Entry
    def create_entry(self):
        self.entry.create(editor_entry_x, editor_entry_y, outline="white")

    def delete_entry(self):
        self.entry.delete()

    def reset_entry(self):
        self.entry.reset_text()

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(width="false", height="false")

    cav = tk.Canvas(root, width=editor_width, height=editor_height, bg="white")
    cav.pack()

    editor = Editor(cav)
    editor.start()

    idd=cav.create_rectangle(0,0,50,50,fill="blue")
    cav.tag_bind(idd,"<1>",lambda event: editor.save())

    root.mainloop()
