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
        self.idd_popup = []
        self.indicator_popup = 0
        
        self.funcid = []
        self.layout_uncover = None

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

    def start(self):
        self.bind()
        if self.indicator_popup == 0:
            self.create()
        elif self.indicator_popup != "notouch":
            self.delete_all_circle()
            self.create_map()
        self.indicator_popup = 0

    def create(self):
        x1 = editor_grid_x1
        y1 = editor_grid_y1
        x2 = editor_grid_x1 + editor_grid_square
        y2 = editor_grid_y1 + editor_grid_square
        while (y2 <= editor_grid_height + editor_grid_y1):
            self.cav.create_rectangle(x1, y1, x2, y2, outline="grey60", fill="grey80", tags="square")
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
                print(line)
                j = 0
                for circle in line:
                    if circle != "0":
                        self.first_place(i, j)
                        self.update_around(i, j)
                    j += 1
                i += 1

    def bind(self):
        self.funcid.append(self.cav.bind("<Button-1>", self.place))
        self.funcid.append(self.cav.bind("<Button-3>", self.remove))
        self.funcid.append(self.cav.bind("<B1-Motion>", self.place))
        self.funcid.append(self.cav.bind("<B3-Motion>", self.remove))

    def stop(self):
        self.unbind()
        self.delete_all_circle()

    def unbind(self):
        self.cav.unbind("<Button-1>", self.funcid[0])
        self.cav.unbind("<Button-3>", self.funcid[1])
        self.cav.unbind("<B1-Motion>", self.funcid[2])
        self.cav.unbind("<B3-Motion>", self.funcid[3])
        self.funcid = []

    def delete_all_circle(self):
        N = len(self.matrix)
        i = 0
        while i < N:
            j = 0
            while j < N:
                self.matrix_delete(i, j)
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

    # map manager
    def map_manager_delete(self):
        self.indicator_popup = "notouch"
        self.unbind()
        self.display_delete()
        """
        if fd:
            for i in self.matrix:
                fd.write(str(i)+"\n")
            fd.close()"""

    def map_manager_open(self):
        self.indicator_popup = "notouch"
        self.unbind()
        self.display_open()

    def display_delete(self):
        i = 0
        listdir = os.listdir("map/custom")
        while i < len(listdir):
            x = (width // 2) - editor_delete_gap_x
            y = editor_delete_first_y + (i * editor_delete_gap_x)
            idd = self.cav.create_text(x, y, text=listdir[i], font=("Arial",13))
            self.idd_popup.append(idd)

            x = (width // 2) + editor_delete_gap_x
            y = editor_delete_first_y + (i * editor_delete_gap_x)
            idd = self.cav.create_rectangle(x, y, x+30, y+15, fill="red")
            self.cav.tag_bind(idd, "<Button-1>", lambda event, i=i: self.delete_map(i))
            self.idd_popup.append(idd)
            i += 1

    def display_open(self):
        i = 0
        listdir = os.listdir("map/custom")
        while i < len(listdir):
            x = (width // 2) - editor_open_gap_x
            y = editor_open_first_y + (i * editor_open_gap_x)
            idd = self.cav.create_text(x, y, text=listdir[i], font=("Arial",13))
            self.idd_popup.append(idd)

            x = (width // 2) + editor_open_gap_x
            y = editor_open_first_y + (i * editor_open_gap_x)
            idd = self.cav.create_rectangle(x, y, x+30, y+15, fill="green")
            self.cav.tag_bind(idd, "<Button-1>", lambda event, i=i: self.open_map(i))
            self.idd_popup.append(idd)
            i += 1

    def delete_popup(self):
        for idd in self.idd_popup:
            self.cav.delete(idd)
        self.idd_popup = []

    def delete_map(self, i):
        print(os.listdir("map/custom")[i], "removed")
        #os.remove("map/custom/" + os.listdir("map/custom")[i])
        self.delete_popup()
        self.display_delete()

    def open_map(self, i):
        self.indicator_popup = "map/custom/" + os.listdir("map/custom")[i]
        self.delete_popup()
        self.layout_uncover()
    
    
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
