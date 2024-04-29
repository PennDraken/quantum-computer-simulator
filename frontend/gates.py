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
    
    # Draws a gate at position rect
    def draw_gate(gate_text : str, x: int, y: int, width : int, height : int, color):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, color,rect,0)
        # screen.blit(pygame.font.SysFont('Times New Roman', 10).render(gate, True, (170, 200, 200)), (xpos+4, ypos-3))
        if len(gate_text)==1:
            font_size = 40
        else:
            font_size = 20
        text(gate_text, x+width/2, y+height/2, Colors.black, pygame.font.Font(None, font_size))
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
    
    #alignmentValue = 35
    #adjustedDistance = (self.gateHeight / 3)
    adjust = 0

    # Renders a gate + lines for qubits
    def render_gate(self, gate_text : str, qubits, input_data, offset_x_y_tuple : tuple, column, color, selected=False): # integrating evenhandler for this method
        # First check if label TODO maybe move this somewhere else?
        if (gate_text=="label"):
            mid_x = UI.grid_size * column + UI.grid_size/2 + offset_x_y_tuple[0]
            UI.draw_dashed_line(screen, color, (mid_x, 0), (mid_x, screen.get_height()))
            label_text = qubits # YES this is stupid
            UI.rotated_text(screen, label_text, mid_x, screen.get_height()/2, Colors.blue, bg_rect=True)
            return

        nrQubits = len(qubits)
        if nrQubits < 1: # should be at least one qubit
            raise ValueError
        # Check inside screen
        x = UI.grid_size * column + offset_x_y_tuple[0]
        if x < 0 or x > screen.get_width():
            return # Were out of bounds so we dont need to draw this gate
        
        # Draws vertical lines for connecting qubits
        if nrQubits > 1 and (gate_text=="CNOT" or gate_text=="X" or gate_text=="Toffoli" or gate_text=="SWAP" or gate_text=="X" or gate_text=="Y" or gate_text=="Z"):
            # Draw qubit line
            low_qubit = min(qubits)
            high_qubit = max(qubits)
            y1 = low_qubit * UI.grid_size + UI.grid_size/2 + offset_x_y_tuple[1] # Find midpoint of gate
            y2 = high_qubit * UI.grid_size + UI.grid_size/2 + offset_x_y_tuple[1] # Find midpoint of second gate
            mid_x = UI.grid_size * column + UI.grid_size/2 + offset_x_y_tuple[0]
            screenHandler.draw_qubit_line((mid_x,y1),(mid_x,y2), color) # Vertical line

            if gate_text=="CNOT" or gate_text=="Toffoli":
                for qubit in qubits:
                    y = qubit * UI.grid_size + UI.grid_size/2 + offset_x_y_tuple[1] # Find midpoint of gate
                    if qubit == high_qubit:
                        screenHandler.draw_mod(Loc.CIRCLE_CROSS, mid_x, y, color)
                    else:
                        screenHandler.draw_mod(Loc.FILLED_CIRCLE, mid_x, y, color)
            elif gate_text=="SWAP":
                for qubit in qubits:
                    y = qubit * UI.grid_size + UI.grid_size/2 + offset_x_y_tuple[1] # Find midpoint of gate
                    screenHandler.draw_mod(Loc.X_CROSS, mid_x, y, color)
            else:
                for qubit in qubits:
                    y = qubit * UI.grid_size + UI.grid_size/2 + offset_x_y_tuple[1] # Find midpoint of gate
                    # Controlled single qubit gates
                    if qubit!=high_qubit:
                        screenHandler.draw_mod(Loc.FILLED_CIRCLE, mid_x, y, color)
                    else:
                        self.__render_box_gate__(gate_text, [qubits[-1]], input_data, offset_x_y_tuple, column, color)
            gate = Gate(gate_text, mid_x, y, self.gateWidth, self.gateHeight)
        # Draw blank gate outline/ highlight
        elif gate_text=="blank":
            low_qubit = min(qubits)
            high_qubit = max(qubits)
            y1 = low_qubit * UI.grid_size + UI.grid_size/2 + offset_x_y_tuple[1] # Find midpoint of gate
            y2 = high_qubit * UI.grid_size + UI.grid_size/2 + offset_x_y_tuple[1] # Find midpoint of second gate
            x = UI.grid_size * column + center_offset + offset_x_y_tuple[0]
            pygame.draw.rect(screen, Colors.white, (x, y1, x + UI.gate_size, y2-y1), width=2)
        # Measure gate
        elif gate_text=="measure":
            center_offset = (UI.grid_size - UI.gate_size)/2 # Used to draw gate at centre of grid
            x = UI.grid_size * column + center_offset + offset_x_y_tuple[0]
            y = qubits[0] * UI.grid_size + center_offset + offset_x_y_tuple[1]
            gate_rect = (x, y, UI.gate_size, UI.gate_size) # Note this rect does not scale icon
            if not selected:
                image = pygame.image.load("frontend/images/gates/measure-unmeasured.png")
            else:
                # Measured
                if input_data==1:
                    image = pygame.image.load("frontend/images/gates/measure-measured-1.png")
                elif input_data==0:
                    image = pygame.image.load("frontend/images/gates/measure-measured-0.png")
                else:
                    image = pygame.image.load("frontend/images/gates/measure-measured.png")

            image = pygame.transform.smoothscale(image, (UI.gate_size, UI.gate_size))
                
            pygame.draw.rect(screen, color, gate_rect)
            screen.blit(image, gate_rect)
            gate = Gate(gate_text, x, y, self.gateWidth, self.gateHeight)
        # Draw the actual gate
        else:
            center_offset = (UI.grid_size - UI.gate_size)/2 # Used to draw gate at centre of grid
            x = UI.grid_size * column + center_offset + offset_x_y_tuple[0]
            y = qubits[0] * UI.grid_size + center_offset + offset_x_y_tuple[1] 
            gate = Gate(gate_text, x, y, self.gateWidth, self.gateHeight) # New gate object
            # Gate.draw_gate(gate.gate_text, x, y, self.gateWidth + self.adjust, self.gateHeight + self.adjust, color) # Draws gate
            self.__render_box_gate__(gate_text, qubits, input_data, offset_x_y_tuple, column, color)
        return gate # for gate shifting

    # Draws a gate as a box. Used for some custom gates (such as amod). Note: We might want to mark controlling qubit somehow
    # offset_x_y_tuple contatins the circuit offset (for panning)
    def __render_box_gate__(self, gate_text : str, qubits, calculations : [str], offset_x_y_tuple : tuple, column, color):
        center_offset = (UI.grid_size - UI.gate_size)/2 # Used to draw gate at centre of grid. This is the amount of pixels to reach centre
        
        # Draw dashed line to show outline of qubit
        lowest_qubit = min(qubits)
        highest_qubit = max(qubits)
        top_y = lowest_qubit * UI.grid_size + offset_x_y_tuple[1] + center_offset
        bottom_y = highest_qubit * UI.grid_size + offset_x_y_tuple[1] + UI.grid_size - center_offset
        left_x   = column * UI.grid_size + center_offset + offset_x_y_tuple[0]
        right_x  = column * UI.grid_size + center_offset + offset_x_y_tuple[0] + UI.gate_size
        line_width = 2
        UI.draw_dashed_line(screen, color, (left_x, top_y), (left_x, bottom_y), line_width)
        UI.draw_dashed_line(screen, color, (right_x - line_width, top_y), (right_x - line_width, bottom_y), line_width)

        # Draw vertical border lines for the qubits
        for qubit_index, qubit in enumerate(qubits):
            top_y    = qubits[qubit_index] * UI.grid_size + offset_x_y_tuple[1] # Note: The left and right lines are padded on the x-axis, but follow the grid size on the y axis
            bottom_y = qubits[qubit_index] * UI.grid_size + offset_x_y_tuple[1] + UI.grid_size
            if qubits[qubit_index] == lowest_qubit:
                top_y += center_offset
            if qubits[qubit_index] == highest_qubit:
                bottom_y -= center_offset

            # Draw left and right vertical lines
            left_x   = column * UI.grid_size + center_offset + offset_x_y_tuple[0]
            right_x  = column * UI.grid_size + center_offset + offset_x_y_tuple[0] + UI.gate_size
            # Draw gate shape
            pygame.draw.rect(screen, color, (left_x, top_y, UI.gate_size, bottom_y - top_y))
        # Draw text rotated 90 degrees
        center_row = (highest_qubit - lowest_qubit)/2
        center_x = column * UI.grid_size + UI.grid_size/2 + offset_x_y_tuple[0]
        center_y = (lowest_qubit + center_row + 0.5) * UI.grid_size + offset_x_y_tuple[1]
        # Draw text
        if len(gate_text)<3:
            UI.text(screen, gate_text, center_x, center_y, Colors.black)
        else:
            UI.rotated_text(screen, gate_text, center_x, center_y, Colors.black, bg_rect=True)

    # This is used to draw null-gates. Null-gates are gates which are temporarily added to list to highlight how the circuit will change.
    def __render_empty_gate__(): # TODO implement ()
        pass

def gatelist_gate_to_rect(gate_text : str, gate_index_in_list : int, operating_qubit : int, offset_x : int, offset_y : int)->pygame.rect:
    if gate_text == "label":
        return pygame.Rect(0,0,0,0) # TODO fix this collision
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
       
