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
    
    def renderGate(gate : str, xpos: int, ypos: int, width : int, height : int):
        rect = pygame.Rect(xpos, ypos, width, height)
        pygame.draw.rect(screen,Colors.white,rect,0)
        screen.blit(pygame.font.SysFont('Times New Roman', 45).render(gate, True, (170, 200, 200)), (xpos+4, ypos-3))
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


    def addGate(self, gate : str, qubits, calculations : [str], relative_position : tuple, column): # integrating evenhandler for this method
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
        Gate.renderGate(gate.gate, x, y, self.gateWidth, self.gateHeight) # Render gate 
        return gate # for gate shifting
       
