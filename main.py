import tkinter as tk
import highlight as m_highlight
import layout as m_layout
import editor as m_editor
import helps as m_help
import button as m_button
from const import *

def main_loop():
    """
    fonction récurssive pour gérer les animations et autres
    """
    highlight.find()

    root.after(main_loop_mili, main_loop)

if __name__ == "__main__":
    root = tk.Tk()
    cav = tk.Canvas(root, width=1200, height=675, highlightthickness=0)
    cav.pack()

    #classes
    highlight = m_highlight.Highlight(cav)

    editor = m_editor.Editor(cav)

    helps = m_help.Help(cav)

    button = m_button.Button(cav)

    layout = m_layout.Layout(root, cav, highlight, editor, button, helps)
    layout.display("home")

    main_loop()

    root.mainloop()
