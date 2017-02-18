import tkinter as tk
from PIL import Image, ImageTk
import os


class Layout():
    def __init__(self, cav, highlight):
        self.dico_objects = {" ": []}
        self.actual = " "
        self.cav = cav
        self.know_types = {"img": self.add_img, "fun": self.add_functions, "rec": self.add_rec}
        self.know_commands = {"display": self.display}

        self.dico_functions = {}
        self.know_functions = {"highlight.create_text": highlight.create_text,
                               "highlight.delete_highlight_text": highlight.delete_highlight_text}

        self.img = {}
        self.load_img()
        self.load_objects()

    # create objects
    def load_img(self):
        for path in os.listdir("layout/img"):
            path_all="layout/img/" + path
            pilimg = Image.open(path_all)
            tkimg = ImageTk.PhotoImage(pilimg)
            self.img[path] = tkimg


    def load_objects(self):
        with open("layout/layout.txt", 'r') as fd:
            actual = None
            for line in fd:
                if line[0] == "*":
                    actual = line[1:].strip()
                    self.dico_objects[actual] = []
                    self.dico_functions[actual] = []
                else:
                    self.add(line.strip().split(), actual)

    def add(self, fields, actual):
        for ktype in self.know_types:
            if fields[0] == ktype:
                self.know_types[ktype](fields, actual)


    def add_img(self, fields, actual):
        params, command = self.get_params_command(fields)
        idd = self.cav.create_image(int(params[0]), int(params[1]), image = self.img[params[2]], state="hidden")
        self.dico_objects[actual].append(idd)
        self.bind_command(command, idd)

    def add_rec(self, fields, actual):
        params, command = self.get_params_command(fields)
        idd = self.cav.create_rectangle(int(params[0]), int(params[1]), int(params[2]), int(params[3]), fill=params[4], state="hidden")
        self.dico_objects[actual].append(idd)
        self.bind_command(command, idd)

    def get_params_command(self, fields):
        if fields[-1][0] == "#":
            return fields[1:-1], fields[-1][1:].split(":")
        else:
            return fields[1:], None

    def bind_command(self, command, idd):
        if command:
            if len(command) > 1:
                self.cav.tag_bind(idd, "<Button-1>", lambda event: self.know_commands[command[0]](*command[1:]))
            else:
                self.cav.tag_bind(idd, "<Button-1>", self.know_commands[command[0]])


    # Manage
    def display(self, layout_name):
        self.delete_actual()
        self.actual = layout_name
        self.display_objects()
        self.launch_functions()


    def display_objects(self):
        for idd in self.dico_objects[self.actual]:
            self.cav.itemconfig(idd, state="normal")


    def delete_actual(self):
        for idd in self.dico_objects[self.actual]:
            self.cav.itemconfig(idd, state="hidden")

    # launch direct functions
    def launch_functions(self):
        for fields in self.dico_functions[self.actual]:
            print(fields)
            params, command = self.get_params_command(fields)
            print(params, command)
            command[0] = self.know_commands[command[0]]
            if len(params) > 1:
                if command:
                    self.know_functions[params[0]](*params[1:], command)
                else:
                    self.know_functions[params[0]](*params[1:])
            else:
                if command:
                    self.know_functions[params[0]](command)
                else:
                    self.know_functions[params[0]]()


    def add_functions(self, fields, actual):
        self.dico_functions[actual].append(fields)


if __name__ == "__main__":
    root = tk.Tk()
    cav = tk.Canvas(root, width=1200, height=675, bg="black")
    cav.pack()

    layout = Layout(cav)
    layout.display("home")

    root.mainloop()
