import sys
import os
from math import floor
import copy
import re
import pygame

# Change path (in order to import backend module)
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

# Custom modules
import UI
import Utilities.Colors as Colors
import bloch_sphere
import Fields.MenuButton as MenuButton
import Fields.calculation_view_window as calculation_view_window
import Fields.qubit_name_panel as qubit_name_panel
from backend import qusim_class
from Fields.circuit_navigation_window import Circuit_Navigation_Window
import gates
from gates import Gate, gateHandler
from Utilities.mouse import Mouse
import Fields.TextInput as input_box
import screenHandler

screen = screenHandler.screen

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
circuit_dx = 0
circuit_dy = 0
# Tag meny: menyns höjd variabel 
# textCanvasY =  pygame.display.Info().current_h - 100 #920

drag_bar_y = screen.get_height() - 100
drag_bar_color = Colors.white
drag_bar_height = 15 # Height of draggable bar TODO make this into a reuseable class

tab_panel = UI.ChoicePanel(screen, drag_bar_y + drag_bar_height, ["Logic gates","Math view","Text view","Bloch sphere"])
tab_panel.set_icons([pygame.image.load("frontend/images/icons/gate-icon.png"), pygame.image.load("frontend/images/icons/state-view-icon.png"), pygame.image.load("frontend/images/icons/text-edit-icon.png"), pygame.image.load("frontend/images/icons/q-sphere-icon.png")]) # Set icons for the different options

bloch_sphere = bloch_sphere.Bloch_Sphere(screen, 0, drag_bar_y + 40, screen.get_width(), screen.get_height() - drag_bar_height)
bloch_sphere.add_random_point_on_unit_sphere()
bloch_sphere.add_random_point_on_unit_sphere()

# Calculation window (generate example circuit)
circuit : qusim_class.Circuit = qusim_class.Circuit([["A","B","C"],"Ry(np.pi/4) 0","H 1","CNOT 1 2","CNOT 0 1","H 0", "measure 0", "measure 1", "X 2 1", "Z 2 0"])
# circuit : qusim_class.Circuit = qusim_class.Circuit([["A","B","C"],"H 1","CNOT 1 2","CNOT 0 1","H 0", "measure 0", "measure 1", "X 2 1", "Z 2 0"])
# circuit : qusim_class.Circuit = qusim_class.Circuit([["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P"],"CNOT 0 1","CNOT 1 2","CNOT 2 3","CNOT 3 4","CNOT 4 5","CNOT 5 6","CNOT 6 7","CNOT 7 8","CNOT 8 9","CNOT 9 10","CNOT 10 11","CNOT 11 12","CNOT 12 13","CNOT 13 14","CNOT 14 15"])
# circuit : qusim_class.Circuit = qusim_class.Circuit([["A","B"],"H 0","CNOT 1 0","CNOT 1 0","CNOT 0 1"])

calculation_window = calculation_view_window.Calculation_Viewer_Window(screen, 0, tab_panel.y + tab_panel.height, screen.get_width(), screen.get_height() - (tab_panel.y + tab_panel.height), circuit.systems)

circuit_navigation_window = Circuit_Navigation_Window(screen, 0, 0, circuit)

qubit_name_panel = qubit_name_panel.Qubit_Name_Panel(screen, circuit_navigation_window.y + circuit_navigation_window.height, circuit.systems[0].qubits, circuit_dy)

displayCalc = False
dragging = False

# name of selected gate
dragging2 = False
coordinates = []

gateBoxHit = False
gateButton = False
        
gateList = circuit.as_frontend_gate_list()
circuit_x = qubit_name_panel.width # Qubit label width
circuit_y = 75

# gate_option_str_list = ["H", "X", "Y", "Z", "I", "S", "T", "CNOT"]
gate_option_list = [("H", [0]), ("X", [0]), ("Y", [0]), ("Z", [0]), ("I", [0]), ("S", [0]), ("T", [0]), ("CNOT", [1, 0]), ("Ry(np.pi/4)", [0]), ("Toffoli", [2,1,0]), ("Swap", [1, 0])]
menu_buttons = MenuButton.createGateButtons(gate_option_list, 40, 40)
gates_cleaned = re.findall(r"\((.+?)\)", str(gateList))
input_boxes = input_box.input_box(screen, 0, drag_bar_y + 60, screen.get_width(), 50, gates_cleaned) 

# keep track of shifting
moving_gate = False

