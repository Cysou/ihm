import tkinter as tk
from PIL import Image, ImageTk
from time import sleep
from const import *


class Render():
    """
    Classe unique.
    Sert à afficher un level
    Fontion utile : level(*)
    """
    def __init__(self, cav, robot, button):
        self.cav = cav
        self.rec = {"void": "white",
                    "wall": "black"}
        self.img = {}
        self.load_img()
        self.layout_display = None
        self.robot = robot
        self.button = button
        self.robot.render = self

    def set_layout_display(self, layout_display):
        self.layout_display = layout_display

    def load_img(self):
        path_all="level/img/end.png"
        pilimg = Image.open(path_all)
        tkimg = ImageTk.PhotoImage(pilimg)
        self.img["end"] = tkimg

        path_all="level/img/start.png"
        pilimg = Image.open(path_all)
        tkimg = ImageTk.PhotoImage(pilimg)
        self.img["start"] = tkimg

        path_all="level/img/start_b.png"
        pilimg = Image.open(path_all)
        tkimg = ImageTk.PhotoImage(pilimg)
        self.img["start_b"] = tkimg

        path_all="level/img/end_b.png"
        pilimg = Image.open(path_all)
        tkimg = ImageTk.PhotoImage(pilimg)
        self.img["end_b"] = tkimg

    def level(self, path, x, y, lenght, bind, big=False):
        with open(path, "r") as fd:
            i = 0
            for line in fd:
                line = line.strip()
                line = line.split(" ")
                # print(line)
                j = 0
                for circle in line:
                    if circle == "0":
                        self.create_rec(i, j, x, y, lenght, "void", path, bind)
                    elif circle == "1":
                        self.create_rec(i, j, x, y, lenght, "wall", path, bind)
                    elif circle == "2":
                        self.create_img(i, j, x, y, lenght, "start", path, bind, big)
                    elif circle == "3":
                        self.create_img(i, j, x, y, lenght, "end", path, bind, big)
                    j += 1
                i += 1
        self.cav.create_rectangle(x, y, x + lenght*map_nb_square,
                                        y + lenght*map_nb_square,
                                        fill=None, width=2, outline="grey80",
                                        tags=("square_render", "map", "obj"))
        self.cav.lift("img_render")

    def create_rec(self, i, j, x, y, lenght, name, path, bind):
        x = x + lenght * j
        y = y + lenght * i
        idd = self.cav.create_rectangle(x, y, x + lenght, y + lenght,
                                        fill=self.rec[name], width=0, tags=("square_render", "map", "obj"))
        if bind:
            self.cav.tag_bind(idd, "<Button-1>", lambda event, path=path: self.init_launch(path))

    def create_img(self, i, j, x, y, lenght, name, path, bind, big):
        x = x + lenght * j
        y = y + lenght * i

        if (big):
            self.cav.create_rectangle(x, y, x + lenght, y + lenght,
                                      fill="white", width=0, tags=("square_render", "map"))
            idd = self.cav.create_image(x, y, ancho="nw", image=self.img[name+"_b"],
                                    tags=("square", "img_render", "map", "obj"))
            if (name == "start"):
                self.cav.create_oval(x, y, x + 29, y + 29, fill="grey60", tags=("map", "robot"), outline="grey60")
        else:
            self.cav.create_rectangle(x, y, x + lenght, y + lenght,
                                      fill="white", width=0, tags=("square_render", "obj"))
            idd = self.cav.create_image(x, y, ancho="nw", image=self.img[name],
                                    tags=("square", "img_render", "map", "obj"))
        if bind:
            self.cav.tag_bind(idd, "<Button-1>", lambda event, path=path: self.init_launch(path))

    def delete(self):
        self.cav.delete("square_render")
        self.cav.delete("img_render")

    def init_launch(self, path):
        self.robot.path_matrix = path
        self.delete()
        self.button.take()
        self.layout_display("game")
        self.button.delete_taken()

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(width="false", height="false")

    cav = tk.Canvas(root, width=editor_width, height=editor_height, bg="white")
    cav.pack()

    render = Render(cav)
    render.level("level/easy/caca.map", 100, 100, 10)

    root.mainloop()
