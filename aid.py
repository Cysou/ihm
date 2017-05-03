import tkinter as tk
from const import *
import copy

class Aid:
    """
    Classe non unique.
    Affiche pendant un temps un message d'aide
    Nécessite un appel dans la fontion récurssive
    Fontion utile : create(*)
    """
    compteur = 0
    def __init__(self, cav):
        self.cav = cav
        self.dico = {}

    def create(self, text, bbx1, bby1, bbx2="n", bby2="n", color="black", fill="white", outline="black"):
        """
        Crée le carré d'aide
        text : texte a afficher
        bbx1/bby1/bbx2/bby2 : coords du renctangle autour duquel le fonction va essayer d'afficher l'aide
        On peut aussi définir un point
        color : couleur du texte
        fill : couleur de fond
        outline: couleur du contour
        Returne rien
        """
        if bbx2 == "n" and bby2 == "n":
            bbx2 = bbx1
            bby2 = bby1
        Aid.compteur += 1
        self.dico[Aid.compteur] = [aid_sec * 1000]
        coords = self.create_coords(bbx1, bby1, bbx2, bby2)
        self.create_rectangle(coords, bbx1, bbx2, fill, outline)
        self.create_text(coords, text, color)

    def create_rectangle(self, coords, bbx1, bbx2, fill, outline):
        self.verif_y(coords)
        self.verif_x(coords, bbx1, bbx2)
        idd = self.cav.create_polygon(coords, fill=fill, outline=outline)
        self.dico[Aid.compteur].append(idd)

    def create_text(self, coords, text, color):
        x1, y1 = [coords[0] , coords[1]]
        x2, y2 = [coords[2] , coords[5]]
        x = ((x2 - x1) // 2) + x1
        y = ((y2 - y1) // 2) + y1
        max_width = abs(x2 - x1) - aid_padding
        idd = self.cav.create_text(x, y, text=text, width=max_width, fill=color, font=(aid_font_name, aid_font_size))
        self.dico[Aid.compteur].append(idd)

    def create_coords(self, bbx1, bby1, bbx2, bby2):
        coords = [bbx2 + aid_xoffset, bby1 - aid_len // 2,
            bbx2 + aid_xoffset + aid_len, bby1 - aid_len // 2,
            bbx2 + aid_xoffset + aid_len, bby1 - aid_len // 2 + aid_len,
            bbx2 + aid_xoffset, bby1 - aid_len // 2 + aid_len,
            bbx2 + aid_xoffset, bby1 - aid_len // 2 + aid_len - aid_ygap,
            bbx2,
            bby1 - aid_len // 2 + aid_len - aid_ygap - aid_height_t // 2,
            bbx2 + aid_xoffset,
            bby1 - aid_len // 2 + aid_len - aid_ygap - aid_height_t]
        return coords

    def verif_y(self, coords):
        if coords[1] < aid_margin_top:
            y = aid_margin_top - coords[1]
            self.add_coords(coords, (1, 3, 5, 7), y)
        elif coords[5] > (height - aid_margin_bot):
            y = coords[5] - (height - aid_margin_bot)
            self.add_coords(coords, (1, 3, 5, 7), -y)

    def verif_x(self, coords, bbx1, bbx2):
        if coords[2] > (width - aid_margin_left):
            x = bbx2 - bbx1
            self.add_coords(coords, (10,), -x)
            x = x + (2 * aid_xoffset)
            self.add_coords(coords, (0, 6, 8, 12), -x)
            x = x + (2 * aid_len)
            self.add_coords(coords, (2, 4), -x)

    def add_coords(self, coords, indexs, value):
        for i in indexs:
            coords[i] += value

    def update(self):
        memo = copy.deepcopy(self.dico)
        for key in memo:
            self.dico[key][0] -= main_loop_mili
            self.check_end(key)

    def check_end(self, key):
        if self.dico[key][0] == 0:
            self.cav.delete(self.dico[key][1],  self.dico[key][2])
            self.dico.pop(key)


def main_loop():
    aid.update()
    root.after(main_loop_mili, main_loop)


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(width="false", height="false")

    cav = tk.Canvas(root, width=editor_width, height=editor_height, bg="grey80")
    cav.pack()

    aid = Aid(cav)
    bbox = [600, 300, 700, 350]
    cav.create_rectangle(bbox, fill="grey60")
    text = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."
    #aid.create(text, *bbox)

    cav.bind("<1>", lambda event, text=text, bbox=bbox: aid.create(text, *bbox))

    main_loop()

    root.mainloop()
