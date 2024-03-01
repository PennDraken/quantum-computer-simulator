import pygame
from enum import Enum
import Utilities.Colors as Colors
import screenHandler

Loc = screenHandler.Loc
screen = screenHandler.screen

class Gate:
    def __init__(self, name : str , x : int , y : int , width : int , height : int):
        self.width = width
        self.height = height
        self.gate = name
        self.x = x
        self.y = y
    
    def renderGate(gate_text : str, xpos: int, ypos: int, width : int, height : int, color):
        rect = pygame.Rect(xpos, ypos, width, height)
        pygame.draw.rect(screen, color,rect,0)
        # screen.blit(pygame.font.SysFont('Times New Roman', 10).render(gate, True, (170, 200, 200)), (xpos+4, ypos-3))
        text(gate_text, xpos+width/2, ypos+height/2, Colors.black, pygame.font.Font(None, 20))
        return rect
    

    
    def gCollider(self):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return rect
        
class gateHandler:
    xStart = 75
    yStart = 75
    gateWidth = 40
    gateHeight = 40
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


    def addGate(self, gate : str, qubits, calculations : [str], relative_position : tuple, column, color): # integrating evenhandler for this method
        grid_size = 50
        nrQubits = len(qubits)
        if nrQubits < 1: # should be at least one qubit
            raise ValueError

        pygame.font.init()
        if nrQubits > 1:
            for i in range(1, nrQubits):
                x = relative_position[0] + grid_size * column + 20
                y = relative_position[1] + (qubits[i] * grid_size) + 25
                screenHandler.drawQline((x, (relative_position[1] + (qubits[0] * grid_size)) + 20), (x, y))
            for i in range(1, nrQubits):
                x = relative_position[0] + grid_size * column + 20
                y = relative_position[1] + (qubits[i] * grid_size) + 25
                # need to change this
                screenHandler.drawQlineMod((x, y), (x, y), Loc.NONE, Loc.END_FILLED)

        x = relative_position[0] + grid_size * column
        y = relative_position[1] + (qubits[0] * grid_size)
        gate = Gate(gate, x, y, self.gateWidth, self.gateHeight) # New gate object
        Gate.renderGate(gate.gate, x, y, self.gateWidth, self.gateHeight, color) # Render gate
        return gate # for gate shifting


# Draws centered text on screen
def text(string, x, y, color, font):
    text_color = pygame.Color(color)
    text_surface = font.render(string, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
       
