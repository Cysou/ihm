"""
Fichier contenant les constantes
"""
# general
width = 1200
height = 675
main_loop_mili = 50

# map.py
map_width = 200
map_height = 200
map_square = 10  # doit être divisible par width et height
map_nb_square = map_height / map_square

# editor.py
editor_width = width
editor_height = height

editor_grid_square = 30  # laisser à 30 sinon taille img plus bon
editor_grid_width = editor_grid_square * (map_width//map_square)
editor_grid_height = editor_grid_square * (map_height//map_square)
editor_grid_x1 = (editor_width - editor_grid_width) // 2
editor_grid_y1 = (editor_height - editor_grid_height) // 2

editor_pos_start = (19, 0)
editor_pos_end = (0, 19)

editor_delete_first_y = 100
editor_delete_gap_x = 50
editor_delete_gap_y = 50

editor_open_first_y = 100
editor_open_gap_x = 50
editor_open_gap_y = 50

editor_entry_x = 1050
editor_entry_y = 250

# gates.py
gates_window_width = 200
gates_window_height = 475
dico_gates = {}
dico_gates["gate_or"] = (40, 25, "blue")
dico_gates["gate_and"] = (40, 25, "red")
dico_gates["gate_xor"] = (40, 25, "seagreen")
dico_gates["gate_not"] = (40, 25, "purple")

# wire.py
# Dictionnaire utilisé pour les déplacements des fils.
dico_wire = {}
dico_wire["gate_or"] = ([0, dico_gates["gate_or"][1]//4], [0, dico_gates["gate_or"][1]*3//4], [dico_gates["gate_or"][0], dico_gates["gate_or"][1]//2])
dico_wire["gate_and"] = ([0, dico_gates["gate_and"][1]//4], [0, dico_gates["gate_and"][1]*3//4], [dico_gates["gate_and"][0], dico_gates["gate_and"][1]//2])
dico_wire["gate_xor"] = ([0, dico_gates["gate_xor"][1]//4], [0, dico_gates["gate_xor"][1]*3//4], [dico_gates["gate_xor"][0], dico_gates["gate_xor"][1]//2])
dico_wire["gate_not"] = ([0, dico_gates["gate_not"][1]//2], [dico_gates["gate_not"][0], dico_gates["gate_not"][1]//2])

# circuit.py
x1_circuit = 0
y1_circuit = 75
x2_circuit = 1000
y2_circuit = 675

# sensor
sensor_width = 20
sensor_height = 20

# motor
motor_width = 20
motor_height = 20

# entry.py
entry_max_char = 15
entry_font_name = "Courier New"
entry_font_size = 16
entry_gap = 5
autorised_key = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8',
                 '9', ' ', '_', '-', 'é', 'è', 'à', 'ù', 'ç']

# aid.py
aid_len = 120  # coté du carré
aid_xoffset = 40  # l'offset du carré a droite de la bbox
aid_ygap = 15  # l'écrat entre le bas du triangle et le bas du rectangle a droite
aid_height_t = 30  # hauteur du triangle
aid_margin_top = 5
aid_margin_left = 30
aid_margin_bot = 5
aid_font_name = "Verdana"
aid_font_size = 10
aid_sec = 2
aid_padding = 5

# help.py
help_font_name = "Noto Sans CJK JP"
help_font_size = 12

# level.py
level_start_x = 80
level_start_y = 80
level_gap_x = 80
level_gap_y = 15
level_lenght_square = 9
