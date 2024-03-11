import pygame
import sys
from enum import Enum
import UI
import Utilities.Colors as Colors

pygame.init()
screen = pygame.display.set_mode((800, 700), pygame.RESIZABLE)
pygame.display.set_caption("Kvantis")

class Loc(Enum):
    NONE = 0;
    START_FILLED = 1; 
    END_FILLED = 2
    START_CROSS = 3; 
    END_CROSS = 4;


# Draws a line between 2 points on the canvas (used for rendering qubit lines and connections)
def draw_qubit_line(start: tuple, end: tuple, color):
    pygame.draw.line(screen, color, start, end, 4)


# draws a line between 2 points on the canvas and adds a circle at the start and end
def drawQlineMod(start : tuple, end : tuple, mod1 : Loc, mod2 : Loc, color):
    draw_qubit_line(start, end, color)
    draw_qubit_connection_point(mod1, start, end)
    draw_qubit_connection_point(mod2, start, end)

def draw_horizontal_qubit_lines(qubits : int, offset_dx : int, offset_dy : int, width : int, color):
    y = UI.grid_size/2 + offset_dy
    for i in range(qubits):
        draw_qubit_line((0, y), (width, y), color)
        y += UI.grid_size


# draws a circle at a point on the canvas
def draw_qubit_connection_point(mod : Loc, start : tuple, end : tuple):
    match mod:
        case Loc.START_FILLED:
            pygame.draw.circle(screen, Colors.white, start, 8)
        case Loc.END_FILLED:
            pygame.draw.circle(screen, Colors.white, end, 8) 
        case Loc.START_CROSS: 
            pygame.draw.circle(screen, Colors.white, start, 15, 2) #change 
        case Loc.END_CROSS:
            pygame.draw.circle(screen, Colors.white, end, 15, 2) #change
        case Loc.NONE:
            pass
