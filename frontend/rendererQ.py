from ast import List, Return
from asyncio.windows_events import NULL
from enum import Enum
from os import system
from pickle import TRUE
from pickletools import pyfloat
from math import floor
import select
import string
from tkinter import END, Button
from turtle import Screen, circle, width
import mouse
import UI
import numpy
import pygame
import array 
import Colors
import bloch_sphere




class gateRenderer:
    def renderGate(gate : str, xpos: int, ypos: int):
        pygame.draw.rect(screen,colorWhite,(xpos, ypos, 40, 40),0)
        screen.blit(pygame.font.SysFont('Times New Roman', 45).render(gate, True, (170, 200, 200)), (xpos+1, ypos-2)) 
        
    def renderGateCustom(gate : str, xpos: int, ypos: int, width : int , height : int):
        rect = pygame.Rect(xpos, ypos, width, height)
        pygame.draw.rect(screen,colorWhite,rect,0)
        screen.blit(pygame.font.SysFont('Times New Roman', 45).render(gate, True, (170, 200, 200)), (xpos+1, ypos-2))
        return rect
        
class gateHandler:
    xStart = 75
    yStart = 75
    gateWidth = 40
    gateHeight = 40
    step = 0
    gateRenderer = gateRenderer()
    
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

    def addGate(self, gate : str, qubits, calculations : [str], relative_position : tuple, collumn): # integrating evenhandler for this method
        #pygame.draw.rect(screen, colorWhite, (self.xStart, self.yStart, self.gateWidth, self.gateHeight), 0)

        nrQubits = len(qubits)
        if nrQubits < 1: # should be at least one qubit
            raise ValueError

        #self.addGateCount(qubits[0])
        #self.step += 1
        pygame.font.init()
        
        #dy = relative_position[1] - 75

        if nrQubits > 1:
            for i in range(1, nrQubits):
                x = relative_position[0] + 50 * collumn + 20
                y = relative_position[1] + (qubits[i] * 50) + 25
                drawQline((x, (relative_position[1] + (qubits[0] * 50)) + 20), (x, y))
            for i in range(1, nrQubits):
                x = relative_position[0] + 50 * collumn + 20
                y = relative_position[1] + (qubits[i] * 50) + 25
                # need to change this
                drawQlineMod((x, y), (x, y), Loc.NONE, Loc.END_FILLED)

        gateRenderer.renderGate(gate, relative_position[0] + 50 * collumn, relative_position[1] + (qubits[0] * 50))
        wasClicked = pygame.mouse.get_pressed()[0]
        # below is an alternative way of handeling calculations
      

# this is mainly for testing, expect significant changes
# screen.blit(pygame.font.SysFont('Times New Roman', 45).render('I', True, (170, 200, 200)) ,((x + (n * 50) + 3,y+ (n * 50) - 5))) 
    
def renderQlines(qubits : int, dy : int, dx : int, width : int):
    if(dx < 0):
        dx = 0
    y = 50 + dy
    for i in range(qubits):
        y += 50
        drawQline((0 - dx, y),(width + (dx * 2),y))

def showCalculation(position : tuple, calculations : [str]): # not settled on calculation format, this is a test
            pygame.draw.rect(screen,colorWhite,(position[0], position[1], 100, 100),0)
            for calculation in calculations:
                screen.blit(pygame.font.SysFont(calculation, 45).render(calculation, True, (170, 170, 200)), (position[0]+1, position[1]-2))

class Loc(Enum):
    NONE = 0;
    START_FILLED = 1; 
    END_FILLED = 2
    START_CROSS = 3; 
    END_CROSS = 4;

# draws a line between 2 points on the canvas         
def drawQline(start : tuple, end : tuple):
    pygame.draw.line(screen,(255, 0, 0),start,end,1)
    

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

def drawQlineMod(start : tuple, end : tuple, mod1 : Loc, mod2 : Loc):
    
    drawQline(start,end)
    
    modCases(mod1, start, end)
    modCases(mod2, start, end)


#def panScreen(directions):
pygame.init()
screen = pygame.display.set_mode((800,700),pygame.RESIZABLE)
pygame.display.set_caption("circuitQ")

# Colors constants
colorWhite = (250,250,250)
colorSelected = (255, 200, 100) # Yellow

amount = 5 # stand in for number of qubits
renderQlines(amount, 0, 0, pygame.display.Info().current_w) # draw a line for each qubit

# below is for testing
handler = gateHandler()
calculations = ["calculation_placeholder"]

framerate = pygame.time.Clock()

