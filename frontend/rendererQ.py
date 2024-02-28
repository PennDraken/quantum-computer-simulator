from pickletools import pyfloat
from math import floor
import Utilities.mouse as mouse
import UI
import pygame
import Utilities.Colors as Colors
import bloch_sphere

from gates import Gate, gateHandler
import Utilities.screenHandler as screenHandler

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
mouse = mouse.Mouse()

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
        if (self.gatefield.collidepoint(pygame.mouse.get_pos()) and (mouse.r_click or mouse.r_held)):
            self.selected = True


def createGateButtons(names : [str], width : int, height : int):
    temp = []
    for gate in names:
        temp.append(MenuButton(gate, width, height))
    return temp

gatesList = ["H", "X", "Y", "Z", "I", "S", "T", "CNOT"]
gateButtons = createGateButtons(gatesList, 40, 40)
        
def renderButtons(buttonRows : [[MenuButton]], canvasYT : int ):
    xOffset = 75
    yOffset = 75
    for bRow in range (0, len(buttonRows)):
        for b in range (0, len(buttonRows[bRow])):
            button = buttonRows[bRow][b] # Is a MenuButton
            button.update(buttonRows[bRow][b].gate, 15 + xOffset * b, canvasYT + 50 + (bRow * yOffset))

#buttons for the gate tab

#related to merge
gateList = [('X', [0,3]),('H', [1,4,2]),('X', [0,3]), ('Z', [1,3,2]),('X', [0,3])]
x = 75
y = 75

def checkLines( x : int , y : int, xl, xr):
  
    withinLx = xl < x
    withinRx = x < xr
    withinX = withinLx and withinRx
    
    return withinX


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
        drag_bar_color = Colors.yellow
        print("hover")
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
            drag_bar_color = Colors.yellow
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
            Gate.renderGate(button.gate, mouse.x,  mouse.y, 40, 40)
    
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

    
    screenHandler.renderQlines(amount, circuit_dy, circuit_dx, pygame.display.Info().current_w) # Draws horisontal lines for qubits

    # Draw example circuit
    for i in range(0,len(gateList)):
        temp = gateList[i]      
        handler.addGate(temp[0], temp[1], ["calculation_placeholder"],(x + circuit_dx,y + circuit_dy),i+1)

    pygame.display.update()
    framerate.tick(30)
    
