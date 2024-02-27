import pygame
import mouse
import Colors

# A single button on screen
class Button():
    def __init__(self, screen, rect : pygame.Rect, text, color_base, color_hover, color_selected):
        self.screen = screen
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color_base # Color thatds drawn
        self.color_unselected = color_base
        self.color_hover = color_hover
        self.color_selected = color_selected
        self.selected = False

    def draw(self):
        border = 3
        outline_rect = self.rect.inflate(border * 2, border * 2)  # Make a larger rect for the outline
        pygame.draw.rect(self.screen, (0, 0, 0), outline_rect)
        if self.selected:
            pygame.draw.rect(self.screen, self.color, self.rect)
        else:
            pygame.draw.rect(self.screen, self.color_selected, self.rect)

    def overlaps(self, x, y):
        return x > self.rect[0] and y > self.rect[1] and x < self.rect[0]+self.rect[2] and y < self.rect[1]+self.rect[3]
    
# Creates buttons with different choices
class ChoicePanel():
    def __init__(self, screen, y, choices : [str]):
        self.screen = screen
        self.y = y
        self.choices = choices
        self.selected = 1 # Selected choice index
        self.color_unselected = Colors.unselected
        self.color_hover = Colors.hover
        self.color_selected = Colors.selected
        self.height = 40

    # Draw all options in panel
    def draw(self):
        border = 1
        button_width = self.screen.get_width()/len(self.choices)
        button_height = self.height
        for i in range(0, len(self.choices)):
            x = i * button_width
            y = self.y
            w = button_width
            h = button_height
            rect = pygame.Rect(x, y, w, h)
            if i==self.selected:
                pygame.draw.rect(self.screen, self.color_selected, rect)
            else:
                pygame.draw.rect(self.screen, self.color_unselected, rect)
            text(self.screen, self.choices[i], x + button_width/2, y + button_height/2, Colors.black)

    # Handles mouse input
    def click(self, mouse_x, mouse_y):
        # Check inside all the tabs
        button_width = self.screen.get_width()/len(self.choices)
        button_height = self.height
        for i in range(0, len(self.choices)):
            x = i * button_width
            y = self.y
            w = button_width
            h = button_height
            rect = pygame.Rect(x, y, w, h)
            if rect.collidepoint(mouse_x, mouse_y):
                self.selected = i

    # Gets the value of the selected option
    def get_selected(self):
        return self.choices[self.selected]

# Useful method to quickly draw centered text on screen
def text(screen, string, x, y, color):
    font = pygame.font.Font(None, 24)
    text_color = pygame.Color(color)
    text_surface = font.render(string, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
