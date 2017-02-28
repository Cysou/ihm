import tkinter as tk
import os


class Button():
    def __init__(self, cav):
        self.dico = {}
        self.dico_img = {}
        self.cav = cav
        self.load_img()
        print(self.dico_img)


    def load_img(self):
        for img in os.listdir("button/img"):
            actual = self.get_name(img)
            if not img_is_loaded(actual):
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

    def create_text(self, x, y, text, fill, font, size, commands=None):
        idd = self.cav.create_text(int(x), int(y), text=text, fill=fill, font=(font, int(size)), tags="highlight_text")
        self.cav.tag_bind(idd, "<Enter>", lambda event: self.start(event))
        self.cav.tag_bind(idd, "<Leave>", lambda event: self.stop(event))
        self.bind_command(commands, idd)
        self.cav.tag_bind(idd, "<Button-1>", lambda event: self.binding_commands(commands))


    def find(self):
        dico_copy = copy.deepcopy(self.dico)
        for idd in dico_copy:
            self.anim(idd)



def main_loop():

    button.find()

    root.after(50, main_loop)


if __name__ == "__main__":
    root = tk.Tk()
    cav = tk.Canvas(root, width=1200, height=675, bg="black", highlightthickness=0)
    cav.pack()

    button = Button(cav)

    #button.create()

    #main_loop()

    root.mainloop()
