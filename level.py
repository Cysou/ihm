import tkinter as tk
from PIL import Image, ImageTk
from const import *
import render as m_render
import os


class Level():
    """
    Classe unique.
    Sert à l'affichage du choix de la map
    Fontion utile : start(*)
    """
    def __init__(self, render):
        self.path = {"easy": [],
                     "medium": [],
                     "hard": [],
                     "custom": []}
        self.fill_lists()
        # print(self.path)
        self.max_depth = self.calcul_max_depth()
        # print(self.max_depth)
        self.render = render

    def calcul_max_depth(self):
        maxi = 0
        for dif in self.path:
            if len(dif) > maxi:
                maxi = len(dif)
        return (maxi-1)//3

    def fill_lists(self):
        for repository in ("easy", "medium", "hard", "custom"):
            path = "level/" + repository + "/"
            for i in os.listdir(path):
                self.path[repository] += [path + i]

    def print_by3(self, depth):
        x = level_start_x
        for repository in ("easy", "medium", "hard", "custom"):
            y = level_start_y
            for i in range(depth, depth+3):
                if len(self.path[repository]) >= i+1:
                    self.render.level(self.path[repository][i], x, y, level_lenght_square)
                y += level_lenght_square*map_nb_square + level_gap_y
            x += level_lenght_square*map_nb_square + level_gap_x


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(width="false", height="false")

    cav = tk.Canvas(root, width=editor_width, height=editor_height, bg="white")
    cav.pack()

    render = m_render.Render(cav)

    level = Level(render)
    level.print_by3(0)

    root.mainloop()
