import tkinter as tk
from const import *

class Aid:
    
    def __init__(self, cav):
        self.cav = cav
        
    def create(self, bbx1, bby1, bbx2, bby2, text):
        x1 = bbx2 + aid_xoffset
        y1 = bby1 - aid_len // 2
        x2 = x1 + aid_len
        y2 = y1
        x3 = x2
        y3 = y1 + aid_len
        x4 = x1
        y4 = y3
        x5 = x4
        y5 = y4 - aid_ygap
        x6 = bbx2
        y6 = y5 - (aid_height_t // 2)
        x7 = x5
        y7 = y5 - aid_height_t
        coords = [x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7]
        self.verif_y(coords)
        self.verif_x(coords, bbx1, bbx2)
        self
        self.cav.create_polygon(coords, fill="orange", outline="blue")
        
    def verif_y(self, coords):
        if coords[1] < aid_margin_top:
            y = aid_margin_top - coords[1]
            self.add_coords(coords, (1, 3, 5, 7), y)
        elif coords[5] > (height - aid_margin_bot):
            y = coords[5] - (height - aid_margin_bot)
            self.add_coords(coords, (1, 3, 5, 7), -y)

    def verif_x(self, coords, bbx1, bbx2):
        if coords[2] > (width - aid_margin_left):
            x = bbx2 - bbx1
            self.add_coords(coords, (10,), -x)
            x = x + (2 * aid_xoffset)
            self.add_coords(coords, (0, 6, 8, 12), -x)
            x = x + (2 * aid_len)
            self.add_coords(coords, (2, 4), -x)

    def add_coords(self, coords, indexs, value):
        for i in indexs:
            coords[i] += value

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(width="false", height="false")

    cav = tk.Canvas(root, width=editor_width, height=editor_height, bg="grey80")
    cav.pack()

    aid = Aid(cav)
    bbox = [900, 620, 950, 675]
    cav.create_rectangle(bbox, fill="grey60")
    aid.create(*bbox)

    root.mainloop()
