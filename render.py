import tkinter as tk
from PIL import Image, ImageTk
from const import *


class Render():
    """
    Classe unique.
    Sert à afficher un level
    Fontion utile : level(*)
    """
    def __init__(self, cav):
        self.cav = cav
        self.rec = {"void": "white",
                      "wall": "black"}
        self.img = {}
        self.load_img()

    def load_img(self):
        path_all="level/img/start.png"
        pilimg = Image.open(path_all)
        tkimg = ImageTk.PhotoImage(pilimg)
        self.img["start"] = tkimg

        path_all="level/img/end.png"
        pilimg = Image.open(path_all)
        tkimg = ImageTk.PhotoImage(pilimg)
        self.img["end"] = tkimg

    def level(self, path, x, y, lenght):
        with open(path, "r") as fd:
            i = 0
            for line in fd:
                line = line.strip()
                line = line.split(" ")
                # print(line)
                j = 0
                for circle in line:
                    if circle == "0":
                        self.create_rec(i, j, x, y, lenght, "void")
                    elif circle == "1":
                        self.create_rec(i, j, x, y, lenght, "wall")
                    elif circle == "2":
                        self.create_img(i, j, x, y, lenght, "start")
                    elif circle == "3":
                        self.create_img(i, j, x, y, lenght, "end")
                    j += 1
                i += 1
        self.cav.create_rectangle(x, y, x + lenght*map_nb_square,
                                        y + lenght*map_nb_square,
                                        fill=None, width=2, outline="grey20",
                                        tags="square_render")
        self.cav.lift("img_render")

    def create_rec(self, i, j, x, y, lenght, name):
        x = x + lenght * j
        y = y + lenght * i
        self.cav.create_rectangle(x, y, x + lenght, y + lenght,
                                  fill=self.rec[name], width=0, tags="square_render")

    def create_img(self, i, j, x, y, lenght, name):
        x = x + lenght * j
        y = y + lenght * i
        self.cav.create_rectangle(x, y, x + lenght, y + lenght,
                                  fill="white", width=0, tags="square_render")
        self.cav.create_image(x, y, ancho="nw", image=self.img[name],
                              tags=("square", "img_render"))

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(width="false", height="false")

    cav = tk.Canvas(root, width=editor_width, height=editor_height, bg="white")
    cav.pack()

    render = Render(cav)
    render.level("level/easy/caca.map", 100, 100, 10)

    root.mainloop()
