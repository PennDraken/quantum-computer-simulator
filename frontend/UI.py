import pygame
import Utilities.mouse as mouse
import Utilities.Colors as Colors

grid_size = 90
gate_size = 70

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
        self.icons = [] # Empty list containing images for the different choices
        self.selected = 0 # Selected choice index
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
            # Draw text and icons
            if self.icons != []: # TODO center both icon and text on tab
                image = self.icons[i] # gets corresponsind image
                icon_width = self.height
                icon_rect = (x + self.height, y, icon_width, icon_width) # Note this rect does not scale icon
                # Text and image
                self.screen.blit(image, icon_rect)
                offset = icon_width
                text(self.screen, self.choices[i], x + button_width/2 + icon_width, y + button_height/2, Colors.black)
            else:
                # Just text
                text(self.screen, self.choices[i], x + button_width/2, y + button_height/2, Colors.black)

    # Sets images of choice panel (automatically scales to size)
    def set_icons(self, images):
        self.icons = []
        for image in images:
            scaled_image = pygame.transform.smoothscale(image, (self.height, self.height))
            self.icons.append(scaled_image)

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

# Useful method to quickly draw centered text on screen (Rotated 90 degrees)
def rotated_text(screen, string, x, y, color, bg_rect=False):
    # pygame.draw.circle(screen, Colors.white, (x, y), 40) # Uncomment this line to debug center of text
    font = pygame.font.Font(None, 24)
    text_color = pygame.Color(color)
    text_surface = font.render(string, True, text_color)
    text_rect = text_surface.get_rect(center=(x, y))
    rect_width = text_surface.get_height() + 10
    rect_height = text_surface.get_width() + 10
    rect = pygame.Rect(text_rect.centerx - rect_width // 2, text_rect.centery - rect_height // 2, rect_width, rect_height)
    if bg_rect:
        pygame.draw.rect(screen, (200, 200, 200), rect) # BG of text
    rotated_surface = pygame.transform.rotate(text_surface, 90)
    rotated_rect = rotated_surface.get_rect(center=text_rect.center)
    screen.blit(rotated_surface, rotated_rect.topleft)
    
# Draws a dashed line. Similar to pygames built in function
def draw_dashed_line(surface, color, start_pos, end_pos, width=2, dash_length=grid_size/10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    distance = max(abs(dx), abs(dy))
    dx_unit = dx / distance
    dy_unit = dy / distance
    dash_count = int(distance / dash_length)

    for i in range(dash_count):
        if i % 3 == 0:
            start = (round(x1 + i * dash_length * dx_unit),
                     round(y1 + i * dash_length * dy_unit))
            end = (round(x1 + (i + 1) * dash_length * dx_unit),
                   round(y1 + (i + 1) * dash_length * dy_unit))
            pygame.draw.line(surface, color, start, end, width)