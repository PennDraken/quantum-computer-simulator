import pygame
import sys
from enum import Enum
import UI
import Utilities.Colors as Colors

pygame.init()
img = pygame.image.load("frontend/images/icons/program-logo-32.png")
pygame.display.set_icon(img)

screen = pygame.display.set_mode((800, 700), pygame.RESIZABLE)
pygame.display.set_caption("Kvantis")


offsetMod = 0

class Loc(Enum):
    NONE = 0;
    START_FILLED = 1; 
    END_FILLED = 2
    START_CROSS = 3; 
    END_CROSS = 4;
    START_CROSS2 = 5; 
    END_CROSS2 = 6;
    CIRCLE_CROSS = 7;
    FILLED_CIRCLE = 8;
    X_CROSS = 9;


# Draws a line between 2 points on the canvas (used for rendering qubit lines and connections)
def draw_qubit_line(start: tuple, end: tuple, color):
    pygame.draw.line(screen, color, start, end, 4)


# draws a line between 2 points on the canvas and adds a circle at the start and end
def drawQlineMod(start : tuple, end : tuple, mod1 : Loc, mod2 : Loc, color):
    draw_qubit_line(start, end, color)
    draw_qubit_connection_point(mod1, start, end, color)
    draw_qubit_connection_point(mod2, start, end, color)

def draw_horizontal_qubit_lines(number_of_qubits : int, x : int, offset_dy : int, width : int, color):
    y = UI.grid_size/2 + offset_dy
    for i in range(number_of_qubits):
        draw_qubit_line((x, y), (width, y), color)
        y += UI.grid_size


# draws a circle at a point on the canvas
def draw_qubit_connection_point(mod : Loc, start : tuple, end : tuple, color):
    match mod:
        case Loc.START_FILLED:
            pygame.draw.circle(screen, color, start, 8)
        case Loc.END_FILLED:
            pygame.draw.circle(screen, color, end, 8) 
        case Loc.START_CROSS: 
            #pygame.draw.circle(screen, Colors.white, start, 15, 2) #change 
            pygame.draw.circle(screen,color,start,UI.gate_size / 3, 3) # move these to screen handler 
            draw_qubit_line((start[0] - (UI.gate_size / 3),start[1]), (start[0] + (UI.gate_size / 3), start[1]), color)
            draw_qubit_line((start[0],start[1] - (UI.gate_size / 3)), (start[0], start[1]  + (UI.gate_size / 3)), color)
        case Loc.END_CROSS:
            # pygame.draw.circle(screen, color, end, 15, 2) #change
            pygame.draw.circle(screen,color,end,UI.gate_size / 3, 3) # move these to screen handler 
            draw_qubit_line((end[0] - (UI.gate_size / 3),end[1]), (end[0] + (UI.gate_size / 3), end[1]), color)
            draw_qubit_line((end[0],end[1] - (UI.gate_size / 3)), (end[0], end[1]  + (UI.gate_size / 3)), color)
        case Loc.START_CROSS2:
            draw_qubit_line((start[0] - (UI.gate_size / 3),start[1] - (UI.gate_size / 3)), (start[0] + (UI.gate_size / 3), start[1] + (UI.gate_size / 3)), color)
            draw_qubit_line((start[0] + (UI.gate_size / 3),start[1] - (UI.gate_size / 3)), (start[0] - (UI.gate_size / 3), start[1]  + (UI.gate_size / 3)), color)
        case Loc.END_CROSS2:
           draw_qubit_line((end[0] - (UI.gate_size / 3),end[1] - (UI.gate_size / 3)), (end[0] + (UI.gate_size / 3), end[1] + (UI.gate_size / 3)), color)
           draw_qubit_line((end[0] + (UI.gate_size / 3),end[1] - (UI.gate_size / 3)), (end[0] - (UI.gate_size / 3), end[1]  + (UI.gate_size / 3)), color)
        case Loc.NONE:
            pass

# Draws a mod shape at x y on screen. Used to render gates like CNOT, TOFFOLI, SWAP.
def draw_mod(mod, x, y, color):
    pos = (x,y)
    match mod:
        case Loc.FILLED_CIRCLE:
            pygame.draw.circle(screen, color, pos, 8)
        case Loc.CIRCLE_CROSS: 
            pygame.draw.circle(screen,color,pos,UI.gate_size / 3, 3) # move these to screen handler 
            draw_qubit_line((pos[0] - (UI.gate_size / 3),pos[1]), (pos[0] + (UI.gate_size / 3), pos[1]), color)
            draw_qubit_line((pos[0],pos[1] - (UI.gate_size / 3)), (pos[0], pos[1]  + (UI.gate_size / 3)), color)
        case Loc.X_CROSS:
            # pygame.draw.circle(screen,color,pos,UI.gate_size / 3, 3) # move these to screen handler
            draw_qubit_line((x - (UI.gate_size / 3), y + (UI.gate_size / 3)), (x + (UI.gate_size / 3), y - (UI.gate_size / 3)), color)
            draw_qubit_line((x - (UI.gate_size / 3), y - (UI.gate_size / 3)), (x + (UI.gate_size / 3), y + (UI.gate_size / 3)), color)
        case Loc.NONE:
            pass