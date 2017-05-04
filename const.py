# general
width = 1200
height = 675

# gates.py
gates_window_width = 200
gates_window_height = 475
dico_gates = {}
dico_gates["gate_or"] = (50, 30, "blue")
dico_gates["gate_and"] = (50, 30, "red")
dico_gates["gate_xor"] = (50, 30, "seagreen")
dico_gates["gate_not"] = (50, 30, "purple")

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
