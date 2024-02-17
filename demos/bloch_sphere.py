# Draws a Bloch sphere
# ------------------------------------------------------

# Example file showing a circle moving on screen
import pygame
import numpy as np

# pygame setup
pygame.init()
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()
running = True
dt = 0

center_x=screen.get_width()/2
center_y=screen.get_height()/2
sphere_r=screen.get_width()/2
mouse_last_pos=None # Used for m

# Rotation angles of sphere
a = 0.1
a2 = 0 # horizontal

# Draws the 3D sphere
def draw_bloch(x, y, r, a):
    pygame.draw.ellipse(screen, pygame.Color("darkslategrey"), pygame.Rect(x-r,y-r,2*r,2*r), width=5) # could be cirlce instead
    n = 5
    for i in range(-n,n+1,2):
        s=(i)*(r/n)
        x1=x+np.sqrt(r**2-s**2)
        y1=y-s
        x2=x-np.sqrt(r**2-s**2)
        y2=y-s
        p1=rotate_point(x,y,x1,y1,a)
        p2=rotate_point(x,y,x2,y2,a)
        dx=np.sqrt(r**2-s**2)
        oval(x-dx,p1['y'],x+dx,p2['y'], pygame.Color("darkslategrey"))
        # print(p1['y'])

# Kind of unneccessary, just that the old code was implemented using oval(x1,y1,x2,y2) (not available in Pygame) instead of ellipse
# Draws an oval at rectangle of points P(x1,y1) to P(x2,y2)
def oval(x1, y1, x2, y2, color):
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    left = min(x1, x2)
    top = min(y1, y2)
    pygame.draw.ellipse(screen, color, (left, top, width, height), width=5)

# Plots a point at x,y,z
def plot_point(x,y,r,px,py,pz):
    np=ry(px,py,pz,a2)
    px=np['x']
    py=np['y']
    pz=np['z']
    p=rotate_point(x,y,x+pz,y+py,a)
    # Pointing outwards
    # if pz<0:
        # drawX(x+px, p['y'], 10, pygame.Color("coral4"))
    # Pointing towards
    if pz>0: # z axis is positive outside of screen (check if vector points towards viewpoint)
        r2=10
        pygame.draw.circle(screen, pygame.Color("gold3"), [x+px, p['y']], r2, width=5)

def plot_point_line(x,y,r,px,py,pz):
    np=ry(px,py,pz,a2)
    px=np['x']
    py=np['y']
    pz=np['z']
    p=rotate_point(x,y,x+pz,y+py,a)
    # Pointing outwards
    if pz<0:
        pygame.draw.line(screen, pygame.Color("gray20"), (x+px, p['y']), (x,y), width=1)
    # Pointing towards
    if pz>0: # z axis is positive outside of screen (check if vector points towards viewpoint)
        pygame.draw.line(screen, pygame.Color("gray20"), (x+px, p['y']), (x,y), width=5)

def plot_point_text(x,y,r,px,py,pz):
    np=ry(px,py,pz,a2)
    px=np['x']
    py=np['y']
    pz=np['z']
    p=rotate_point(x,y,x+pz,y+py,a)    
    # Pointing towards
    if pz>0: # z axis is positive outside of screen (check if vector points towards viewpoint)
        # Draw alpha beta values of point
        # We need to unrotate point to get its real values
        p_original = ry(px,py,pz, -a2)
        state = pointToAlphaBeta(p_original['x']/r, p_original['y']/r, p_original['z']/r) # scaling to unit sphere
        alpha = state[0]
        beta = state[1]
        text(f"{alpha:.2}*|0>+{beta:.2}*|1>", x+px, p['y']-20, "white")

# Draws a cross shape
def drawX(x,y, length, color):
    pygame.draw.lines(screen, color, True, [(x-length,y-length),(x+length,y+length)], 5)
    pygame.draw.lines(screen, color, True, [(x-length,y+length),(x+length,y-length)], 5)

