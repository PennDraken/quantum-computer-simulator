import pygame
from enum import Enum
import Utilities.Colors as Colors
import screenHandler
import pygame
import UI

Loc = screenHandler.Loc
screen = screenHandler.screen

class Gate:
    def __init__(self, name : str , x : int , y : int , width : int , height : int):
        self.width = width
        self.height = height
        self.gate_text = name
        self.x = x
        self.y = y
    
    def draw_gate(gate_text : str, x: int, y: int, width : int, height : int, color):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, color,rect,0)
        # screen.blit(pygame.font.SysFont('Times New Roman', 10).render(gate, True, (170, 200, 200)), (xpos+4, ypos-3))
        text(gate_text, x+width/2, y+height/2, Colors.black, pygame.font.Font(None, 20))
        return rect
    
    def as_rect(self):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return rect
        
class gateHandler:
    xStart = 75
    yStart = 75
    gateWidth = UI.gate_size
    gateHeight = UI.gate_size
    step = 0
    
    def __init__(self):
        self.gateMap = {}
    
    def addGateCount(self, qubitIndex : int):
        if qubitIndex not in self.gateMap:
            self.gateMap[qubitIndex] = 1
        else:
            self.gateMap[qubitIndex] += 1  
            
    
    def setGateCount(self, qubitIndex : int, value : int):
        self.gateMap[qubitIndex] = value
       

    def getGateCount(self, key: int):
        return self.gateMap[key]

    # Renders a gate + lines for qubits
    def render_gate(self, gate_text : str, qubits, calculations : [str], offset_x_y_tuple : tuple, column, color): # integrating evenhandler for this method        
        nrQubits = len(qubits)
        if nrQubits < 1: # should be at least one qubit
            raise ValueError

        pygame.font.init()
        # Draws lines for connecting qubits
        if nrQubits > 1:
            for i in range(1, nrQubits):
                # Draw lines here to qubits connected to gate
                mid_x = UI.grid_size * column + UI.grid_size/2 + offset_x_y_tuple[0]
                y1 = qubits[i-1] * UI.grid_size + UI.grid_size/2 + offset_x_y_tuple[1] # Find midpoint of gate
                y2 = qubits[i] * UI.grid_size + UI.grid_size/2 + offset_x_y_tuple[1] # Find midpoint of second gate
                screenHandler.draw_qubit_line((mid_x, y1), (mid_x, y2), color)

            for i in range(1, nrQubits):
                # Draw connections here (dots)
                mid_x = UI.grid_size * column + UI.grid_size/2 + offset_x_y_tuple[0]
                y = qubits[i] * UI.grid_size + UI.grid_size/2 + offset_x_y_tuple[1]
                # need to change this
                screenHandler.drawQlineMod((mid_x, y), (mid_x, y), Loc.NONE, Loc.END_FILLED, color)

        # Draw the actual gate
        center_offset = (UI.grid_size - UI.gate_size)/2 # Used to draw gate at centre of grid
        x = UI.grid_size * column + center_offset + offset_x_y_tuple[0]
        y = qubits[0] * UI.grid_size + center_offset + offset_x_y_tuple[1] 
        gate = Gate(gate_text, x, y, self.gateWidth, self.gateHeight) # New gate object
        Gate.draw_gate(gate.gate_text, x, y, self.gateWidth, self.gateHeight, color) # Render gate
        return gate # for gate shifting

# This is a simple function that converts an element in gateList to a rect
# This is useful for collision detection etc
# Uses constants defined in UI to render gate
# This function is used in addGate, before adding the gate to the gateHandler class
def gatelist_gate_to_rect(gate_text : str, gate_index_in_list : int, operating_qubit : int, offset_x : int, offset_y : int)->pygame.rect:
    # Find location of upper left corner in underlying grid
    grid_x = (gate_index_in_list + 1) * UI.grid_size + offset_x
    grid_y = operating_qubit * UI.grid_size + offset_y
    # Center rect on the grid location
    offset = (UI.grid_size - UI.gate_size)/2
    x = grid_x + offset
    y = grid_y + offset
    # Return found rect
    return pygame.Rect(x, y, UI.gate_size, UI.gate_size)


# Draws centered text on screen
def text(string, x, y, color, font):
    text_color = pygame.Color(color)
    text_surface = font.render(string, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
       