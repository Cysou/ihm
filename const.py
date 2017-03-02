# general
width = 1200
height = 675

# map.py
map_width = 200
map_height = 200
map_square = 10  # doit être divisible par width et height

# editor.py
editor_width = width
editor_height = height

editor_grid_square = 30  # laisser à 30 sinon taille img plus bon
editor_grid_width = editor_grid_square * (map_width//map_square)
editor_grid_height = editor_grid_square * (map_height//map_square)
editor_grid_x1 = (editor_width - editor_grid_width) // 2
editor_grid_y1 = (editor_height - editor_grid_height) // 2

editor_delete_first_y = 100
editor_delete_gap_x = 50
editor_delete_gap_y = 50

editor_open_first_y = 100
editor_open_gap_x = 50
editor_open_gap_y = 50

# gates.py
# la taille des portes doit être impaire
dico_gates = {}
dico_gates["gate_or"] = (5, 3, "or", "blue")
dico_gates["gate_and"] = (5, 3, "and", "red")
dico_gates["gate_not"] = (5, 3, "not", "purple")
dico_gates["gate_xor"] = (5, 3, "xor", "seagreen")

# grid.py
grid_width = 900  # Il faut que grid_width % grid_squares = 0
grid_height = 550  # Il faut que grid_height % grid_squares = 0
grid_squares = 10  # ne pas changer a cause des images
