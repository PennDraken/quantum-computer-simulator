import numpy as np
# Stores the different gates TODO More gates
# Identity
I = np.array([[1,0],[0,1]]) 
# Pauli gates
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex) 
Z = np.array([[1,0],[0,-1]], dtype=complex) 
# Controlled gates
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
# Hadamard gate
H = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)
# Swap gate
SWAP = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
zero_state = np.array([1,0])
# zero_state = 1/np.sqrt(2)*np.array([1,1j], dtype=complex)
one_state = np.array([0,1])

# TODO Name to something more intuitive
# Vector that coreresponds to the states that are searched for
def collapsed_vector(single_qubit_state, qubit_index, qubit_count)->np.array:
    m = np.array([1, 1])
    vector = single_qubit_state if qubit_index == 0 else m
    for i in range(1, qubit_count):
        vector = np.kron(vector, single_qubit_state if i == qubit_index else m)
    return vector

def Rx(theta)->np.array:
    return np.array([[np.cos(theta/2), -1j*np.sin(theta/2)],
                     [-1j*np.sin(theta/2), np.cos(theta/2)]], dtype=complex)

def Ry(theta):
    return np.array([[np.cos(theta/2), -np.sin(theta/2)],
                     [np.sin(theta/2), np.cos(theta/2)]], dtype=complex)

# Generates a Quantum Fourier Transform matrix
def QFT(N : int)->np.array:
    W = np.power(np.e, (2 * np.pi*1j)/N)
    constant = 1/np.sqrt(N)
    Matrix = np.ones((N,N), dtype= complex)
    for n in range(N):
        for m in range(n, N):
            value = np.power(W, n * m)
            Matrix[n][m] = value
            Matrix[m][n] = value
    Matrix *= constant
    return Matrix
def DFT(N : int)-> np.array:
    W = np.power(np.e, (-2 * np.pi*1j)/N)
    constant = 1/np.sqrt(N)
    Matrix = np.ones((N,N), dtype= complex)
    for n in range(N):
        for m in range(n, N):
            value = np.round(np.power(W, n * m), 5)
            Matrix[n][m] = value
            Matrix[m][n] = value
    Matrix *= constant
    return Matrix

# gets corresponding gate from a gate_str
def string_to_gate(gate_str : str):
    # TODO More programmatic approach, perhaps dictionaries or eval()
    match gate_str:
        case "H":
            return H
        case "I":
            return I
        case "CNOT":
            return CNOT
        case "Y":
            return Y
        case "X":
            return X
        case "Z":
            return Z
        case "Ry(np.pi/4)": # TODO parse actual value
            return Ry(np.pi/4)
        case _ :
            return None # TODO Error

def checkIfCoprime(a, b)->bool: # Checks if two numbers are coprime, i.e. their greatest common divisor is 1, i.e. gcd(a,b) = 1
    while b != 0:
        a, b = b, a % b
    return a # If a is 1, then a and b are coprime

def checkIfNOdd(n : int)->bool:
    return n % 2 != 0

def find_n(N: int)->int:
    return int(np.ceil(np.log2(N)))

# This is the function we want the quantum subroutine to find. This is a working example in classical code potentially.
def findPeriod(a, N)->int: # Finds the period of a function f(x) = a^x mod N
    for r in range(a, N):
        if a**r % N == 1:
            return r
    return None

def amodNStrings(a: int, N: int)->np.array:
    if not 1 < a < N or not checkIfNOdd(N):
        return None
    
    if checkIfCoprime(a, N) != 1: # If a and N are not coprime, then we a is a factor of N
        return N/a # Returns the other factor of N
    
    strings = []
    for i in range(0, 2*find_n(N)): # 2n iterations
        x = 2**(i)      
        strings.append(f"{a}^{x} mod {15}")   
    return strings # return ['7^1 mod 15', '7^2 mod 15', '7^4 mod 15', '7^8 mod 15', '7^16 mod 15', '7^32 mod 15', '7^64 mod 15', '7^128 mod 15']

# Function that is used to verify amod?
def fabian_print():
    a = 7
    N = 15
    print(amodNStrings(a, N))
    a_inv = pow(a, -1, N)
    print(a_inv)  # 13
    print(a * a_inv)  # 91
    print(a * a_inv % N)  # 1
    print(amodN(7, 15))

def controlled_mul_amodN(a, N)->np.array:
    gate = np.zeros((N, N), dtype=complex)
    return -1

def controlled_swap(n)->np.array:
    #qusim_class.swap(, )
    I = np.eye((2), dtype=complex)
    SWAP = np.array([[1, 0, 0, 0],
                     [0, 0, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1]])
    matrix = np.zeros((n,n), dtype=complex)
    if n == 0:
        matrix = np.kron(np.kron(I, I), I)
    elif n == 1:
        matrix = np.kron(np.kron(I, SWAP), I)
    else:
        matrix = np.kron(np.kron(SWAP, I), I)
    return matrix
    
def add_control_qubit(matrix):
  m, n = matrix.shape
  new_matrix = np.hstack((np.eye(m, n), np.zeros((m, n), dtype=complex)))
  new_matrix = np.vstack((new_matrix, np.hstack((np.zeros((m, n)), matrix), dtype=complex)))
    
  return new_matrix

def amodN(a, N)->np.array:
    return controlled_mul_amodN(a, N)*controlled_swap(N)*controlled_mul_amodN(pow(a, -1, N), N)


def expand_gate(gate, index, qubit_count):
    # Check that gate fits at given index
    width = int(np.log2(len(gate)))
    assert index+width-1 < qubit_count, "Error! Gate does not fit"
    if index == 0:
        expanded_gate = gate
        i = width  # start position
        while i < qubit_count:
            expanded_gate = np.kron(expanded_gate, I)
            i += 1
    else:
        expanded_gate = I
        i = 1
        while i < qubit_count:
            if i == index:
                expanded_gate = np.kron(expanded_gate, gate)
                i += width  # increment counter by size of gate
            else:
                expanded_gate = np.kron(expanded_gate, I)
                i += 1
    return expanded_gate


def generateConditional(k : int):
    #return np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,5]])
    return np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,(np.e**((2*np.pi*1j) / (2**k)))]])

# can use for other gates too   
def conditional_auto_swap(gate, q1):
     gate_1 = expand_gate(gate, 0, q1 +1)
     for i in range(1, q1):
         expanded_swap = expand_gate(SWAP, i, q1 +1)
         #print(expanded_swap)
         gate_1 = np.dot(gate_1, expanded_swap)
     for i in range(q1 - 1, 0 ,-1):
         expanded_swap = expand_gate(SWAP, i, q1 +1)  
         gate_1 = np.dot(gate_1, expanded_swap)
     return gate_1



def testSwap():
    gate = CNOT
    temp = np.dot(SWAP, gate)
    temp_2 = np.dot(temp, SWAP)
    print(temp_2)


