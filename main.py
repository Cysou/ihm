import tkinter as tk
from const import *
from gates import *
from circuit import *


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x675")
    root.resizable(width=tk.FALSE, height=tk.FALSE)
    root.title("Titre")
    cav = tk.Canvas(root, width=width, height=height)
    cav.pack()

    # classes
    circuit = Circuit(cav)
    gate = Gate(cav, circuit)

    root.mainloop()
