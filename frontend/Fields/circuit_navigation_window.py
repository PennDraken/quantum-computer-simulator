# This is a class that handles the logic for the navigation bar at top
# Where you can step through circuit
import pygame
import Utilities.Colors as Colors
import UI

class Circuit_Navigation_Window:
    def __init__(self, screen, x: int, y: int, circuit):
        self.screen: pygame.screen = screen
        self.x = x
        self.y = y
        self.width = screen.get_width()
        self.height = 50
        self.button_width = 100
        self.button_height = 50
        self.circuit = circuit
        self.title_font = pygame.font.Font(None, 24)
        self.state_font = pygame.font.Font(None, 20)
        self.options = ["Run","<<",">>"]

    def draw(self):
        # update width
        self.width = self.screen.get_width()
        # draw background
        pygame.draw.rect(self.screen, Colors.black, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.screen, Colors.white, (self.x, self.y, self.width, self.height), width=1)
        # draw squares at equal distance
        box_y = self.height/2-self.button_height/2
        for i in range(0, len(self.options)):
            distance_between_boxes = self.width / len(self.options)
            box_x = distance_between_boxes * i + distance_between_boxes/2 - self.button_width/2
            # Draw button square
            pygame.draw.rect(self.screen, Colors.white, (box_x, box_y, self.button_width, self.button_height))
            # Draw button text centered on square
            text(self.screen, self.options[i], box_x + self.button_width/2, box_y + self.button_height/2, Colors.black, self.title_font)

    # Handles mouse input
    def click(self, x, y):
        # update width
        self.width = self.screen.get_width()
        # iterate through all buttons
        box_y = self.height/2-self.button_height/2
        for i in range(0, len(self.options)):
            distance_between_boxes = self.width / len(self.options)
            box_x = distance_between_boxes * i + distance_between_boxes/2 - self.button_width/2
            # check click collision
            if x > box_x and x < box_x + self.button_width and y > box_y and y < box_y + self.button_height:
                if self.options[i]=="Run":
                    self.circuit.run()
                elif self.options[i]=="<<":
                    self.circuit.step_back()
                elif self.options[i]==">>":
                    self.circuit.step_fwd()
# Draws centered text on screen
def text(screen, string, x, y, color, font):
    text_color = pygame.Color(color)
    text_surface = font.render(string, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