# sampleString = "H 2 1 4 X 4 1 2 Z 2 0 H 2 1 4 X 4 1 2 Z 2 0 H 2 1 4 X 4 1 2 Z 2 0 H 2 1 4 X 4 1 2 Z 2 0 H 2 1 4 X 4 1 2 Z 2 0 H 2 1 4 X 4 1 2 Z 2 0"
# TODO: zoom out
offset = (75,75)

# access screen
pygame.display.Info()

x = 75
y = 75
# Tag panning:offset som apliceras på allt i scenen
circuit_dx = 0;
circuit_dy = 0;
# Tag meny: menyns höjd variabel 
# textCanvasY =  pygame.display.Info().current_h - 100 #920

drag_bar_y = screen.get_height() - 100
drag_bar_color = colorWhite
drag_bar_height = 15 # Height of draggable bar TODO make this into a reuseable class

tab_panel = UI.ChoicePanel(screen, drag_bar_y + drag_bar_height, ["Logic gates","Math view","Text view","Bloch sphere"])

bloch_sphere = bloch_sphere.Bloch_Sphere(screen, 0, drag_bar_y + 40, screen.get_width(), screen.get_height() - drag_bar_height)
bloch_sphere.add_random_point_on_unit_sphere()
bloch_sphere.add_random_point_on_unit_sphere()


displayCalc = False
dragging = False

# Mouse status
mouse = mouse.Mouse()

# drag/drop development below, unfinished
# name of selected gate
#selected = ""
dragging2 = False
coordinates = []


#skeleton for multi-check if above any hitbox.
def checkHitboxes(menuItems : int, boxCoordinates : [(int,int)], mouseX : int , mouseY : int ):
    print ("here")
    withinAnyHitBox = False  
    
    for i in range (0, menuItems):
        print (i)
        if within(40,40,boxCoordinates[i][0],boxCoordinates[i][1], mouseX, mouseY):
            withinAnyHitBox = True
            print ("here")
            print(f"withinAnyHitBox value for iteration {i}: {withinAnyHitBox}")
    return withinAnyHitBox
   

def within(width : int, height : int, xPos : int, yPos, mouseX : int, mouseY : int):
    selectReduction = 0
    print ("mouse coords")
    print (mouseX)
    print (mouseY)
    print ("gate coords")
    print (xPos)
    print (yPos)
    withinLy = (yPos + (height) - selectReduction) > mouseY
    withinHy = mouseY > yPos - (height) + selectReduction
    withinY = withinLy and withinHy

    withinLx = ( xPos - (width) + selectReduction) < mouseX
    withinRx = mouseX < xPos + (width) - selectReduction
    withinX = withinLx and withinRx
    return withinX and withinY
    
gateBoxHit = False
gateButton = False
         

xtest = 0
ytest = 0
# just for testing 
color = (250,250,250)


class MenuButton:
    def __init__(self, name : str , width : int , height : int):
        self.width = width
        self.height = height
        self.gate = name
        self.selected = False
        self.gatefield = pygame.Rect(150, 150, 175, 175) 
        
    def update(self, x : int, y : int):
        self.gatefield = gateRenderer.renderGateCustom(self.gate, x, y, self.width, self.height)
        

    def checkClicked(self, mouse):
        if (self.gatefield.collidepoint(pygame.mouse.get_pos()) and (mouse.r_click or mouse.r_held)):
            self.selected = True

class gate:
    def __init__(self, name : str , x : int , y : int , width : int , height : int):
        self.width = width
        self.height = height
        self.gate = name
        self.x = x
        self.y = y

    def gateAdded(self):
        gateRenderer.renderGateCustom(self.gate, self.x, self.y, self.width, self.height)

gates = ["X","Y","Z","H","S","T"]

def createGateButtons(names : [str], width : int, height : int):
    temp = []
    for gate in names:
        temp.append(MenuButton(gate, width, height))
    return temp
        

def renderButtons(buttonRows : [[MenuButton]], canvasYT : int ):
    xOffset = 75
    yOffset = 75
    for bRow in range (0, len(buttonRows)):
        for b in range (0, len(buttonRows[bRow])):
            button = buttonRows[bRow][b]
            button.update(15 + xOffset * b, canvasYT + 50 + (bRow * yOffset))

#buttons for the gate tab
gateButtons = createGateButtons(gates, 40, 40)

#related to merge
gateList = [('X', [0,3]),('H', [1,4,2]),('X', [0,3]), ('Z', [1,3,2]),('X', [0,3])]
x = 75
y = 75

def checkLines( x : int , y : int, xl, xr):
  
    withinLx = xl < x
    withinRx = x < xr
    withinX = withinLx and withinRx
    
    return withinX

