import tkinter as tk
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

    root.mainloop()
