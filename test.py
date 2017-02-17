import tkinter as tk

def test(event):
    cav.tag_raise("1", "3")

if __name__ == "__main__":
    root = tk.Tk()
    cav = tk.Canvas(root, width=1200, height=675, highlightthickness=0, bg="black")
    cav.pack()


    cav.create_rectangle(0, 0, 100, 100, fill="red", tags="1")
    cav.create_rectangle(20, 20, 120, 120, fill="blue", tags="2")
    cav.create_rectangle(40, 40, 140, 140, fill="grey", tags="3")

    cav.bind("<Button-1>", test)

    root.mainloop()