# the gate being shifted
selectedGate = None

sizeQ = 40

while True:
    screen.fill((0,0,0))
    pygame_event = pygame.event.get() # This removes all events from stack
    redraw_screen = False
    if len(pygame_event) > 0: # Check if anything has happened since last frame
        redraw_screen = True
    for event in pygame_event:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEWHEEL:
            UI.grid_size += (5 * event.y) 
            UI.gate_size += (5 * event.y)
            handler.adjust += (5 * event.y) 
            screenHandler.offsetMod += (5 * event.y)  
            sizeQ += (2 * event.y) 
            qubit_name_panel.title_font = pygame.font.Font(None, sizeQ)
            qubit_name_panel.state_font = pygame.font.Font(None, 20)

    # Clear screen
    screen.fill((0,0,0))
    # Update circuit behind the scenes TODO support additional qubits/ removal of qubits
    circuit.set_circuit_from_frontend_gate_list(gateList)

    # Draw a line to show where user has stepped to TODO make it dotted
    pygame.draw.line(screen, Colors.yellow, (circuit.position * UI.grid_size + UI.grid_size/2 + circuit_x + circuit_dx, 0), (circuit.position * UI.grid_size + UI.grid_size/2 + circuit_x + circuit_dx, screen.get_height()))
    # Gates placed on the circuit (used for collision detection, resets every frame)
    gates_on_circuit = []
    # Draw circuit view
    screenHandler.draw_horizontal_qubit_lines(len(circuit.systems[0].qubits), circuit_x + circuit_dx, circuit_y + circuit_dy, pygame.display.Info().current_w, Colors.qubit_line) # Draws horisontal lines for qubits
    # Draw example circuit
    for i in range(0,len(gateList)):
        gate_data = gateList[i]      
        if i==circuit.position-1:
            color = Colors.yellow
        else:
            color = Colors.white
        gate_data = handler.render_gate(gate_data[0], gate_data[1], ["calculation_placeholder"],(circuit_x + circuit_dx,circuit_y + circuit_dy), i+1, color)
        gates_on_circuit.append(gate_data) # <---------- made active gates change
    
    # Draw qubit names on left side
    qubit_name_panel.offset_y = circuit_y + circuit_dy
    qubit_name_panel.draw()

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
    calculation_window.circuit_dx = circuit_x + circuit_dx
    calculation_window.systems = circuit.systems # update states

    # Draw window with run and step buttons
    circuit_navigation_window.draw()

    # Draw selected screen
    option = tab_panel.get_selected()
    if option == "Logic gates": # TODO Use enum/ atoms instead of strings
        MenuButton.renderButton([menu_buttons], drag_bar_y + 20)
    elif option == "Math view":
        # Implement math view renderer here
        calculation_window.draw()
    elif option == "Text view":
        pressed_keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        input_boxes.handle_event(pygame_event, pressed_keys, mouse_x, mouse_y, mouse_pressed)
        input_boxes.update(tab_panel.y, tab_panel.height)

    elif option == "Bloch sphere":
        # update bloch_sphere
        single_register = circuit.single_register()
        bloch_sphere.set_register(single_register)
        bloch_sphere.draw()
    # ---------------------------------------------------------------

    # Mouse themeing based on status
    Mouse.update(Mouse)
    # Update cursor + temporary colors
    if Mouse.status == None and Mouse.y > drag_bar_y and Mouse.y < drag_bar_y + drag_bar_height:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS) # Set mouse cursor to "resize"-image
        drag_bar_color = Colors.yellow
    elif Mouse.status == "Panning":
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
    elif Mouse.status == "Moving gate":
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
    else:
        pygame.mouse.set_cursor(pygame.cursors.arrow) # Reset mouse image
        drag_bar_color = Colors.white

    # Left click
    if Mouse.l_click:
        # Check for tabs here
        tab_panel.click(Mouse.x, Mouse.y)
        if Mouse.y > drag_bar_y and Mouse.y < drag_bar_y + drag_bar_height:
            Mouse.status = "Resizing bottom panel"
        elif Mouse.y < circuit_navigation_window.y+circuit_navigation_window.height:
            circuit_navigation_window.click(Mouse.x, Mouse.y)
        elif Mouse.y > circuit_navigation_window.y+circuit_navigation_window.height and Mouse.y < drag_bar_y:
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
            if circuit_dx>0:
                circuit_dx=0
            if circuit_dy>0:
                circuit_dy=0
        # Rotate Bloch sphere
        elif Mouse.status == "Panning sphere":
            bloch_sphere.pan(Mouse)
    elif not (Mouse.l_held or Mouse.l_click) and (Mouse.status=="Panning" or Mouse.status=="Resizing bottom panel" or Mouse.status=="Resizing bottom panel"):
        Mouse.status = None

    # Dragging gates logic
    offset_x = circuit_x + circuit_dx
    offset_y = circuit_y + circuit_dy
    if Mouse.r_click:
        # Find gate we're dragging
        for i, gate_data in enumerate(gateList):
            rect = gates.gatelist_gate_to_rect(gate_text=gate_data[0], gate_index_in_list=i, operating_qubit=gate_data[1][0], offset_x = circuit_x + circuit_dx, offset_y = circuit_y + circuit_dy)
            if rect.collidepoint(Mouse.x, Mouse.y):
                Mouse.holding = copy.deepcopy(gate_data)
                Mouse.status = "Moving gate"
                gateList.remove(gate_data) # Remove gate from list so we can see where we're moving it
                print("clicked gate")
                break
        if Mouse.status==None:
            # Find qubit to drag
            col = (Mouse.x - offset_x) // UI.grid_size
            row = (Mouse.y - offset_y) // UI.grid_size
            if -1 < col-1 < len(gateList):
              gate_data = gateList[col-1]
              print(gate_data[0])
              qubits = gate_data[1]
              for qubit_index in range(1, len(qubits)):
                  if row==qubits[qubit_index]:
                      Mouse.holding = (col, qubit_index)
                      Mouse.status = "Holding qubit"
                      print(f"Holding qubit{qubits[qubit_index]}")
                      break

    elif Mouse.r_held and Mouse.status == "Moving gate":
        # Draw gate
        grid_x = floor((Mouse.x - offset_x) / UI.grid_size) * UI.grid_size + offset_x
        grid_y = floor((Mouse.y - offset_y) / UI.grid_size) * UI.grid_size + offset_y
        # Draw highlight square for gate
        gate_data = Mouse.holding
        qubits = gate_data[1]
        if qubits[0] != min(qubits):
            print (qubits[0])
            grid_y -= (max(qubits) - min(qubits)) * UI.grid_size
        delta_qubit_index = max(qubits) - min(qubits) # Find height of qubits
        highlight_height = (delta_qubit_index + 1) * UI.grid_size# The height of the highlighter square
        gate_color = Colors.white
        if Mouse.y < drag_bar_y:
            pygame.draw.rect(screen, Colors.white, (grid_x, grid_y, UI.grid_size, highlight_height), width = 1)
        else:
            gate_color = Colors.red
        Gate.draw_gate(gate_data[0], Mouse.x,  Mouse.y, UI.gate_size, UI.gate_size, gate_color)
    elif Mouse.r_held and Mouse.status == "Holding qubit":
        qubit_row = (Mouse.y - offset_y) // UI.grid_size
        # Mouse.holding is a tuple (col, qubit_index)
        # Check if gateList location is occupied
        col = Mouse.holding[0]-1
        occupied_qubits = gateList[col][1]
        if qubit_row not in occupied_qubits:
            # Reminder gateList is formatted like this: column, [gate, qubits: []]
            gateList[col][1][Mouse.holding[1]] = qubit_row # TODO Change row of qubit by swapping?
    elif Mouse.status == "Holding qubit":
        # Qubits have already been placed so we just remove it from mouse  TODO Shift qubit at location
        Mouse.holding = None
        Mouse.status = None
    # Button release
    elif Mouse.holding != None and Mouse.status == "Moving gate":
        # Ensure dropping only allowed on panel
        if Mouse.y < drag_bar_y:
            # Dropping gate
            gate_data = Mouse.holding
            col = (Mouse.x - circuit_x - circuit_dx) // UI.grid_size
            row = (Mouse.y - circuit_y - circuit_dy) // UI.grid_size
            # Move qubits to correct position
            qubits = gate_data[1]
            delta_row = row - gate_data[1][0]
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
    
    if option=="Logic gates" and Mouse.status != "Moving gate":
        MenuButton.check_moving_gate(menu_buttons, gateList, circuit_x, circuit_y, circuit_dx, circuit_dy)  # gate placement

    # Draw everything here
    # TODO move this?
    if redraw_screen:
        pygame.display.update()

    framerate.tick(60)
