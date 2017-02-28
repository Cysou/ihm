import tkinter as tk
from PIL import Image, ImageTk
import copy
import os


class Highlight():
    def __init__(self, cav):
        self.dico = {}
        self.img = []
        self.nb_img = len(os.listdir("img"))
        self.cav = cav
        self.load_img()


    def load_img(self):
        for i in range(self.nb_img):
            path="img/highlight" + str(i) + ".png"
            pilimg = Image.open(path)
            tkimg = ImageTk.PhotoImage(pilimg)
            self.img.append(tkimg)


    def get_center(self, idd):
        return self.cav.coords(idd)


    def create_text(self, x, y, text, fill, font, size, commands=None):
        idd = self.cav.create_text(int(x), int(y), text=text, fill=fill, font=(font, int(size)), tags="highlight_text")
        self.cav.tag_bind(idd, "<Enter>", lambda event: self.start(event))
        self.cav.tag_bind(idd, "<Leave>", lambda event: self.stop(event))
        self.bind_command(commands, idd)

    def bind_command(self, commands, idd):
        if commands:
            self.cav.tag_bind(idd, "<Button-1>", lambda event: self.binding_commands(commands))

    def binding_commands(self, commands):
        for com in commands:
            if len(com) > 1:
                com[0](*com[1:])
            else:
                com[0]()

    def delete_highlight_text(self):
        self.cav.delete("highlight_text")
        self.delete_all()


    def start(self, event):
        idd = self.cav.find_withtag("current")[0]
        if self.dico.get(idd):
            self.delete(idd)
        (x, y) = self.get_center(idd)
        self.dico[idd] = [0, "start", None, x, y]


    def stop(self, idd):
        idd = self.cav.find_withtag("current")[0]
        self.dico[idd][0] -= 1
        self.dico[idd][1] = "stop"
        self.verif(idd)


    def verif(self, idd):
        if self.dico[idd][0] == -1 or self.dico[idd][0] == 0:
            self.dico[idd][0] = 1


    def delete_all(self):
        dico_copy = copy.deepcopy(self.dico)
        for idd in dico_copy:
            self.delete(idd)


    def delete(self, idd):
        self.img_delete(idd)
        self.dico.pop(idd)


    def img_delete(self, idd):
        self.cav.delete(self.dico[idd][2])
        self.dico[idd][2] = None


    def find(self):
        dico_copy = copy.deepcopy(self.dico)
        for idd in dico_copy:
            self.anim(idd)


    def anim(self, idd):
        if self.dico[idd][1] == "start":
            #print(self.dico)
            self.img_delete(idd)
            self.dico[idd][2] = self.cav.create_image(self.dico[idd][3], self.dico[idd][4], image=self.img[self.dico[idd][0]], tags="highlight_oval")
            self.cav.tag_raise("highlight_text", "highlight_oval")
            self.dico[idd][0] += 1
            if self.dico[idd][0] == 10:
                self.dico[idd][1] = "pause"
                #print("pause", self.dico)
        elif self.dico[idd][1] == "stop":
            #print(self.dico)
            self.img_delete(idd)
            self.dico[idd][2] = self.cav.create_image(self.dico[idd][3], self.dico[idd][4], image=self.img[self.dico[idd][0]], tags="highlight_oval")
            self.cav.tag_raise("highlight_text", "highlight_oval")
            self.dico[idd][0] -= 1
            if self.dico[idd][0] == -1:
                #print("last", self.dico)
                self.delete(idd)


def main_loop():

    highlight.find()

    root.after(50, main_loop)


if __name__ == "__main__":
    root = tk.Tk()
    cav = tk.Canvas(root, width=1200, height=675, bg="black", highlightthickness=0)
    cav.pack()

    highlight = Highlight(cav)

    highlight.create_text(500, 300, "Bonjour", "white", "Arial", 20)
    highlight.create_text(500, 350, "Salut", "white", "Arial", 20)

    main_loop()

    root.mainloop()
