import tkinter as tk
from const import *

class Help:
    """
    Classe non unique.
    Affiche le message d'aide
    Fontion utile : start(*)
    """
    def __init__(self, cav):
        self.cav = cav
        self.idd = None

    def start(self):
        """
        Affiche un texte sur l'écran
        """
        x = 600
        y = 338
        max_width = 600
        color = "black"
        text = """\
Le but du jeu est de permettre à notre robot de retourver la sortie du \
labyrinthe.\n\
Le jeu se déroule en 3 phases :\n\
\t-Le choix du niveau : c'est le labyrinthe dans lequel notre robot pourra \
évoluer.\n\
\t-La construction du circuit : c'est dans cette partie que vous aller devoir \
créer un circuit à l'aide de portes logiques. Le robot possède 4 capteurs \
situés à gauche de l'écran. Ces capteurs sont à l'état "activé" seuleument si \
ils sont situés à un bloc d'un mur. C'est grâce à cela que vous devrez\
dessiner le circuit jusqu'aux moteurs sur la partie gauche pour faire avancer \
votre robot.\
        """
        idd = self.cav.create_text(x, y, text=text, width=max_width, fill=color, font=(help_font_name, help_font_size))
        self.idd = idd

    def stop(self):
        self.cav.delete(self.idd)


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(width="false", height="false")

    cav = tk.Canvas(root, width=editor_width, height=editor_height, bg="grey80")
    cav.pack()

    help = Help(cav)

    cav.bind("<1>", lambda event: help.start() )

    root.mainloop()
