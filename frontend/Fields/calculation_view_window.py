# This is a class that shows the states at various points of the calculation on window
import pygame
import Utilities.Colors as Colors

class Calculation_Viewer_Window:
    def __init__(self, screen, x : int , y : int , width : int , height : int, systems : []):
        self.screen : pygame.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.systems = systems
        self.grid_size = 90 # Width and height of the underlying grid

    def draw(self):
        # draw grid in panel
        self.height = self.screen.get_height() - self.y
        grid_columns = int(self.screen.get_width() / self.grid_size) + 1
        grid_rows = int(self.height / self.grid_size) + 1

        # Draw grids
        for i in range(0, grid_columns):
            for j in range(0, grid_rows):
                pygame.draw.rect(self.screen,Colors.white, (self.x + i * self.grid_size, self.y + j * self.grid_size, self.grid_size, self.grid_size), width=1)

        # Draw registers
        for col in range(0, len(self.systems)):
            system = self.systems[col]
            for register_index in range(0, len(system.registers)):
                register = system.registers[register_index]
                x = col * self.grid_size # Leftmost pos 
                y = register_index * self.grid_size + self.y
                label = register.get_label()
                text(self.screen, label, x + self.grid_size/2, y, Colors.yellow)
        
def text(screen, string, x, y, color):
    font_size = 24
    font = pygame.font.Font(None, font_size)
    text_color = pygame.Color(color)
    text_surface = font.render(string, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y + font_size/2)
    screen.blit(text_surface, text_rect)