# Rotate point around center coords
# Input: Center point=cx,cy point=x,y
def rotate_point(cx, cy, x, y, a):
    nx=cx+(x-cx)*np.cos(a)-(y-cy)*np.sin(a)
    ny=cy+(x-cx)*np.sin(a)+(y-cy)*np.cos(a)
    return {'x' : nx, 'y' : ny}

# Rotates around the y axis a degrees
def ry(x,y,z,a):
    xp=x*np.cos(a)+z*np.sin(a)
    yp=y
    zp=-x*np.sin(a)+z*np.cos(a)
    return {'x' : xp, 'y' : yp, 'z' : zp}

# Converts alpha beta values to a blochvector
def blochVector(alpha, beta)->list:
    u = complex(beta) / complex(alpha)
    ux = u.real
    uy = u.imag
    # Coordinates of point on unit sphere
    px = (2*ux)/(1+ux**2+uy**2)
    py = (2*uy)/(1+ux**2+uy**2)
    pz = (1-ux**2-uy**2)/(1+ux**2+uy**2)
    return np.array([px,py,pz])

def pointToAlphaBeta(px, py, pz):
    # Solve equations to find alpha and beta
    uy = (2 * py) / (1 - pz)
    ux = (2 * px) / (1 - pz)
    beta = uy + 1j * ux
    alpha = 1 / np.sqrt(1 + np.abs(beta) ** 2)
    return np.array([alpha, beta])

# Used to generate some random points
def random_point_on_unit_sphere():
    theta = np.random.uniform(0, 2*np.pi)
    phi = np.random.uniform(0, np.pi)
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    return np.array([x, y, z])

# Useful method to quickly draw text on screen
def text(string, x, y, color):
    font = pygame.font.Font(None, 24)
    text_color = pygame.Color(color)
    text_surface = font.render(string, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Generates some random points on sphere
points = []
for i in range(0,5):
    p = random_point_on_unit_sphere()
    p = p*sphere_r
    points.append(p)

# Game loop
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # draw sphere
    draw_bloch(center_x,center_y,sphere_r,a)

    # draw points (theyre seperated to layers so points are always drawn over lines, (depth))
    for p in points:
        plot_point_line(center_x,center_y,sphere_r,p[0],p[1],p[2])

    for p in points:
        plot_point(center_x,center_y,sphere_r,p[0],p[1],p[2])

    for p in points:
        plot_point_text(center_x,center_y,sphere_r,p[0],p[1],p[2])


    # Input WASD to rotate sphere
    delta_angle = 0.015 # Velocity of angle change
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        a = (a + delta_angle) % (2 * np.pi)
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        a = (a - delta_angle) % (2 * np.pi)
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        a2 = (a2 - delta_angle) % (2 * np.pi)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        a2 = (a2 + delta_angle) % (2 * np.pi)

    # rotate with mouse
    if pygame.mouse.get_pressed()[0]:
        # find difference between old and new
        curr_pos = pygame.mouse.get_pos()
        if mouse_last_pos != None:
            delta_pos = np.array(curr_pos) - np.array(mouse_last_pos)
            # moving mouse across half screen should rotate sphere 1/4 turn = 1/2 pi=>1 width = 1pi | screen/f=pi f=screen/pi
            factor = 2*sphere_r/np.pi
            delta_angle_x = delta_pos[0]/factor
            delta_angle_y = delta_pos[1]/factor
            a2 = (a2 + delta_angle_x) % (2 * np.pi)
            a = (a + delta_angle_y) % (2 * np.pi)
        mouse_last_pos = curr_pos
    else:
        mouse_last_pos = None

    # Automatic rotation
    # a = (a+0.01)%(2*np.pi)
    # a2 = (a2+0.01)%(2*np.pi)
    text(str(int(clock.get_fps())), 10, 10, "white")
    pygame.display.flip() # Draw screen
    dt = clock.tick(60) / 1000


pygame.quit()