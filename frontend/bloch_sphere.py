# Draws a Bloch sphere
# ------------------------------------------------------
# Example file showing a circle moving on screen
import pygame
import numpy as np

# Draws the 3D sphere
def draw_bloch(screen, x, y, r, a, a2):
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
        oval(screen, x-dx,p1['y'],x+dx,p2['y'], pygame.Color("darkslategrey"))
        # print(p1['y'])

# Kind of unneccessary, just that the old code was implemented using oval(x1,y1,x2,y2) (not available in Pygame) instead of ellipse
# Draws an oval at rectangle of points P(x1,y1) to P(x2,y2)
def oval(screen, x1, y1, x2, y2, color):
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    left = min(x1, x2)
    top = min(y1, y2)
    pygame.draw.ellipse(screen, color, (left, top, width, height), width=5)

# Plots a point at x,y,z
def plot_point(screen, x,y,r,px,py,pz, a, a2):
    np=ry(px,py,pz,a2)
    px=np['x']
    py=np['y']
    pz=np['z']
    p=rotate_point(x,y,x+pz,y+py,a)
    # Pointing outwards
    # if pz<0:
        # drawX(x+px, p['y'], 10, pygame.Color("coral4"))
    # Pointing towards
    if pz>=0: # z axis is positive outside of screen (check if vector points towards viewpoint)
        r2=10
        pygame.draw.circle(screen, pygame.Color("gold3"), [x+px, p['y']], r2, width=5)

def plot_point_line(screen, x,y,r,px,py,pz, a, a2):
    np=ry(px,py,pz,a2)
    px=np['x']
    py=np['y']
    pz=np['z']
    p=rotate_point(x,y,x+pz,y+py,a)
    # Pointing outwards
    if pz<0:
        pygame.draw.line(screen, pygame.Color("gray20"), (x+px, p['y']), (x,y), width=1)
    # Pointing towards
    else: # z axis is positive outside of screen (check if vector points towards viewpoint)
        pygame.draw.line(screen, pygame.Color("gray20"), (x+px, p['y']), (x,y), width=5)

def plot_point_text(screen, x,y,r,px,py,pz, a, a2):
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
        text(screen, f"{alpha:.2}*|0>+{beta:.2}*|1>", x+px, p['y']-20, "white")

# Draws a cross shape
def drawX(screen, x, y, length, color, a, a2):
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
def state_to_point(alpha, beta)->list:
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
def text(screen, string, x, y, color):
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
    # p = p * sphere_r
    points.append(p)

class Bloch_Sphere():
    def __init__(self, screen, x, y, w, h):
        self.screen=screen
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.a=0.1
        self.a2=0
        self.sphere_r =  min(w, h)/2
        self.points = []

    def add_random_point_on_unit_sphere(self):
        theta = np.random.uniform(0, 2*np.pi)
        phi = np.random.uniform(0, np.pi)
        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(phi)
        self.points.append(np.array([x, y, z]))

    def add_point(self, x, y, z):
        point = np.array([x, y, z])
        self.points.append(point)

    # Draws the Bloch sphere with vectors etc
    def draw(self):
        self.h = self.screen.get_height() - self.y
        center_x = self.x + self.screen.get_width()/2
        center_y = self.y + self.h/2
        self.sphere_r = min(self.w, self.h)/2
        # draw sphere
        draw_bloch(self.screen, center_x, center_y, self.sphere_r, self.a, self.a2)

        # draw points (theyre seperated to layers so points are always drawn over lines, (depth))
        for p in self.points:
            plot_point_line(self.screen, center_x,center_y, self.sphere_r,p[0]*self.sphere_r,p[1]*self.sphere_r,p[2]*self.sphere_r, self.a, self.a2)

        for p in self.points:
            plot_point(self.screen, center_x,center_y, self.sphere_r,p[0]*self.sphere_r,p[1]*self.sphere_r,p[2]*self.sphere_r, self.a, self.a2)

        # for p in self.points:
            # plot_point_text(self.screen, center_x,center_y, self.sphere_r,p[0]*self.sphere_r,p[1]*self.sphere_r,p[2]*self.sphere_r, self.a, self.a2)

    # Sets the state from a rgister
    # Q-sphere uses hamming distance to find distance 
    def set_register(self, register):
        """self.points = []
        point = np.array([0,0,1])
        self.points.append(point)
        point = np.array([0,1,0])
        self.points.append(point)
        point = np.array([1,0,0])
        self.points.append(point)
        point = np.array([0,-1,0])
        self.points.append(point)"""

        self.points = []
        vector = register.vector
        max_number = 2**len(register.vector)-1 # |11111> All 1s
        max_distance = self.binary_hamming(0, max_number)
        # convert register to points
        for i,state in enumerate(vector):
            probability = np.abs(state)**2
            if probability==0:
                continue

            distance = self.binary_hamming(i, max_number)
            # normalise
            distance_norm = 1 - (distance / max_distance) # 1 - to flip rotation

            theta = distance_norm * np.pi # Vertical movement
            x = 0
            y = np.round(np.cos(theta),2)
            z = np.round(np.sin(theta),2)
            point = np.array([x,y,z])
            self.points.append(point)

    def binary_hamming(self, num1, num2):
        # Convert numbers to binary strings
        binary_str1 = bin(num1)[2:]
        binary_str2 = bin(num2)[2:]
        # Make binary strings of equal length by padding with zeros
        max_length = max(len(binary_str1), len(binary_str2))
        binary_str1 = binary_str1.zfill(max_length)
        binary_str2 = binary_str2.zfill(max_length)
        # Calculate Hamming distance
        hamming_distance = sum(ch1 != ch2 for ch1, ch2 in zip(binary_str1, binary_str2))
        return hamming_distance

    def pan(self, mouse):
        if mouse.l_held:
            # moving mouse across half screen should rotate sphere 1/4 turn = 1/2 pi=>1 width = 1pi | screen/f=pi f=screen/pi
            factor = 2*self.sphere_r/np.pi
            delta_angle_x = mouse.dx/factor
            delta_angle_y = mouse.dy/factor
            self.a2 = (self.a2 + delta_angle_x) % (2 * np.pi)
            self.a = (self.a + delta_angle_y) % (2 * np.pi)