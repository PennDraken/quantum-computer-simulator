import pygame

# Simple class for handling mouse input
class Mouse():
    x = 0 # Current x position of mouse
    y = 0 # Current y position of mouse
    last_x = 0 # Last frames position
    last_y = 0
    dx = 0 # Change in x between frames
    dy = 0 # Change in y between frames
    l_click = False # Only true at frame user presses l_click
    l_held = False  # Only true when button is held down
    status = None # Set this object to for example a string when the mouse interacts with a certain object. Gets reset on button release
    holding = None # Set this to object were holding (used for moving gates)
    r_click = False # Only true at frame user presses r_click
    r_held = False  # Only true when button is held down


    # Updates the mouse
    @staticmethod
    def update(self):
        # Update position
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        self.dx = self.x-self.last_x
        self.dy = self.y-self.last_y

        # Update button statuses
        # Check left click
        if pygame.mouse.get_pressed()[0]:
            if not self.l_held and not self.l_click:
                self.l_click = True
            else:
                self.l_click = False
                self.l_held = True
        else: # Mouse left released
            self.l_held = False
            self.l_click = False
            
        # Check right click
        if pygame.mouse.get_pressed()[2]:
            if not self.r_held and not self.r_click:
                self.r_click = True
            else:
                self.r_click = False
                self.r_held = True
        else: # Mouse right released
            self.r_held = False
            self.r_click = False

        # Update old position
        self.last_x = self.x
        self.last_y = self.y

        if not (pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]):
            self.status = None

    # Draws the mouse
    def draw():
        return