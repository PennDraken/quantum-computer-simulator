import pygame
import sys, os

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
        self.gatefield = Gate.renderGate(gate, x, y, self.width, self.height)
        
    def checkClicked(self, mouse):
        if (self.gatefield.collidepoint(pygame.mouse.get_pos()) and (Mouse.r_click or Mouse.r_held)):
            self.selected = True


def createGateButtons(names : [str], width : int, height : int):
    temp = []
    for gate in names:
        temp.append(MenuButton(gate, width, height))
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

def test(gateButtons : [[MenuButton]], gateList : [(str, [int])], x : int, y : int, circuit_dx : int, circuit_dy : int):
    for button in gateButtons:
        if button.selected and (Mouse.r_held or Mouse.r_click):
            print ("Clicked gate " + button.gate)
            Gate.renderGate(button.gate, Mouse.x,  Mouse.y, 40, 40)
    
        elif button.selected and (not Mouse.r_held):
            print ("Release " + button.gate)
            print (Mouse.dy)
            print (floor((Mouse.y - Mouse.dy) / 50))
            check = False
            for i in range(0,len(gateList)):
                if checkLines(Mouse.x, Mouse.y, ((x + circuit_dx) + 50 * i) - 20, ((x + circuit_dx) + 50 * i) + 20):
                    gateList.insert(i -1, (button.gate, [floor((Mouse.y - circuit_dy) / 50) - 1]))
                    check = True
            if not check:
                gateList.append((button.gate, [floor((Mouse.y - circuit_dy) / 50) - 1]))
            button.selected = False  
        if not button.selected:
            button.checkClicked(Mouse)