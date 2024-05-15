from ast import If
from json import tool
import sys
import os
from math import floor
import copy
import re
import pygame
import json
# Change path (in order to import backend module)
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

# Custom modules
import screenHandler
import UI
import Utilities.Colors as Colors
import frontend.q_sphere as q_sphere
import Fields.MenuButton as MenuGateButton
import Fields.calculation_view_window as calculation_view_window
import Fields.qubit_name_panel as qubit_name_panel
from backend.circuit import Circuit
from backend.Gates import string_to_gate 
import backend.algorithms as algorithms # This is used to quickly set starting circuit state
from frontend.Fields.circuit_navigation_panel import Circuit_Navigation_Window
import gates
from gates import Gate, gateHandler
from Utilities.mouse import Mouse
import Fields.TextInput as input_box
import Fields.gate_date_visualizer as gate_data_visualizer
from tkinter.filedialog import asksaveasfile, askopenfile
from time import time
import numpy as np
screen = screenHandler.screen
gate_handler : gateHandler = gateHandler()
framerate = pygame.time.Clock()

# positioning of circuit
circuit_x = 75
circuit_y = 75
circuit_dx = 0
circuit_dy = 0

# The seperator between upper and lower screen
drag_bar_y = screen.get_height() - 100 
drag_bar_color = Colors.white
drag_bar_height = 15 # Height of draggable bar TODO make this into a reuseable class

resize_tab_panel: UI.ChoicePanel = UI.ChoicePanel(screen, pygame.display, drag_bar_y + drag_bar_height, ["Logic gates","State Viewer","Text Editor","Q-sphere"])
resize_tab_panel.set_icons([pygame.image.load("frontend/images/icons/gate-icon.png"), pygame.image.load("frontend/images/icons/state-view-icon.png"), pygame.image.load("frontend/images/icons/text-edit-icon.png"), pygame.image.load("frontend/images/icons/q-sphere-icon.png")]) # Set icons for the different options

#tool_panel.set_icons([pygame.image.load("frontend/images/icons/gate-icon.png"), pygame.image.load("frontend/images/icons/state-view-icon.png"), pygame.image.load("frontend/images/icons/text-edit-icon.png"), pygame.image.load("frontend/images/icons/q-sphere-icon.png")])
#(0, circuit_navigation_panel.y + circuit_navigation_panel.height, screen.get_width(), tool_panel.y)

q_sphere = q_sphere.Q_Sphere(screen, 0, drag_bar_y + 40, screen.get_width(), screen.get_height() - drag_bar_height)

# Calculation window (generate example circuit) Comment out to load different presets
# circuit : Circuit = Circuit([["A","B","C"],"Ry(np.pi/4) 0","H 1","CNOT 1 2","CNOT 0 1","H 0", "measure 0", "measure 1", "X 1 2", "Z 0 2"]) # Quantum teleportation
# circuit : Circuit = Circuit([["A","B","C","D","E","F","G"], "CU 4 5", "CUSTOM 2 3", "CUSTOM 0 1 2 3 4", "CUSTOM 2 3 5", "CUSTOM 1 3 5"])
# circuit : qusim_class.Circuit = qusim_class.Circuit([["A","B","C"],"H 1","CNOT 1 2","CNOT 0 1","H 0", "measure 0", "measure 1", "X 2 1", "Z 2 0"])
# circuit : qusim_class.Circuit = qusim_class.Circuit([["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P"],"CNOT 0 1","CNOT 1 2","CNOT 2 3","CNOT 3 4","CNOT 4 5","CNOT 5 6","CNOT 6 7","CNOT 7 8","CNOT 8 9","CNOT 9 10","CNOT 10 11","CNOT 11 12","CNOT 12 13","CNOT 13 14","CNOT 14 15"])
circuit : Circuit = Circuit(algorithms.shor_subroutine_circuit(7,15))
# circuit : Circuit = Circuit(algorithms.grover(3,0b010))
# circuit : Circuit = Circuit(algorithms.grover_2_qubits(0b01))
# circuit : Circuit = Circuit(algorithms.grover(5, [0b11010], iterations=4))
# circuit : Circuit = Circuit([["q0","q1","q2","q3","q4","q5"],"gen_I(3) 3 5 4","gen_I(3) 1 4 5","gen_I(3) 5 3 4"])

