import tkinter as tk
from const import *

class Entry:

    def __init__(self, cav):
        self.cav = cav
        self.coords = None
        self.focus = None
        self.idd_rec = None
        self.idd_text = None
        self.string = ""
        self.funcid = []

    def create(self, x, y, fill="white", outline="black"):
        x1 = x - ((entry_max_char*entry_font_size) // 2) - entry_gap
        y1 = y - (entry_font_size // 2) - entry_gap
        x2 = x + ((entry_max_char*entry_font_size) // 2) + entry_gap
        y2 = y + (entry_font_size // 2) + entry_gap
        idd_rec = self.cav.create_rectangle(x1, y1, x2, y2, outline=outline, fill=fill, width=2)
        self.coords = [x1, y1 ,x2, y2]
        self.idd_rec = idd_rec

        idd_text = self.cav.create_text(x1 + entry_gap, y1, text=self.string, anchor="nw", font=(entry_font_name, entry_font_size))
        self.idd_text = idd_text

        self.funcid.append(self.cav.bind("<Button-1>", self.check_focus))
        self.funcid.append(self.cav.bind_all("<KeyPress>", self.print_char))
        self.cav.tag_bind(idd_rec, "<Enter>", lambda event: self.update_cursor(2))
        self.cav.tag_bind(idd_rec, "<Leave>", lambda event: self.update_cursor(1))

    def update_cursor(self, num):
        if num == 1:
            self.cav.config(cursor="arrow")
        elif num == 2:
            self.cav.config(cursor="hand2")

    def delete(self):
        if self.idd_rec:
            self.cav.delete(self.idd_rec)
            self.cav.delete(self.idd_text)
            self.coords = None
            self.focus = None
            self.idd_rec = None
            self.idd_text = None
            self.string = ""
            self.unbind()
            self.funcid = []

    def unbind(self):
        self.cav.unbind("<Button-1>", self.funcid[0])
        self.cav.unbind("<KeyPress>", self.funcid[1])

    def check_focus(self, event):
        if self.in_entry(event.x, event.y):
            self.focus = True
            self.cav.itemconfig(self.idd_rec, width=3)
        else:
            self.focus = False
            self.cav.itemconfig(self.idd_rec, width=2)

    def in_entry(self, x , y):
        x1, y1, x2, y2 = self.coords
        return ((x1 < x < x2) and (y1 < y < y2))

    def print_char(self, event):
        if self.focus:
            self.update_string(event.char, event.keycode)

    def update_string(self, char, code):
        if code == 8 or code == 22:
            self.string = self.string[:-1]
        else:
            if char in autorised_key:
                if not self.max_char():
                    self.string += char
        self.update_text()

    def max_char(self):
        return (len(self.string) > entry_max_char)

    def update_text(self):
        self.cav.itemconfig(self.idd_text, text=self.string)

    def get_string(self):
        return self.string

    def reset_text(self):
        self.string = ""
        self.update_text()


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(width="false", height="false")

    cav = tk.Canvas(root, width=editor_width, height=editor_height, bg="grey80")
    cav.pack()

    entry = Entry(cav)
    entry.create(200,200)

    root.mainloop()
