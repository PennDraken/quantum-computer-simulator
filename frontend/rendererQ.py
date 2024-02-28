from pickletools import pyfloat
from math import floor
import Utilities.mouse as mouse
import UI
import pygame
import Utilities.Colors as Colors
import bloch_sphere
import Fields.MenuButton as MenuButton

from gates import Gate, gateHandler
from Utilities.mouse import Mouse
import screenHandler

import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

screen = screenHandler.screen
# this is mainly for testing, expect significant changes
# screen.blit(pygame.font.SysFont('Times New Roman', 45).render('I', True, (170, 200, 200)) ,((x + (n * 50) + 3,y+ (n * 50) - 5))) 

amount = 5 # stand in for number of qubits

def showCalculation(position : tuple, calculations : [str]): # not settled on calculation format, this is a test
            pygame.draw.rect(screen,(position[0], position[1], 100, 100),0)
            for calculation in calculations:
                screen.blit(pygame.font.SysFont(calculation, 45).render(calculation, True, (170, 170, 200)), (position[0]+1, position[1]-2))


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
drag_bar_color = Colors.white
drag_bar_height = 15 # Height of draggable bar TODO make this into a reuseable class

tab_panel = UI.ChoicePanel(screen, drag_bar_y + drag_bar_height, ["Logic gates","Math view","Text view","Bloch sphere"])

bloch_sphere = bloch_sphere.Bloch_Sphere(screen, 0, drag_bar_y + 40, screen.get_width(), screen.get_height() - drag_bar_height)
bloch_sphere.add_random_point_on_unit_sphere()
bloch_sphere.add_random_point_on_unit_sphere()


displayCalc = False
dragging = False

# Mouse status
# drag/drop development below, unfinished
# name of selected gate
#selected = ""
dragging2 = False
coordinates = []



gateBoxHit = False
gateButton = False
         

xtest = 0
ytest = 0
# just for testing 
color = (250,250,250)
        
#buttons for the gate tab

#related to merge
gateList = [('X', [0,3]),('H', [1,4,2]),('X', [0,3]), ('Z', [1,3,2]),('X', [0,3])]
x = 75
y = 75

gatesList = ["H", "X", "Y", "Z", "I", "S", "T", "CNOT"]
gateButtons = MenuButton.createGateButtons(gatesList, 40, 40)

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    # Draw circuit view
    screenHandler.renderQlines(amount, circuit_dy, circuit_dx, pygame.display.Info().current_w) # Draws horisontal lines for qubits
    # Draw example circuit
    for i in range(0,len(gateList)):
        temp = gateList[i]      
        handler.addGate(temp[0], temp[1], ["calculation_placeholder"],(x + circuit_dx,y + circuit_dy),i+1)

    # Draw drag bar
    if drag_bar_y > screen.get_height() - 70: # TODO Replace with drag_bar_height for more natural resizing
        drag_bar_y = screen.get_height() - 70
    pygame.draw.rect(screen, drag_bar_color, (0, drag_bar_y, screen.get_width(), drag_bar_height))
    # Draw options panel + update positions
    tab_panel.y = drag_bar_y + drag_bar_height
    tab_panel.draw()
    bloch_sphere.y = tab_panel.y + tab_panel.height
    # Draws bg of panel window (hides circuit)
    pygame.draw.rect(screen, Colors.black, (0, tab_panel.y+tab_panel.height, screen.get_width(), screen.get_height()-tab_panel.y-tab_panel.height))


    # Draw selected screen
    option = tab_panel.get_selected()
    if option == "Logic gates": # TODO Use enum/ atoms instead of strings
        MenuButton.renderButton([gateButtons], drag_bar_y + 20)
    elif option == "Math view":
        pass # Implement math view renderer here
    elif option == "Text view":
        pass # TODO implement text view here
    elif option == "Bloch sphere":
        bloch_sphere.draw()
        pass # Implement Bloch sphere render here
    # ---------------------------------------------------------------
    # Mouse input
    Mouse.update(Mouse)
    # Update cursor + temporary colors
    if Mouse.status == None and Mouse.y > drag_bar_y and Mouse.y < drag_bar_y + drag_bar_height:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS) # Set mouse cursor to "resize"-image
        drag_bar_color = Colors.yellow
    elif Mouse.status == "Panning": # TODO Now it changes when cursor isnt moving, should use a time held timer instead probably. This is to preventing cursor changing when clicking
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow) # Reset mouse image
        drag_bar_color = Colors.white

    # Left click
    if Mouse.l_click:
        # Check for tabs here
        tab_panel.click(Mouse.x, Mouse.y)
        if Mouse.y > drag_bar_y and Mouse.y < drag_bar_y + drag_bar_height:
            Mouse.status = "Resizing bottom panel"
        elif Mouse.y < drag_bar_y:
            Mouse.status = "Panning"
        elif Mouse.y > drag_bar_y + drag_bar_height + tab_panel.height:
            # Below panel selector
            # Bloch sphere
            if tab_panel.get_selected()=="Bloch sphere":
                mouse.status = "Panning sphere"
    # Left mouse is being held down
    elif Mouse.l_held:
        # Below is interaction for the reizeable panel at the bottom
        if Mouse.status == "Resizing bottom panel":
            drag_bar_y = Mouse.y # Move UI
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS) # Set mouse cursor to "resize"-image
            drag_bar_color = Colors.yellow
        # Drag circuit
        elif Mouse.status == "Panning":
            circuit_dx += Mouse.dx
            circuit_dy += Mouse.dy
        # Rotate Bloch sphere
        elif Mouse.status == "Panning sphere":
            bloch_sphere.pan(Mouse)
    # ---------------------------------------------------------------

    #screenInfo = pygame.display.Info()
    #screenWidth = screenInfo.current_w
    #screenHeight = screenInfo.current_h

    if displayCalc:
        showCalculation((100,200), calculations)

    MenuButton.test(gateButtons, gateList, x, y, circuit_dx, circuit_dy)

    pygame.display.update()
    framerate.tick(30)
    
    