class gate:
    def __init__(self, name : str , x : int , y : int , width : int , height : int):
        self.width = width
        self.height = height
        self.gate = name
        self.x = x
        self.y = y
        #TODO 
        

    def gateAdded(self):
        gateRenderer.renderGateCustom(self.gate, self.x, self.y, self.width, self.height)


while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        
    # Draw drag bar
    if drag_bar_y > screen.get_height() - 70: # TODO Replace with drag_bar_height for more natural resizing
        drag_bar_y = screen.get_height() - 70
    pygame.draw.rect(screen, drag_bar_color, (0, drag_bar_y, screen.get_width(), drag_bar_height))
    # Draw options panel + update positions
    tab_panel.y = drag_bar_y + drag_bar_height
    tab_panel.draw()
    bloch_sphere.y = tab_panel.y + tab_panel.height

    # Draw selected screen
    option = tab_panel.get_selected()
    if option == "Logic gates": # TODO Use enum/ atoms instead of strings
        renderButtons([gateButtons], drag_bar_y + 20)
    elif option == "Math view":
        pass # Implement math view renderer here
    elif option == "Text view":
        pass # TODO implement text view here
    elif option == "Bloch sphere":
        bloch_sphere.draw()
        pass # Implement Bloch sphere render here
    # ---------------------------------------------------------------
    # Mouse input
    mouse.update()
    # Update cursor + temporary colors
    if mouse.status == None and mouse.y > drag_bar_y and mouse.y < drag_bar_y + drag_bar_height:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS) # Set mouse cursor to "resize"-image
        drag_bar_color = colorSelected
    elif mouse.status == "Panning": # TODO Now it changes when cursor isnt moving, should use a time held timer instead probably. This is to preventing cursor changing when clicking
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow) # Reset mouse image
        drag_bar_color = Colors.white

    # Left click
    if mouse.l_click:
        # Check for tabs here
        tab_panel.click(mouse.x, mouse.y)
        if mouse.y > drag_bar_y and mouse.y < drag_bar_y + drag_bar_height:
            mouse.status = "Resizing bottom panel"
        elif mouse.y < drag_bar_y:
            mouse.status = "Panning"
        elif mouse.y > drag_bar_y + drag_bar_height + tab_panel.height:
            # Below panel selector
            # Bloch sphere
            if tab_panel.get_selected()=="Bloch sphere":
                mouse.status = "Panning sphere"
    # Left mouse is being held down
    elif mouse.l_held:
        # Below is interaction for the reizeable panel at the bottom
        if mouse.status == "Resizing bottom panel":
            drag_bar_y = mouse.y # Move UI
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS) # Set mouse cursor to "resize"-image
            drag_bar_color = colorSelected
        # Drag circuit
        elif mouse.status == "Panning":
            circuit_dx += mouse.dx
            circuit_dy += mouse.dy
        # Rotate Bloch sphere
        elif mouse.status == "Panning sphere":
            bloch_sphere.pan(mouse)
    # ---------------------------------------------------------------

    screenInfo = pygame.display.Info()
    screenWidth = screenInfo.current_w
    screenHeight = screenInfo.current_h

    # allt nedan ska paketeras i lämpliga metoder
    # use for test
    if displayCalc:
        showCalculation((100,200), calculations)
       
    for button in gateButtons:
        if button.selected and (mouse.r_held or mouse.r_click):
            print ("Clicked gate" + button.gate)
            gateRenderer.renderGate(button.gate, mouse.x,  mouse.y)
    
        elif button.selected and (not mouse.r_held):
            print ("release " + button.gate)
            print (mouse.dy)
            print (floor((mouse.y - mouse.dy) / 50))
            check = False
            for i in range(0,len(gateList)):
                if checkLines(mouse.x, mouse.y, ((x + circuit_dx) + 50 * i) - 20, ((x + circuit_dx) + 50 * i) + 20):
                    gateList.insert(i -1, (button.gate, [floor((mouse.y - circuit_dy) / 50) - 1]))
                    check = True
            if not check:
                gateList.append((button.gate, [floor((mouse.y - circuit_dy) / 50) - 1]))
            button.selected = False  
        if not button.selected:
            button.checkClicked(mouse)

    # Draw circuit
    renderQlines(amount, circuit_dy, circuit_dx, pygame.display.Info().current_w) # Draws horisontal lines for qubits
    for i in range(0,len(gateList)):
        temp = gateList[i]      
        handler.addGate(temp[0], temp[1], ["calculation_placeholder"],(x + circuit_dx,y + circuit_dy),i+1)

    pygame.display.update()
    framerate.tick(30)
    
