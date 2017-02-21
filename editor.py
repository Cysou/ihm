import tkinter as tk
from PIL import Image, ImageTk
import os
from const import *

class Editor:
    
    def __init__(self, cav):
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
        
        self.create()
        self.bind()

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

    def start(self):
        self.create()
        self.bind()

    def create(self):
        x1 = editor_grid_x1
        y1 = editor_grid_y1
        x2 = editor_grid_x1 + editor_grid_square
        y2 = editor_grid_y1 + editor_grid_square
        while (y2 <= editor_grid_height + editor_grid_y1):
            self.cav.create_rectangle(x1, y1, x2, y2, outline="grey60", fill="white", tags="square")
            if x2 >= editor_grid_width + editor_grid_x1:
                x1 = editor_grid_x1
                y1 += editor_grid_square
                x2 = editor_grid_x1 + editor_grid_square
                y2 += editor_grid_square
            else:
                x1 += editor_grid_square
                x2 += editor_grid_square

    def bind(self):
        self.cav.bind("<Button-1>", self.place)
        self.cav.bind("<Button-3>", self.remove)
        self.cav.bind("<B1-Motion>", self.place)
        self.cav.bind("<B3-Motion>", self.remove)
        
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
        self.matrix_delete(i ,j)
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
        return (x1 <= x <= x2) and (y1 <= y <= y2)

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
                if self.matrix[li[a]][lj[a]] != 0:
                    self.update_corners(corners, lc[a])
            a += 1
        self.matrix[i][j] = [0, corners]
        name_img = self.get_name_img(self.matrix[i][j][1])
        y = (i * editor_grid_square) + editor_grid_y1
        x = (j * editor_grid_square) + editor_grid_x1
        idd = self.cav.create_image(x, y, anchor="nw", image=self.img[name_img])
        self.matrix[i][j][0] = idd

    def update_around(self, i, j):
        self.update(i-1, j, (0,0,1,1))
        self.update(i, j-1, (0,1,1,0))
        self.update(i+1, j, (1,1,0,0))
        self.update(i, j+1, (1,0,0,1))

    def update(self, i, j, corners):
        if 0 <= i < len(self.matrix) and 0 <= j < len(self.matrix):
            if self.matrix[i][j] != 0:
                self.cav.delete(self.matrix[i][j][0])
                self.update_corners(self.matrix[i][j][1], corners)
                name_img = self.get_name_img(self.matrix[i][j][1])
                y = (i * editor_grid_square) + editor_grid_y1
                x = (j * editor_grid_square) + editor_grid_x1
                idd = self.cav.create_image(x, y, anchor="nw", image=self.img[name_img])
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
        if self.matrix_delete(i-1, j):
            self.first_place(i-1, j)
        if self.matrix_delete(i, j-1):
            self.first_place(i, j-1)
        if self.matrix_delete(i+1, j):
            self.first_place(i+1, j)
        if self.matrix_delete(i, j+1):
            self.first_place(i, j+1)

    def matrix_delete(self, i, j):
        if 0 <= i < len(self.matrix) and 0 <= j < len(self.matrix):
            if self.matrix[i][j] != 0:
                self.cav.delete(self.matrix[i][j][0])
                self.matrix[i][j] = 0
                return True
        return False
    
    
if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(width="false", height="false")

    cav = tk.Canvas(root, width=editor_width, height=editor_height, bg="white")
    cav.pack()

    editor = Editor(cav)
    #editor.start()

    root.mainloop()