calculation_window = calculation_view_window.Calculation_Viewer_Window(screen, 0, resize_tab_panel.y + resize_tab_panel.height, screen.get_width(), screen.get_height() - (resize_tab_panel.y + resize_tab_panel.height), circuit.systems)

circuit_navigation_panel : Circuit_Navigation_Window = Circuit_Navigation_Window(screen, pygame.display, 0, 0, circuit)

tool_panel: UI.ChoicePanel = UI.ChoicePanel(screen, pygame.display, circuit_navigation_panel.y + circuit_navigation_panel.height, ["Drag qubit","Drag gate","Select multiple","Add qubit"])
tool_panel.set_icons([pygame.image.load("frontend/images/icons/move-gate-icon.png"), pygame.image.load("frontend/images/icons/move-qubit-icon.png"), pygame.image.load("frontend/images/icons/select-gates-icon.png"), pygame.image.load("frontend/images/icons/select-gates-icon.png")]) # Set icons for the different options

qubit_name_panel = qubit_name_panel.Qubit_Name_Panel(screen, pygame.display, circuit_navigation_panel.y + circuit_navigation_panel.height, circuit.systems[0].qubits, circuit_dy)
  


gateList = circuit.as_frontend_gate_list()
circuit_x = qubit_name_panel.width # Qubit label width
circuit_y = 75
buttons_text = ["UPDATE", "SUBMIT", "IMPORT", "EXPORT"]


# gate_option_str_list = ["H", "X", "Y", "Z", "I", "S", "T", "CNOT"]
gate_option_list = [("H", [0]), ("X", [0]), ("Y", [0]), ("Z", [0]), ("I", [0]), ("S", [0]), ("T", [0]), ("CNOT", [0, 1]), ("Ry(np.pi/4)", [0]), ("Toffoli", [0,1,2]), ("SWAP", [0, 1])]
menu_buttons = MenuGateButton.createGateButtons(gate_option_list, 40, 40)
gates_cleaned = re.findall(r"\((.+?)\)", str(gateList))
circuit_string = [str(circuit.description[0])] + circuit.description[1:]
text_box = input_box.input_box(screen, 0, drag_bar_y + 60, screen.get_width(), 50, circuit_string) 
buttons_options = input_box.Button(screen, Colors.black, Colors.selected, buttons_text, text_box)

sizeQ = 40 # Zoom level

# Draws the circuit gates
def draw_circuit(handler, circuit_x, circuit_y, circuit_dx, circuit_dy, circuit, gateList, gates_on_circuit):
    # Find indices of visible gates so we dont render anything out of view
    start_index = -int(circuit_dx/UI.grid_size) - 1
    if start_index<0:
        start_index=0
    end_index   = int((-circuit_dx+screen.get_width())/UI.grid_size) - 1
    # print(end_index)
    for i in range(start_index, min(len(gateList), end_index)): # We truncate our ending position so we dont go out of bounds
        gate_data = gateList[i]
        selected = i<=circuit.position-1
        value = None # Value to show on gate     
        if selected: # Change color for gates already having been applied
            color = Colors.yellow
            if gate_data[0]=="measure":
                value = circuit.systems[i+1].get_qubit(int(gate_data[1][0])) # Load qubit data
        else:
            color = Colors.white
        gate_data = handler.render_gate(gate_data[0], gate_data[1], value,(circuit_x + circuit_dx,circuit_y + circuit_dy), i+1, color, selected)
        gates_on_circuit.append(gate_data)

def drag_qubits_on_circuit(screen, circuit_x, circuit_y, circuit_dx, circuit_dy, drag_bar_y, gateList):
    offset_x = circuit_x + circuit_dx
    offset_y = circuit_y + circuit_dy
    
    if Mouse.r_click:
        # Find qubit we're dragging
        if Mouse.status==None:
            col = (Mouse.x - offset_x) // UI.grid_size
            row = (Mouse.y - offset_y) // UI.grid_size
            if -1 < col-1 < len(gateList):
              gate_data = gateList[col-1]
              print(gate_data[0])
              qubits = gate_data[1]
              for qubit_index in range(0, len(qubits)):
                  if row==qubits[qubit_index]:
                      Mouse.holding = (col, qubit_index)
                      Mouse.status = "Holding qubit"
                      print(f"Holding qubit{qubits[qubit_index]}")
                      break
   
    elif Mouse.r_held and Mouse.status == "Holding qubit":
        qubit_row = (Mouse.y - offset_y) // UI.grid_size
        # Mouse.holding is a tuple (col, qubit_index)
        # Check if gateList location is occupied
        col = Mouse.holding[0]-1
        occupied_qubits = gateList[col][1]
        if qubit_row not in occupied_qubits:
            # Reminder gateList is formatted like this: column, [gate, qubits: []]
            gateList[col][1][Mouse.holding[1]] = qubit_row # TODO Change row of qubit by swapping?
    # Qubits have already been placed so we just remove it from mouse  TODO Shift qubit at location
    elif Mouse.status == "Holding qubit":
        Mouse.holding = None
        Mouse.status = None

