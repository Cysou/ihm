import tkinter as tk
<<<<<<< HEAD
import highlight as m_highlight
import layout as m_layout
import editor as m_editor

def main_loop():

    highlight.find()

    root.after(50, main_loop)

if __name__ == "__main__":
    root = tk.Tk()
    cav = tk.Canvas(root, width=1200, height=675, highlightthickness=0)
    cav.pack()

    #classes
    highlight = m_highlight.Highlight(cav)

    editor = m_editor.Editor(cav)

    layout = m_layout.Layout(cav, highlight, editor)
    layout.display("home")

    main_loop()
=======
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
    gate.create()
>>>>>>> e84608114139e0c6b03cb4cc118b6b7af0891981

    root.mainloop()
