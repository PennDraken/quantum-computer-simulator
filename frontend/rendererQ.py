from pickletools import pyfloat
from math import floor
from tkinter import ACTIVE, Menubutton
import UI
import pygame
import Utilities.Colors as Colors
import bloch_sphere
import Fields.MenuButton as MenuButton
import Fields.calculation_view_window as calculation_view_window
import backend.qusim_class as qusim_class
from Fields.circuit_navigation_window import Circuit_Navigation_Window
import copy
import gates
from gates import Gate, gateHandler
from Utilities.mouse import Mouse
import screenHandler

import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

screen = screenHandler.screen
# this is mainly for testing, expect significant changes
# screen.blit(pygame.font.SysFont('Times New Roman', 45).render('I', True, (170, 200, 200)) ,((x + (n * 50) + 3,y+ (n * 50) - 5))) 

amount = 5 # stand in for number of qubits

def showCalculation(position : tuple, calculations : [str]): # not settled on calculation format, this is a test
    pygame.draw.rect(screen,(position[0], position[1], 100, 100),0)
    for calculation in calculations:
        screen.blit(pygame.font.SysFont(calculation, 45).render(calculation, True, (170, 170, 200)), (position[0]+1, position[1]-2))


handler = gateHandler()
calculations = ["calculation_placeholder"]

framerate = pygame.time.Clock()

# sampleString = "H 2 1 4 X 4 1 2 Z 2 0 H 2 1 4 X 4 1 2 Z 2 0 H 2 1 4 X 4 1 2 Z 2 0 H 2 1 4 X 4 1 2 Z 2 0 H 2 1 4 X 4 1 2 Z 2 0 H 2 1 4 X 4 1 2 Z 2 0"
# TODO: zoom out
offset = (75,75)

# access screen
pygame.display.Info()

circuit_x = 75
circuit_y = 75
# Tag panning:offset som apliceras på allt i scenen
circuit_dx = 0;
circuit_dy = 0;
# Tag meny: menyns höjd variabel 
# textCanvasY =  pygame.display.Info().current_h - 100 #920

drag_bar_y = screen.get_height() - 100
drag_bar_color = Colors.white
drag_bar_height = 15 # Height of draggable bar TODO make this into a reuseable class

tab_panel = UI.ChoicePanel(screen, drag_bar_y + drag_bar_height, ["Logic gates","Math view","Text view","Bloch sphere"])

bloch_sphere = bloch_sphere.Bloch_Sphere(screen, 0, drag_bar_y + 40, screen.get_width(), screen.get_height() - drag_bar_height)
bloch_sphere.add_random_point_on_unit_sphere()
bloch_sphere.add_random_point_on_unit_sphere()

# Calculation window (generate example circuit)
circuit : qusim_class.Circuit = qusim_class.Circuit([["A","B","C"],"Ry(np.pi/4) 0","H 1","CNOT 1 2","CNOT 0 1","H 0", "measure 0", "measure 1", "X 2 1", "Z 2 0"])
# circuit.step_fwd()
# circuit.step_fwd()
# circuit.step_fwd()
# circuit.step_fwd()
# circuit.step_fwd()
# circuit.step_fwd()
# circuit.step_fwd()
calculation_window = calculation_view_window.Calculation_Viewer_Window(screen, 0, tab_panel.y + tab_panel.height, screen.get_width(), screen.get_height() - (tab_panel.y + tab_panel.height), circuit.systems)

circuit_navigation_panel = Circuit_Navigation_Window(screen, 0, 0, circuit)

displayCalc = False
dragging = False

# Mouse status
# drag/drop development below, unfinished
# name of selected gate
#selected = ""
dragging2 = False
coordinates = []

gateBoxHit = False
gateButton = False
         
xtest = 0
ytest = 0
# just for testing 
color = (250,250,250)
        
#buttons for the gate tab

#related to merge
# gateList = [('X', [0,3]),('H', [1,4,2]),('X', [0,3]), ('Z', [1,3,2]),('X', [0,3])]
gateList = circuit.as_frontend_gate_list()
circuit_x = 0
circuit_y = 75

gatesList = ["H", "X", "Y", "Z", "I", "S", "T", "CNOT"]
gateButtons = MenuButton.createGateButtons(gatesList, 40, 40)


# keep track of shifting
moving_gate = False

# the gate being shifted
selectedGate = None

