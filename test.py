import tkinter as tk
from PIL import Image, ImageTk
import os

img={}

def test(event):
    cav.tag_raise("1", "3")

def test2(event):
    idd = event.widget.gettag("current")
    tag = event.widget.find_withtag("current")
    print(idd)

def load_img():
    """
    Récupère la liste d'images
    situées dans 'img_divers/'.
    """
    for path in os.listdir("img_divers/"):
        path_all="img_divers/" + path
        pilimg = Image.open(path_all)
        tkimg = ImageTk.PhotoImage(pilimg)
        img[path] = tkimg

if __name__ == "__main__":
    root = tk.Tk()
    cav = tk.Canvas(root, width=1200, height=675, highlightthickness=0, bg="white")
    cav.pack()

    path_all="img_divers/and.png"
    pilimg = Image.open(path_all)
    tkimg = ImageTk.PhotoImage(pilimg)
    cav.create_image(500, 500, anchor="nw",
                      image=tkimg,
                      state="disabled",
                      tags=("sensor", "obj"))
    cav.create_rectangle(0, 0, 100, 100, fill="red", tags="1")
    cav.create_rectangle(20, 20, 120, 120, fill="blue", tags="2")
    cav.create_rectangle(40, 40, 140, 140, fill="grey", tags="3")

    #cav.bind("<Button-1>", test)

    cav.bind("<Button-1>", test2)

    root.mainloop()
