import pygame
import sys, os
import Utilities.Colors as Colors
import UI
import screenHandler

# Add frontend to path
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from gates import Gate
from Utilities.mouse import Mouse
from math import floor


class MenuButton:
    def __init__(self, name : str , width : int , height : int):
        self.gate = name
        self.width = width
        self.height = height
        self.selected = False
        self.gatefield = pygame.Rect(150, 150, 175, 175) 

    def update(self, gate, x : int, y : int):
        self.gatefield = Gate.draw_gate(gate[0], x, y, self.width, self.height, Colors.white)
        
    def checkClicked(self, mouse):
        if (self.gatefield.collidepoint(pygame.mouse.get_pos()) and (Mouse.r_click or Mouse.r_held)):
            self.selected = True

# Takes in a list of gates with qubit positions
def createGateButtons(gate_data_list : [], width : int, height : int):
    temp = []
    for gate_data in gate_data_list:
        temp.append(MenuButton(gate_data, width, height))
    return temp


def renderButton(buttonRows : [[MenuButton]], canvasYT : int ):
    xOffset = 75
    yOffset = 75
    for bRow in range (0, len(buttonRows)):
        for b in range (0, len(buttonRows[bRow])):
            button = buttonRows[bRow][b] # Is a MenuButton
            button.update(buttonRows[bRow][b].gate, 15 + xOffset * b, canvasYT + 50 + (bRow * yOffset))


def checkLines( x : int , y : int, xl, xr):
    withinLx = xl < x
    withinRx = x < xr
    withinX = withinLx and withinRx
    
    return withinX

# Cheks if user has clicked gate. Start moving gate.
def check_moving_gate(gateButtons : [[MenuButton]], gateList : [(str, [int])], x : int, y : int, circuit_dx : int, circuit_dy : int):
    # Calculate how much the cicuit view has shifted
    offset_x = x + circuit_dx
    offset_y = y + circuit_dy

    # Preview drop place
    grid_x = floor((Mouse.x - offset_x) / UI.grid_size) * UI.grid_size + offset_x
    grid_y = floor((Mouse.y - offset_y) / UI.grid_size) * UI.grid_size + offset_y

    # Iterate through buttons in panel
    for button in gateButtons:
        if button.selected and (Mouse.r_held or Mouse.r_click):
            # Show gate snapping position
            pygame.draw.rect(screenHandler.screen, Colors.white, (grid_x, grid_y, UI.grid_size, UI.grid_size), width = 1)
            # Show gate moving
            Gate.draw_gate(button.gate[0], Mouse.x,  Mouse.y, UI.gate_size, UI.gate_size, Colors.white)
            break
        elif button.selected and not (Mouse.r_click or Mouse.r_held):
            # Drop gate on circuit view
            # convert grid_x to index in gate list
            col = (Mouse.x - offset_x) // UI.grid_size
            row = (Mouse.y - offset_y) // UI.grid_size
            # transpose qubits to correct location
            gate_data = button.gate
            qubits = gate_data[1]
            delta_row = row -gate_data[1][0]
            for i, qubit in enumerate(qubits):
                gate_data[1][i] = qubits[i] + delta_row
            if col < len(gateList):
                # Insert into gatelist
                gateList.insert(col - 1, gate_data)
            else:
                # Add to end of gatelist
                gateList.append(gate_data) 
            button.selected = False
            break
        if not button.selected:
            button.checkClicked(Mouse)