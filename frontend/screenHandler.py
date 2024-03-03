import pygame
import sys
from enum import Enum
import UI

pygame.init()
screen = pygame.display.set_mode((800, 700), pygame.RESIZABLE)
pygame.display.set_caption("Kvantis")

class Loc(Enum):
    NONE = 0;
    START_FILLED = 1; 
    END_FILLED = 2
    START_CROSS = 3; 
    END_CROSS = 4;


# Draws a red line between 2 points on the canvas (used for rendering qubit lines and connections)
def drawQline(start: tuple, end: tuple):
    pygame.draw.line(screen, (255, 0, 0), start, end, 1)


# draws a line between 2 points on the canvas and adds a circle at the start and end
def drawQlineMod(start : tuple, end : tuple, mod1 : Loc, mod2 : Loc):
    drawQline(start,end)
    modCases(mod1, start, end)
    modCases(mod2, start, end)

def renderQlines(qubits : int, offset_dx : int, offset_dy : int, width : int):
    y = UI.grid_size/2 + offset_dy
    for i in range(qubits):
        drawQline((0, y), (width, y))
        y += UI.grid_size


# draws a circle at a point on the canvas
def modCases(mod : Loc, start : tuple, end : tuple):
    match mod:
        case Loc.START_FILLED:
            pygame.draw.circle(screen, (255, 255, 255),start,4)
        case Loc.END_FILLED:
            pygame.draw.circle(screen, (255, 255, 255),end, 4) 
        case Loc.START_CROSS: 
            pygame.draw.circle(screen, (255, 255, 255),start,15, 2) #change 
        case Loc.END_CROSS:
            pygame.draw.circle(screen, (255, 255, 255),end, 15, 2) #change
        case Loc.NONE:
            pass
