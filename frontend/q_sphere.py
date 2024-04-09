# Draws a Bloch sphere
# ------------------------------------------------------
# Example file showing a circle moving on screen
import pygame
import numpy as np
from UI import Colors

# Draws the 3D sphere
def draw_bloch(screen, x, y, r, a, a2, lines):
    pygame.draw.ellipse(screen, Colors.dark_gray, pygame.Rect(x-r,y-r,2*r,2*r), width=5) # could be cirlce instead
    n = lines
    for i in range(-n,n+1,2):
        s=(i)*(r/n)
        x1=x+np.sqrt(r**2-s**2)
        y1=y-s
        x2=x-np.sqrt(r**2-s**2)
        y2=y-s
        p1=rotate_point(x,y,x1,y1,a)
        p2=rotate_point(x,y,x2,y2,a)
        dx=np.sqrt(r**2-s**2)
        oval(screen, x-dx,p1['y'],x+dx,p2['y'], Colors.dark_gray)
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
def plot_point(screen, x,y,r,px,py,pz, a, a2, point_radius):
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
        pygame.draw.circle(screen, Colors.yellow, [x+px, p['y']], point_radius, width=5)

def plot_point_line(screen, x,y,r,px,py,pz, a, a2):
    np=ry(px,py,pz,a2)
    px=np['x']
    py=np['y']
    pz=np['z']
    p=rotate_point(x,y,x+pz,y+py,a)
    # Pointing outwards
    if pz<0:
        pygame.draw.line(screen, Colors.gray, (x+px, p['y']), (x,y), width=1)
    # Pointing towards
    else: # z axis is positive outside of screen (check if vector points towards viewpoint)
        pygame.draw.line(screen, Colors.gray, (x+px, p['y']), (x,y), width=5)

def plot_point_text(screen, x,y,r,px,py,pz, a, a2, string : str):
    np=ry(px,py,pz,a2)
    px=np['x']
    py=np['y']
    pz=np['z']
    p=rotate_point(x,y,x+pz,y+py,a)    
    # Pointing towards
    if pz>=0: # z axis is positive outside of screen (check if vector points towards viewpoint)
        # Draw alpha beta values of point
        # We need to unrotate point to get its real values
        p_original = ry(px,py,pz, -a2)
        state = pointToAlphaBeta(p_original['x']/r, p_original['y']/r, p_original['z']/r) # scaling to unit sphere
        alpha = state[0]
        beta = state[1]
        # pygame.draw.rect(screen, Colors, (x+px, p['y']-20, ))
        text(screen, string, x+px, p['y']-20, "white")

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

# Represents the states of a system
class State():
    def __init__(self, coords_vector : np.array, label : str, probability, phase):
        self.coords_vector=coords_vector
        self.label=label
        self.probability=probability
        self.phase=phase

points = []

