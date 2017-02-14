import tkinter as tk
import highlight as m_highlight
import layout as m_layout



if __name__ == "__main__":
    root = tk.Tk()
    cav = tk.Canvas(root, width=1200, height=675, bg="black")
    cav.pack()

    #classes
    highlight = m_highlight.Highlight(cav)
    
    layout = m_layout.Layout(cav, highlight)
    layout.display("test")

    root.mainloop()
