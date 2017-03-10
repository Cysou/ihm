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
gates_window_width = 200
gates_window_height = 475
dico_gates = {}
dico_gates["gate_or"] = (50, 30, "blue")
dico_gates["gate_and"] = (50, 30, "red")
dico_gates["gate_not"] = (50, 30, "purple")
dico_gates["gate_xor"] = (50, 30, "seagreen")

# circuit.py
x1_circuit = 0
y1_circuit = 75
x2_circuit = 1000
y2_circuit = 675
