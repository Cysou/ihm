import tkinter as tk
from PIL import Image, ImageTk
import os


class Button():
    """
    Classe unique.
    Sert à la création de boutons animés au survol avec une fonction associée
    Fontion utile : create(*)
    """
    def __init__(self, cav):
        self.dico_img = {}
        self.cav = cav
        self.load_img()
        print(self.dico_img)
        self.clicked = None

    def create(self, name, x, y, function, *params):
        """
        Crée le bouton et associe le fonction
        name : nom de l'image du bouton (voir dans le fichier bouton)
        x/y : coords du centre
        function : fonction associée au clic
        *params : paramètres éventuels de la fonction associée
        Returne rien
        """
        idd = self.cav.create_image(x, y, image=self.dico_img[name][0], tags="button")
        self.cav.tag_bind(idd, "<Enter>", lambda event, idd=idd, name=name: self.modif(idd, name, 1))
        self.cav.tag_bind(idd, "<Leave>", lambda event, idd=idd, name=name: self.modif(idd, name, 0))
        self.cav.tag_bind(idd, "<Button-1>", lambda event, idd=idd, name=name: self.modif(idd, name, 2))
        lol = [idd, name, function, params]
        self.cav.tag_bind(idd, "<ButtonRelease-1>", lambda event, lol=lol: self.launch_function(event, *lol))


    def load_img(self):
        for img in os.listdir("button/img"):
            actual = self.get_name(img)
            if not self.img_is_loaded(actual):
                self.dico_img[actual] = []
                self.load_actual(actual)

    def load_actual(self, actual):
        for genre in ("normal", "overlap", "click"):
            path = "button/img/" + actual + "_" + genre + ".png"
            pilimg = Image.open(path)
            tkimg = ImageTk.PhotoImage(pilimg)
            self.dico_img[actual].append(tkimg)

    def img_is_loaded(self, actual):
        return self.dico_img.get(actual)

    def get_name(self, img):
        i = 0
        while img[i] != "_":
            i += 1
        return img[:i]

    def modif(self, idd, name, i):
        if i == 1:
            if self.clicked == idd:
                self.cav.itemconfig(idd, image=self.dico_img[name][2])
            else :
                self.cav.itemconfig(idd, image=self.dico_img[name][1])

        elif i == 2:
            self.clicked = idd
            self.cav.itemconfig(idd, image=self.dico_img[name][2])

        else:
            self.cav.itemconfig(idd, image=self.dico_img[name][0])

    def launch_function(self, event, idd, name, functions, params):
        self.clicked = None
        bbox = self.cav.bbox(idd)
        if self.in_bbox(event.x, event.y, bbox):
            self.cav.itemconfig(idd, image=self.dico_img[name][1])
            functions(*params)
        else:
            self.cav.itemconfig(idd, image=self.dico_img[name][0])

    def in_bbox(self, x, y, bbox):
        return (bbox[0] < x < bbox[2]) and (bbox[1] < y < bbox[3])

def main_loop():

    button.find()

    root.after(50, main_loop)


if __name__ == "__main__":
    root = tk.Tk()
    cav = tk.Canvas(root, width=1200, height=675, bg="black", highlightthickness=0)
    cav.pack()

    button = Button(cav)

    button.create("delete", 400, 300, print, "delete")
    button.create("up", 450, 300, print, "up")

    #main_loop()

    root.mainloop()