def drag_gates_on_circuit(screen, circuit_x, circuit_y, circuit_dx, circuit_dy, drag_bar_y, gateList):
    offset_x = circuit_x + circuit_dx
    offset_y = circuit_y + circuit_dy
    
    if Mouse.r_click:
        # Find gate we're clicking on
        for i, gate_data in enumerate(gateList):
            rect = gates.gatelist_gate_to_rect(gate_text=gate_data[0], gate_index_in_list=i, operating_qubit=gate_data[1][0], offset_x = circuit_x + circuit_dx, offset_y = circuit_y + circuit_dy)
            if rect.collidepoint(Mouse.x, Mouse.y):
                Mouse.holding = copy.deepcopy(gate_data)
                Mouse.status = "Moving gate"
                # gateList.remove(gate_data) # Remove gate from list so we can see where we're moving it
                gateList.pop(i)
                print("clicked gate")
                window = gate_data_visualizer.Matrix_Window(string_to_gate(gate_data[0]))
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
            grid_y -= (max(qubits) - min(qubits)) * UI.grid_size # Calculate rectangle height
        delta_qubit_index = max(qubits) - min(qubits) # Find height of qubits
        highlight_height = (delta_qubit_index + 1) * UI.grid_size# The height of the highlighter square
        gate_color = Colors.white
        if Mouse.y < drag_bar_y:
            rect = pygame.draw.rect(screen, Colors.white, (grid_x, grid_y, UI.grid_size, highlight_height), width = 1)
        else:
            gate_color = Colors.red # Delete highlight
        rect = Gate.draw_gate(gate_data[0], Mouse.x,  Mouse.y, UI.gate_size, UI.gate_size, gate_color)
        pygame.display.update(rect)
        print("Drew Gate")
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
                print(gate_data)
                gateList.insert(col - 1, gate_data)
            else:
                # Add to end of gatelist
                gateList.append(gate_data)
        Mouse.holding = None
        Mouse.status = None


