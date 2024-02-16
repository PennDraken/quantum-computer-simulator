# Draws a Bloch sphere
# ------------------------------------------------------

# Example file showing a circle moving on screen
import pygame
import numpy as np

# pygame setup
pygame.init()
screen = pygame.display.set_mode((512, 512))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Rotation angles of sphere
a = np.pi/3
a2 = 0

# Draws the 3D sphere
def draw_bloch(x, y, r, a):
    pygame.draw.ellipse(screen, "navy", pygame.Rect(x-r,y-r,2*r,2*r), width=1)
    n = 10
    for i in range(-n,n+1,2):
        s=(i)*(r/n)
        x1=x+np.sqrt(r**2-s**2)
        y1=y-s
        x2=x-np.sqrt(r**2-s**2)
        y2=y-s
        p1=rotate_point(x,y,x1,y1,a)
        p2=rotate_point(x,y,x2,y2,a)
        dx=np.sqrt(r**2-s**2)
        oval(x-dx,p1['y'],x+dx,p2['y'],"white")
        # print(p1['y'])

def oval(x1, y1, x2, y2, color):
    # Calculate width and height
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    # Determine the top-left coordinates for the ellipse
    left = min(x1, x2)
    top = min(y1, y2)
    # Call the ellipse function
    pygame.draw.ellipse(screen, color, (left, top, width, height), width=1)

# Rotate point around center coords
# Input: Center point=cx,cy point=x,y
def rotate_point(cx, cy, x, y, a):
    nx=cx+(x-cx)*np.cos(a)-(y-cy)*np.sin(a)
    ny=cy+(x-cx)*np.sin(a)+(y-cy)*np.cos(a)
    return {'x' : nx, 'y' : ny}

# Game loop
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    draw_bloch(256,256,128,a)
    
    # Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    a = (a+0.01)%(2*np.pi)
    pygame.display.flip() # Draw screen
    dt = clock.tick(60) / 1000


pygame.quit()