# check if gate was shifting
#wasShifting = False

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    # Draw a dotted line to show where user has stepped to TODO make it dotted
    pygame.draw.line(screen, Colors.yellow, (circuit.position * UI.grid_size + UI.grid_size/2 + circuit_x + circuit_dx, 0), (circuit.position * UI.grid_size + UI.grid_size/2 + circuit_x + circuit_dx, screen.get_height()))
    # Gates placed on the circuit (used for collision detection, resets every frame)
    # Draw circuit view
    screenHandler.renderQlines(amount, circuit_x + circuit_dx, circuit_y + circuit_dy, pygame.display.Info().current_w) # Draws horisontal lines for qubits
    # Draw example circuit
    gates_on_circuit = []
    for i in range(0,len(gateList)):
        gate_data = gateList[i]      
        if i==circuit.position-1:
            color = Colors.yellow
        else:
            color = Colors.white
        gate_data = handler.render_gate(gate_data[0], gate_data[1], ["calculation_placeholder"],(circuit_x + circuit_dx,circuit_y + circuit_dy), i+1, color)
        gates_on_circuit.append(gate_data) # <---------- made active gates change

    # Draw drag bar
    if drag_bar_y > screen.get_height() - 70: # TODO Replace with drag_bar_height for more natural resizing
        drag_bar_y = screen.get_height() - 70
    pygame.draw.rect(screen, drag_bar_color, (0, drag_bar_y, screen.get_width(), drag_bar_height))
    # Draw options panel
    # Update positions
    tab_panel.y = drag_bar_y + drag_bar_height
    tab_panel.draw()
    bloch_sphere.y = tab_panel.y + tab_panel.height
    # Draws background of panel window (hides circuit)
    pygame.draw.rect(screen, Colors.black, (0, tab_panel.y+tab_panel.height, screen.get_width(), screen.get_height()-tab_panel.y-tab_panel.height))
    calculation_window.y = tab_panel.y + tab_panel.height
    calculation_window.circuit_dx = circuit_dx
    calculation_window.systems = circuit.systems # update states

    # Draw navigation window with run and step buttons
    circuit_navigation_panel.draw()

    # Draw selected screen
    option = tab_panel.get_selected()
    if option == "Logic gates": # TODO Use enum/ atoms instead of strings
        MenuButton.renderButton([gateButtons], drag_bar_y + 20)
        MenuButton.check_moving_gate(gateButtons, gateList, circuit_x, circuit_y, circuit_dx, circuit_dy)  # gate placement
    elif option == "Math view":
        # Implement math view renderer here
        calculation_window.draw()
    elif option == "Text view":
        pass # TODO implement text view here
    elif option == "Bloch sphere":
        bloch_sphere.draw()
        pass # Implement Bloch sphere render here
    # ---------------------------------------------------------------

    # Mouse input
    Mouse.update(Mouse)
    # Update cursor + temporary colors
    if Mouse.status == None and Mouse.y > drag_bar_y and Mouse.y < drag_bar_y + drag_bar_height:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS) # Set mouse cursor to "resize"-image
        drag_bar_color = Colors.yellow
    elif Mouse.status == "Panning":
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow) # Reset mouse image
        drag_bar_color = Colors.white

    # Left click
    if Mouse.l_click:
        # Check for tabs here
        tab_panel.click(Mouse.x, Mouse.y)
        if Mouse.y > drag_bar_y and Mouse.y < drag_bar_y + drag_bar_height:
            Mouse.status = "Resizing bottom panel"
        elif Mouse.y < circuit_navigation_panel.y+circuit_navigation_panel.height:
            circuit_navigation_panel.click(Mouse.x, Mouse.y)
        elif Mouse.y > circuit_navigation_panel.y+circuit_navigation_panel.height and Mouse.y < drag_bar_y: # <------ use this check
            Mouse.status = "Panning"
        elif Mouse.y > drag_bar_y + drag_bar_height + tab_panel.height:
            # Below panel selector
            # Bloch sphere
            if tab_panel.get_selected()=="Bloch sphere":
                Mouse.status = "Panning sphere"
    # Left mouse is being held down
    elif Mouse.l_held:
        # Below is interaction for the reizeable panel at the bottom
        if Mouse.status == "Resizing bottom panel":
            drag_bar_y = Mouse.y # Move UI
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS) # Set mouse cursor to "resize"-image
            drag_bar_color = Colors.yellow
        # Drag circuit
        elif Mouse.status == "Panning":
            circuit_dx += Mouse.dx
            circuit_dy += Mouse.dy
        # Rotate Bloch sphere
        elif Mouse.status == "Panning sphere":
            bloch_sphere.pan(Mouse)

    # Dragging gates logic
    offset_x = circuit_x + circuit_dx
    offset_y = circuit_y + circuit_dy
    if Mouse.r_click:
        # Find gate we're dragging
        for i,gate_data in enumerate(gateList):
            rect = gates.gatelist_gate_to_rect(gate_text=gate_data[0], gate_index_in_list=i, operating_qubit=gate_data[1][0], offset_x = circuit_x + circuit_dx, offset_y = circuit_y + circuit_dy)
            if rect.collidepoint(Mouse.x, Mouse.y):
                Mouse.holding = copy.deepcopy(gate_data)
                Mouse.status = "Moving gate"
                gateList.remove(gate_data)
                print("clicked gate")
                break
    elif Mouse.r_held and Mouse.status == "Moving gate":
        # Draw gate
        grid_x = floor((Mouse.x - offset_x) / UI.grid_size) * UI.grid_size + offset_x
        grid_y = floor((Mouse.y - offset_y) / UI.grid_size) * UI.grid_size + offset_y
        pygame.draw.rect(screen, Colors.white, (grid_x, grid_y, UI.grid_size, UI.grid_size), width = 1)
        gate_data = Mouse.holding
        Gate.draw_gate(gate_data[0], Mouse.x,  Mouse.y, UI.gate_size, UI.gate_size, Colors.white)
    elif Mouse.holding != None:
        # Dropping gate
        gate_data = Mouse.holding
        col = (Mouse.x - circuit_x - circuit_dx) // UI.grid_size
        row = (Mouse.y - circuit_y - circuit_dy) // UI.grid_size
        # Move qubits to correct position
        qubits = gate_data[1]
        delta_row = row -gate_data[1][0]
        for i, qubit in enumerate(qubits):
            gate_data[1][i] = qubits[i] + delta_row
        # Where to place gate in list
        if col < len(gateList):
            # Insert into gatelist
            gateList.insert(col - 1, gate_data)
        else:
            # Add to end of gatelist
            gateList.append(gate_data)
        Mouse.holding = None
        Mouse.status = None



    # ---------------------------------------------------------------

    pygame.display.update()
    framerate.tick(30)
    
    
