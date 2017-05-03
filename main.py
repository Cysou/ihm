import tkinter as tk
from const import *
from gates import *
from circuit import *


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=tk.FALSE, height=tk.FALSE)
    root.title("Titre")
    cav = tk.Canvas(root, width=width, height=height, highlightthickness=0)
    cav.pack()

    # classes
    circuit = Circuit(cav)
    wire = Wire(cav, circuit)
    gate = Gate(cav, circuit)
    circuit.init()
    gate.create()
    root.mainloop()
