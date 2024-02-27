import pygame
import sys
from enum import Enum

pygame.init()
screen = pygame.display.set_mode((800, 700), pygame.RESIZABLE)
pygame.display.set_caption("circuitQ")

class Loc(Enum):
    NONE = 0;
    START_FILLED = 1; 
    END_FILLED = 2
    START_CROSS = 3; 
    END_CROSS = 4;


# draws a line between 2 points on the canvas         
def drawQline(start: tuple, end: tuple):
    pygame.draw.line(screen, (255, 0, 0), start, end, 1)


# draws a line between 2 points on the canvas and adds a circle at the start and end
def drawQlineMod(start : tuple, end : tuple, mod1 : Loc, mod2 : Loc):
    drawQline(start,end)
    modCases(mod1, start, end)
    modCases(mod2, start, end)

def renderQlines(qubits : int, dy : int, dx : int, width : int):
    if(dx < 0):
        dx = 0
    y = 50 + dy
    for i in range(qubits):
        y += 50
        drawQline((0 - dx, y), (width + (dx * 2), y))

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
