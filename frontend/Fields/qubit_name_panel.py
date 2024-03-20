# The panel on the left side of the window, which shows the qubit names
import pygame
import Utilities.Colors as Colors
import UI

class Qubit_Name_Panel:
    def __init__(self, screen, y, qubits_list, offset_y):
        self.screen: pygame.screen = screen
        self.x = 0
        self.y = y
        self.offset_y = offset_y
        self.width = int(UI.grid_size) # Not pointer
        self.height = UI.grid_size
        self.qubits_list = qubits_list
        self.title_font = pygame.font.Font(None, 40)
        self.state_font = pygame.font.Font(None, 20)

    def draw(self):
        pygame.draw.rect(self.screen, Colors.black, (self.x, self.y, self.width, self.screen.get_height()))
        pygame.draw.rect(self.screen, Colors.white, (self.x, self.y, self.width, self.screen.get_height()), width=2)
        # Label all qubits
        for i, qubit_str in enumerate(self.qubits_list):
            y = UI.grid_size * i + self.offset_y
            pygame.draw.rect(self.screen, Colors.white, (self.x, y, self.width, UI.grid_size), width=1)
            text(self.screen, f"|{qubit_str}>", self.x + self.width/2, y + UI.grid_size/2, Colors.white, self.title_font)
        # Draw a + button underneath qubits (TODO make clickable)
        y = UI.grid_size * len(self.qubits_list) + self.offset_y
        # pygame.draw.rect(self.screen, Colors.white, (self.x, y, UI.grid_size, UI.grid_size), width=1)
        text(self.screen, "+", self.x + self.width/2, y + UI.grid_size/2, Colors.white, self.title_font)


# Draws centered text on screen TODO Make a general class for this type of prints
def text(screen, string, x, y, color, font):
    text_color = pygame.Color(color)
    text_surface = font.render(string, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