class Q_Sphere():
    def __init__(self, screen, x, y, w, h):
        self.screen=screen
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.a=0.1 # Angles
        self.a2=0
        self.sphere_r =  min(w, h)/2 
        self.states = []
        self.latitudal_lines = 4
        
    def add_random_point_on_unit_sphere(self):
        theta = np.random.uniform(0, 2*np.pi)
        phi = np.random.uniform(0, np.pi)
        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(phi)
        self.states.append(np.array([x, y, z]))

    def add_point(self, x, y, z):
        point = np.array([x, y, z])
        self.states.append(point)

    # Draws the Bloch sphere with vectors etc
    def draw(self):
        self.w = self.screen.get_width()
        self.h = self.screen.get_height() - self.y
        center_x = self.x + self.screen.get_width()/2
        center_y = self.y + self.h/2
        self.sphere_r = min(self.w, self.h)/2 - 20 # 20 is padding
        # draw sphere
        draw_bloch(self.screen, center_x, center_y, self.sphere_r, self.a, self.a2, self.latitudal_lines)

        # draw points (theyre seperated to layers so points are always drawn over lines, (depth))
        for state in self.states:
            p = state.coords_vector
            plot_point_line(self.screen, center_x,center_y, self.sphere_r,p[0]*self.sphere_r,p[1]*self.sphere_r,p[2]*self.sphere_r, self.a, self.a2)

        for state in self.states:
            p = state.coords_vector
            plot_point(self.screen, center_x,center_y, self.sphere_r,p[0]*self.sphere_r,p[1]*self.sphere_r,p[2]*self.sphere_r, self.a, self.a2, state.probability * (self.sphere_r/5))

        for state in self.states:
            p = state.coords_vector
            plot_point_text(self.screen, center_x,center_y, self.sphere_r,p[0]*self.sphere_r,p[1]*self.sphere_r,p[2]*self.sphere_r, self.a, self.a2, state.label)

    # Sets the states shown on q-sphere by providing a register containting state vector
    # Q-sphere uses hamming distance to find distance 
    def set_register(self, register):
        self.states = []
        vector = register.vector
        max_number = len(register.vector) - 1 # Maximum index reached
        max_distance = binary_hamming(0, max_number)
        self.latitudal_lines = max_distance

        # convert register to points
        for i,state in enumerate(vector):
            # only plot states with probability higher than 0%
            probability = np.abs(state)**2
            if probability==0:
                continue
            
            # latitude
            distance = binary_hamming(i, max_number)
            # normalise TODO align to latitudes instead of theta
            distance_norm = (distance / max_distance) # 1 - to flip rotation
            theta = distance_norm * np.pi # Vertical movement

            # longitude TODO fix this calculation
            # longitudal_lines = 2 ** distance - 1 # This is the amount of longitudal lines at this location.
            # longitudal_lines = unique_binary_numbers(count_ones(i), len(register.qubits)) # Finds the permutations of longitudes.
            outcomes = generate_binary_numbers(count_ones(i), len(register.qubits))
            longitudal_pos = outcomes.index(i)
            
            if len(outcomes) != 0:
                phi = longitudal_pos/len(outcomes) * (2 * np.pi) # Calculate phi by finding fraction of index.
            else:
                phi = 0 # Div by zero error when distance is 0

            # create point (note: some axes are not drawn according to mathematical convention, due to computer x, y, z screen conventions)
            x = np.sin(theta) * np.cos(phi) # conventional x
            y = np.round(np.cos(theta),2) # conventional z
            z = np.round(np.sin(theta) * np.sin(phi),2) # conventional y
            point = np.array([x,y,z])
            label = f"|{bin(i)[2:].zfill(len(register.qubits))}>" # Example: |1101>
            state = State(point, label, probability, 0)
            self.states.append(state)

    

    def pan(self, mouse):
        if mouse.l_held:
            # moving mouse across half screen should rotate sphere 1/4 turn = 1/2 pi=>1 width = 1pi | screen/f=pi f=screen/pi
            factor = 2*self.sphere_r/np.pi
            delta_angle_x = mouse.dx/factor
            delta_angle_y = mouse.dy/factor
            self.a2 = (self.a2 + delta_angle_x) % (2 * np.pi)
            self.a = (self.a + delta_angle_y) % (2 * np.pi)

def unique_binary_numbers(n, N):
    """
    Calculate the number of unique binary numbers with n positive bits out of N total bits.
    
    Parameters:
        n (int): Number of positive bits.
        N (int): Total number of bits.
    
    Returns:
        int: Number of unique binary numbers.
    """
    if n > N:
        return 0
    
    binomial_coefficient = np.math.comb(N, n)
    return binomial_coefficient * (2 ** n)

# Finds hamming distance between two numbers
def binary_hamming(num1, num2):
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

def generate_binary_numbers(n, N):
    """
    Generate a list of integers with n positive bits placed in the first N bits.
    
    Parameters:
        n (int): Number of positive bits.
        N (int): Total number of bits.
    
    Returns:
        list: List of integers with n positive bits placed in the first N bits.
    """
    if n > N:
        return []

    result = []
    for i in range(2**N):
        if count_ones(i) == n:
            result.append(i)
    return result

# Counts the amount of binary 1s in an integer
def count_ones(number):
    count = 0
    while number:
        count += number & 1
        number >>= 1
    return count

