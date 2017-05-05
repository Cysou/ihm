import tkinter as tk
from PIL import Image, ImageTk
import os


class Layout():
    """
    Classe unique
    Gère différents assemblages de plans
    Un plan contient l'affichage d'objects à l'écran et le lancement de fonctions
    Fontion utile : display(*)
    """
    def __init__(self, root, cav, highlight, editor, button, helps, circuit, gate, level, render, robot):
        self.dico_objects = {" ": []}
        self.actual = " "
        self.actual_cover = None
        self.cav = cav
        editor.set_layout_uncover(self.uncover)
        render.set_layout_display(self.display)
        self.know_types = {"img": self.add_img,
                           "fun": self.add_functions,
                           "rec": self.add_rec,
                           "txt": self.add_text}
        self.know_commands = {"display": self.display,
                              "highlight.delete_highlight_text": highlight.delete_highlight_text,
                              "editor.start": editor.start,
                              "editor.stop": editor.stop,
                              "cover": self.cover,
                              "uncover": self.uncover,
                              "editor.delete_popup": editor.delete_popup,
                              "editor.save_map": editor.save_map,
                              "root.quit": root.quit,
                              "help.stop": helps.stop,
                              "button.delete_taken": button.delete_taken,
                              "button.take": button.take,
                              "level.rem_depth": level.rem_depth,
                              "level.add_depth": level.add_depth,
                              "level.delete": level.delete,
                              "robot.simulation": robot.simulation,
                              "circuit.clean_cav": circuit.clean_cav,
                              "render.level": render.level}

        self.dico_functions = {}
        self.know_functions = {"highlight.create_text": highlight.create_text,
                               "editor.start": editor.start,
                               "editor.map_manager_delete": editor.map_manager_delete,
                               "editor.map_manager_open": editor.map_manager_open,
                               "help.start": helps.start,
                               "button.create": button.create,
                               "circuit.init": circuit.init,
                               "gate.create": gate.create,
                               "level.print_by3": level.print_by3}

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
                if line !="\n" and line[0] != "#":
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
        params, commands = self.get_params_command(fields)
        idd = self.cav.create_image(int(params[0]), int(params[1]), image = self.img[params[2]], state="hidden")
        if len(params) == 4:
            self.dico_objects[actual].append((idd,1))
        else:
            self.dico_objects[actual].append((idd,0))
        self.bind_command(commands, idd)

    def add_rec(self, fields, actual):
        params, commands = self.get_params_command(fields)
        idd = self.cav.create_rectangle(int(params[0]), int(params[1]), int(params[2]), int(params[3]), fill=params[4], width=0, state="hidden")
        if len(params) == 6:
            self.dico_objects[actual].append((idd,1))
        else:
            self.dico_objects[actual].append((idd,0))
        self.bind_command(commands, idd)

    def add_text(self, fields, actual):
        params, commands = self.get_params_command(fields)
        idd = self.cav.create_text(int(params[0]), int(params[1]), text=params[2], fill=params[3], font=(params[4], int(params[5])), state="hidden")
        if len(params) == 7:
            self.dico_objects[actual].append((idd,1))
        else:
            self.dico_objects[actual].append((idd,0))
        self.bind_command(commands, idd)

    def get_params_command(self, fields):
        if fields[-1][0] == "#":
            commands = fields[-1][1:].split("+")
            for i, c in enumerate(commands):
                commands[i] = c.split(":")
            return fields[1:-1], commands
        else:
            return fields[1:], None

    def bind_command(self, commands, idd):
        if commands:
            self.cav.tag_bind(idd, "<Button-1>", lambda event: self.binding_commands(commands))

    def binding_commands(self, commands):
        for com in commands:
            if len(com) > 1:
                self.know_commands[com[0]](*com[1:])
            else:
                self.know_commands[com[0]]()

    # Manage
    def display(self, layout_name):
        """
        layout_name : nom du plan à afficher
        """
        print(layout_name)
        self.delete_layout(self.actual)
        self.actual = layout_name
        self.display_objects(self.actual)
        self.launch_functions(self.actual)


    def display_objects(self, layout_name):
        for idd in self.dico_objects[layout_name]:
            if idd[1]:
                self.cav.lift(idd[0])
            self.cav.itemconfig(idd[0], state="normal")


    def delete_layout(self, layout_name):
        for idd in self.dico_objects[layout_name]:
            self.cav.itemconfig(idd[0], state="hidden")

    def cover(self, layout_name):
        self.actual_cover = layout_name
        self.display_objects(self.actual_cover)
        self.launch_functions(self.actual_cover)

    def uncover(self):
        self.delete_layout(self.actual_cover)
        self.actual_cover = None
        self.display(self.actual)


    # launch direct functions
    def launch_functions(self, layout_name):
        for fields in self.dico_functions[layout_name]:
            params, commands = self.get_params_command(fields)
            if len(params) > 1:
                if commands:
                    for com in commands:
                        com[0] = self.know_commands[com[0]]
                    self.know_functions[params[0]](*(params[1:]+[commands]))
                else:
                    self.know_functions[params[0]](*params[1:])
            else:
                if commands:
                    for com in commands:
                        com[0] = self.know_commands[com[0]]
                    self.know_functions[params[0]](com)
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