def select_multiple(screen, circuit_x, circuit_y, circuit_dx, circuit_dy, drag_bar_y, gateList):
    offset_x = circuit_x + circuit_dx
    offset_y = circuit_y + circuit_dy

    if Mouse.r_click:
        print(Mouse.point)
        Mouse.point = (Mouse.x, Mouse.y)
    
    #when selecting an area
    if Mouse.r_held and Mouse.status != "Moving multiple":
        print("r_held")
        Mouse.selection_rect = pygame.draw.rect(screen, Colors.white, (Mouse.point[0], Mouse.point[1], Mouse.x - Mouse.point[0], Mouse.y - Mouse.point[1]), width = 10)
        pygame.display.update(Mouse.selection_rect)
        Mouse.status = "Selecting"
        print(Mouse.selection_rect == None)
    
    #when letting go of the mouse button
    elif Mouse.status == "Selecting":
       temp = []
       for i, gate_data in enumerate(gateList):
            rect : pygame.Rect = gates.gatelist_gate_to_rect(gate_text=gate_data[0], gate_index_in_list=i, operating_qubit=gate_data[1][0], offset_x = circuit_x + circuit_dx, offset_y = circuit_y + circuit_dy)
            if rect.colliderect(Mouse.selection_rect) :
                Mouse.gates_to_move.append((i, gate_data))
                temp.append(i)
       Mouse.status = "Moving multiple"
       for i in range (len(temp)):
           gateList.pop(temp[0])
       print(len(Mouse.gates_to_move))
    
    
    if Mouse.r_click and Mouse.status == "Moving multiple":
        if Mouse.y < drag_bar_y and len(Mouse.gates_to_move) >= 1:
            col = (Mouse.x - circuit_x - circuit_dx) // UI.grid_size
            row = (Mouse.y - circuit_y - circuit_dy) // UI.grid_size
            
            #print(Mouse.gates_to_move)

            gateT = Mouse.gates_to_move[0]
            qubits = gateT[1][1]
            delta_row = row - qubits[0]
            
            # Move qubits to correct position
            for gate in Mouse.gates_to_move:
              print(gate)
              print(row)
              #gate = (original index, ("Name", []))
              #qubits = gate[1][1]
              #delta_row = row - qubits[0]
              
              print(delta_row)
              
              for i, qubit in enumerate(gate[1][1]):
                  gate[1][1][i] = gate[1][1][i] + delta_row 
                  
            # Where to place gates in list
            if col < len(gateList):
                for i in range(len(Mouse.gates_to_move)):
                  # Insert into gatelist
                  #print(Mouse.gates_to_move[i])
                  gateList.insert(col - 1 + i, Mouse.gates_to_move[i][1])
            else:
                # Add to end of gatelist
                for i in range(len(Mouse.gates_to_move)):
                  gateList.append(Mouse.gates_to_move[i])
                
        Mouse.status = None
        Mouse.gates_to_move = []
         
    elif Mouse.status == "Moving multiple":
        
        grid_x = floor((Mouse.x - offset_x) / UI.grid_size) * UI.grid_size + offset_x
        grid_y = floor((Mouse.y - offset_y) / UI.grid_size) * UI.grid_size + offset_y
        
        i = 0
        for gate in Mouse.gates_to_move:
            rect = Gate.draw_gate(gate[1][0], Mouse.x + (i * UI.grid_size),  Mouse.y + (i * UI.grid_size), UI.gate_size, UI.gate_size, Colors.red)
            pygame.display.update(rect)
            qubits = gate[1][1]        
            if qubits[0] != min(qubits):
                print (qubits[0])
                grid_y -= (max(qubits) - min(qubits)) * UI.grid_size 
            delta_qubit_index = max(qubits) - min(qubits) 
            highlight_height = (delta_qubit_index + 1) * UI.grid_size
            gate_color = Colors.white
            if Mouse.y < drag_bar_y:
                rect = pygame.draw.rect(screen, Colors.white, (grid_x + (i * UI.grid_size) , grid_y + (i * UI.grid_size), UI.grid_size, highlight_height), width = 1)
                pygame.display.update(rect) 
            i = i + 1  


