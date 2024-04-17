# This is a class that handles the logic for the navigation bar at top
# Where you can step through circuit
import pygame
import Utilities.Colors as Colors
import UI

class Circuit_Navigation_Window:
    def __init__(self, screen, x: int, y: int, circuit, images = [pygame.image.load("frontend/images/icons/circuit-reset.png"), pygame.image.load("frontend/images/icons/circuit-run.png"), pygame.image.load("frontend/images/icons/circuit-step-backwards.png"), pygame.image.load("frontend/images/icons/circuit-step-forwards.png")]):
        self.screen: pygame.screen = screen
        self.x = x
        self.y = y
        self.width = screen.get_width()
        self.height = 50
        self.button_width = 100
        self.button_height = 50
        self.icon_size = int(self.button_height * 0.5)
        self.circuit = circuit
        self.title_font = pygame.font.Font(None, 24)
        self.state_font = pygame.font.Font(None, 20)
        self.options = ["Reset","Run","<<",">>"]
        self.set_icons(images)
        self.hover_button_i = None # Button currently being hovered on
        
    def draw(self):
        # update width
        self.width = self.screen.get_width()
        # draw background
        pygame.draw.rect(self.screen, Colors.black, (self.x, self.y, self.width, self.height))
        w = 2 # Width of outline
        pygame.draw.rect(self.screen, Colors.white, (self.x - w, self.y - w, self.width + 2*w, self.height + 2*w), width=w)
        # draw squares at equal distance
        box_y = self.height/2-self.button_height/2
        for i in range(0, len(self.options)):
            distance_between_boxes = self.width / len(self.options)
            box_x = distance_between_boxes * i + distance_between_boxes/2 - self.button_width/2
            # Draw button square
            if self.hover_button_i==i:
                pygame.draw.rect(self.screen, Colors.hover, (box_x, box_y, self.button_width, self.button_height))
            else:
                pygame.draw.rect(self.screen, Colors.white, (box_x, box_y, self.button_width, self.button_height))
            icon = self.icons[i]
            if icon != None:
                icon_rect = (box_x + self.button_width/2 - self.icon_size/2, box_y + self.button_height/2 - self.icon_size/2, self.icon_size, self.icon_size) # Note this rect does not scale icon
                self.screen.blit(icon, icon_rect)
                # text(self.screen, self.options[i], box_x + self.button_width/2, box_y + self.button_height/2, Colors.black, self.title_font)
            else:
                # Draw button text centered on square
                text(self.screen, self.options[i], box_x + self.button_width/2, box_y + self.button_height/2, Colors.black, self.title_font)

    # Updates state
    def update(self, mouse):
        self.width = self.screen.get_width()
        self.__check_hover__(mouse.x, mouse.y)
        if mouse.l_click:
            self.click(mouse.x, mouse.y)

    # Handles mouse left click input
    def click(self, x, y):
        # iterate through all buttons
        box_y = self.height/2-self.button_height/2
        for i in range(0, len(self.options)):
            distance_between_boxes = self.width / len(self.options)
            box_x = distance_between_boxes * i + distance_between_boxes/2 - self.button_width/2
            # check click collision
            if x > box_x and x < box_x + self.button_width and y > box_y and y < box_y + self.button_height:
                if self.options[i]=="Reset":
                    self.circuit.reset()
                elif self.options[i]=="Run":
                    self.circuit.run()
                elif self.options[i]=="<<":
                    self.circuit.step_back()
                elif self.options[i]==">>":
                    self.circuit.step_fwd()

    def set_icons(self, images):
        self.icons = []
        for image in images:
            scaled_image = pygame.transform.smoothscale(image, (self.icon_size, self.icon_size))
            self.icons.append(scaled_image)    

    def __get_button_i__(self, x, y):
        # iterate through all buttons
        box_y = self.height/2-self.button_height/2
        for i in range(0, len(self.options)):
            distance_between_boxes = self.width / len(self.options)
            box_x = distance_between_boxes * i + distance_between_boxes/2 - self.button_width/2
            # check click collision
            if x > box_x and x < box_x + self.button_width and y > box_y and y < box_y + self.button_height:
                return i

    # Highlights a button if x y are inside
    def __check_hover__(self, x, y):
        self.hover_button_i = self.__get_button_i__(x,y)

    
# Draws centered text on screen
def text(screen, string, x, y, color, font):
    text_color = pygame.Color(color)
    text_surface = font.render(string, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
