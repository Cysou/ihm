import tkinter as tk
import highlight as m_highlight
import layout as m_layout
import editor as m_editor
import helps as m_help
import button as m_button
import aid as m_aid
import circuit as m_circuit
import wire as m_wire
import robot as m_robot
import gates as m_gates
import render as m_render
import level as m_level

from const import *

def main_loop():
    """
    fonction récurssive pour gérer les animations et autres
    """
    highlight.find()
    aid.update()

    root.after(main_loop_mili, main_loop)

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    cav = tk.Canvas(root, width=1200, height=675, highlightthickness=0)
    cav.pack()

    #classes
    highlight = m_highlight.Highlight(cav)

    aid = m_aid.Aid(cav)

    button = m_button.Button(cav)

    editor = m_editor.Editor(cav, aid, button)

    helps = m_help.Help(cav)

    circuit = m_circuit.Circuit(cav)
    wire = m_wire.Wire(cav, circuit)
    robot = m_robot.Robot(cav, circuit, aid)
    gate = m_gates.Gate(cav, circuit)

    render = m_render.Render(cav, robot, button)
    level = m_level.Level(render)

    layout = m_layout.Layout(root, cav, highlight, editor, button, helps, circuit, gate, level, render, robot)
    layout.display("home")



    main_loop()

    root.mainloop()