# Game loop
while True:
    Mouse.update(Mouse)
    # Clear screen
    # screen.fill((0,0,0))
    pygame_event = pygame.event.get() # This removes all events from stack
    redraw_screen = True
    if len(pygame_event) > 0: # Check if anything has happened since last frame
        redraw_screen = True
    for event in pygame_event:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEWHEEL: # Zooming circuit view
            if option == "Text Editor":
                pass
            else:
                zoom_factor = 5 * event.y
                # Check if zooming out is allowed
                if UI.grid_size >= 50 or event.y > 0:
                    UI.grid_size += zoom_factor
                    UI.gate_size += zoom_factor
                    gate_handler.adjust += zoom_factor
                    screenHandler.offsetMod += zoom_factor
                    sizeQ += 2 * event.y
                    qubit_name_panel.changed = True

    # Update circuit behind the scenes
    circuit.set_circuit_from_frontend_gate_list(gateList)
    print("New loop")
    # Gates placed on the circuit (used for collision detection. is reset every frame)
    gates_on_circuit = []
    # Draw circuit view
    rect = pygame.draw.rect(screen, Colors.black, (qubit_name_panel.width, tool_panel.y + tool_panel.height, screen.get_width() - qubit_name_panel.width, (drag_bar_y + drag_bar_height/2) - (tool_panel.y + tool_panel.height)))    # Draw a line to show where user has stepped to TODO make it dotted
    screenHandler.draw_horizontal_qubit_lines(len(circuit.systems[0].qubits), qubit_name_panel.width, circuit_y + circuit_dy, screen.get_width(), Colors.qubit_line) # Draws horisontal lines for qubits
    # Draw example circuit
    pygame.draw.line(screen, Colors.yellow, (circuit.position * UI.grid_size + UI.grid_size/2 + circuit_x + circuit_dx, tool_panel.y + tool_panel.height), (circuit.position * UI.grid_size + UI.grid_size/2 + circuit_x + circuit_dx, screen.get_height()), width = 2)
    draw_circuit(gate_handler, circuit_x, circuit_y, circuit_dx, circuit_dy, circuit, gateList, gates_on_circuit)
    # Dragging gates logic
    if tool_panel.get_selected() == "Drag qubit":
        drag_qubits_on_circuit(screen, circuit_x, circuit_y, circuit_dx, circuit_dy, drag_bar_y, gateList)
    elif tool_panel.get_selected() == "Drag gate":
        drag_gates_on_circuit(screen, circuit_x, circuit_y, circuit_dx, circuit_dy, drag_bar_y, gateList)
    elif tool_panel.get_selected() == "Select multiple":
        select_multiple(screen, circuit_x, circuit_y, circuit_dx, circuit_dy, drag_bar_y, gateList)
    elif tool_panel.get_selected() == "Add qubit":
        circuit.description[0].append(str(len(circuit.description[0])))
        tool_panel.selected = 0
    pygame.display.update(rect)
    # Draw qubit names on left side
    qubit_name_panel.set_rectangle((0, tool_panel.y + tool_panel.height, 90, drag_bar_y - (tool_panel.y + tool_panel.height)))    
    qubit_name_panel.set_offset_y(circuit_y + circuit_dy)
    qubit_name_panel.draw()
    
    if drag_bar_y > screen.get_height() - 70: # TODO Replace with drag_bar_height for more natural resizing
        drag_bar_y = screen.get_height() - 70
    resize_tab_panel.set_rectangle((0, drag_bar_y + drag_bar_height, screen.get_width(), resize_tab_panel.height))
    tool_panel.set_rectangle((0, circuit_navigation_panel.y + circuit_navigation_panel.height, screen.get_width(), tool_panel.y))

    

    # Draw options panel
    # Update positions
    
    # Draws background of panel window (hides circuit)
    rect = pygame.draw.rect(screen, Colors.black, (0, resize_tab_panel.y + resize_tab_panel.height, screen.get_width(), screen.get_height() - resize_tab_panel.y - resize_tab_panel.height))
    # Draw selected screen
    option = resize_tab_panel.get_selected()
    if option == "Logic gates": # TODO Use enum/ atoms instead of strings
        MenuGateButton.renderButton([menu_buttons], drag_bar_y + 20)
    elif option == "State Viewer":
        # Update calculation window
        calculation_window.y = resize_tab_panel.y + resize_tab_panel.height
        calculation_window.circuit_dx = circuit_x + circuit_dx
        calculation_window.systems = circuit.systems # update states
        calculation_window.draw()
    elif option == "Text Editor":
        buttons_options.update(screen.get_width(), resize_tab_panel.y + resize_tab_panel.height)
        pressed_keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        text_box.handle_event(pygame_event, pressed_keys, mouse_x, mouse_y, mouse_pressed)
        text_box.update(resize_tab_panel.y, resize_tab_panel.height)
        buttons_options.draw()
        gates_cleaned = re.findall(r"\((.+?)\)", str(gateList))
        test = buttons_options.handle_event(mouse_x, mouse_y, mouse_pressed, gates_cleaned)
        match test:
            case "SUBMIT":
                # Verify gates here
                # Update our gates if no errors
                description_string_list = text_box.get_text_as_string_list()
                text_box.valid_lines = circuit.verify_description_string_list(description_string_list)
                if False in text_box.valid_lines:
                    message = "Wrong Syntax, please enter the correct syntax"
                    x = int(screen.get_width())
                    y = int(screen.get_height())
                    input_box.popupmsg(msg = message, x=x, y=y)
                    print(f"Error at line {text_box.valid_lines.index(False)}")
                else:
                    qubits = eval(description_string_list[0])
                    circuit.description = [qubits] + description_string_list[1:]
                    gateList = circuit.as_frontend_gate_list()
                    qubit_name_panel.qubits_list = qubits

            case "EXPORT":
                    file_path = asksaveasfile(initialfile='Untitled.txt',
                                      defaultextension=".txt", filetypes=[("Text Documents", "*.txt")])
                    try:
                        if file_path:
                            file_path.writelines(text_box.text)
                            file_path.close()
                    except Exception as e:
                        print(f"An error occurred: {e}")
            case "IMPORT":
                file_path = askopenfile(mode ='r',filetypes=[("Text Documents", "*.txt")])
                try:
                    if file_path:
                        file_content = file_path.read()
                        text_box.set_text_from_string(file_content)
                        description_string_list = text_box.text.split('\n')
                        qubits = eval(description_string_list[0])
                        circuit.description = [qubits] + description_string_list[1:]
                        gateList = circuit.as_frontend_gate_list()
                        qubit_name_panel.qubits_list = qubits
                        pass
                except Exception as e:
                    print(f"An error occurred: {e}")
    elif option == "Q-sphere":
        # Updates and draws q-sphere
        q_sphere.y = resize_tab_panel.y + resize_tab_panel.height
        single_register = circuit.single_register()
        q_sphere.set_register(single_register)
        q_sphere.draw()
    pygame.display.update(rect)

    # Draw drag bar
    if drag_bar_color==Colors.yellow:
        # Big drag bar
        pygame.draw.rect(screen, drag_bar_color, (0, drag_bar_y, screen.get_width(), drag_bar_height)) # Drag bar
        pygame.display.update((0, drag_bar_y, screen.get_width(), drag_bar_height))
    else:
        # Visually less prominent drag bar when not hovering
        pygame.draw.rect(screen, drag_bar_color, (0, drag_bar_y+drag_bar_height//2, screen.get_width(), drag_bar_height//2+1)) # Drag bar
        pygame.display.update((0, drag_bar_y, screen.get_width(), drag_bar_height))

    resize_tab_panel.draw() # Tab panel options
    tool_panel.draw()

    # Draw toolbar with run and step buttons
    circuit_navigation_panel.draw()
    # ---------------------------------------------------------------

    # Mouse themeing based on status
    # Update cursor + temporary colors
    if Mouse.status == None and Mouse.y > drag_bar_y and Mouse.y < drag_bar_y + drag_bar_height:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS) # Set mouse cursor to "resize"-image
        drag_bar_color = Colors.yellow
    elif Mouse.status == "Panning":
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
    elif Mouse.status == "Moving gate":
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # Reset mouse image
        drag_bar_color = Colors.white
    circuit_navigation_panel.update(Mouse)
    # Left click
    resize_tab_panel.hover(Mouse.x, Mouse.y)
    tool_panel.hover(Mouse.x, Mouse.y)
    if Mouse.l_click:
        # Check for tabs here
        resize_tab_panel.click(Mouse.x, Mouse.y)
        tool_panel.click(Mouse.x, Mouse.y)
        if Mouse.y > drag_bar_y and Mouse.y < drag_bar_y + drag_bar_height:
            Mouse.status = "Resizing bottom panel"
        elif Mouse.y < circuit_navigation_panel.y+circuit_navigation_panel.height:
            pass
            # circuit_navigation_window.click(Mouse.x, Mouse.y)
        elif Mouse.y > circuit_navigation_panel.y+circuit_navigation_panel.height and Mouse.y < drag_bar_y:
            Mouse.status = "Panning"
        elif Mouse.y > drag_bar_y + drag_bar_height + resize_tab_panel.height:
            # Below panel selector
            # Q-sphere
            if resize_tab_panel.get_selected()=="Q-sphere":
                Mouse.status = "Panning sphere"
            elif resize_tab_panel.get_selected()=="State Viewer":
                Mouse.status = "Panning state view"
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
        elif Mouse.status == "Panning state view":
            circuit_dx += Mouse.dx
            calculation_window.offset_y += Mouse.dy
            if circuit_dx>0:
                circuit_dx=0
            if calculation_window.offset_y>0:
                calculation_window.offset_y = 0
        # Rotate Q-sphere
        elif Mouse.status == "Panning sphere":
            q_sphere.pan(Mouse)
    elif not (Mouse.l_held or Mouse.l_click) and (Mouse.status=="Panning" or Mouse.status=="Resizing bottom panel" or Mouse.status=="Resizing bottom panel"):
        Mouse.status = None

    
    # Draw everything here
    if redraw_screen:
        # pygame.display.update()
        pass

    framerate.tick(60)


# --------------------------------------------------------
# Update methods
