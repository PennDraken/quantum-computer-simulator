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

# Generates an identity matrix of size qubit count
def gen_I(qubit_count):
    gate = I
    for i in range(1,qubit_count):
        gate = np.kron(gate,I)
    return gate

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


def conditional_phase_shift(k : int):
    #return np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,5]])
    return np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,(np.e**((2*np.pi*1j) / (2**k)))]])




# Moves qubits by swapping indices and expanding (note gate is a 2 qubit gate)
def gate_change_connections(gate: np.array, qubit_a, qubit_b):
    # Expand gate
    qubit_count = qubit_b + 1
    gate = expand_gate(gate, qubit_a, qubit_count)
    output_gate = gate # Copy contents to allow for swapping
    # Move qubits
    for i in range(0, len(gate)):
        new_index = swap_bits(i, qubit_a + 1, qubit_b, qubit_count) # Swap index right of qubit a to qubit b location
        output_gate[new_index] = gate[i]
    return output_gate

# Swaps bits located at i and j
# swaps bits (most significant bit has index 0, least significant has index n)
def swap_bits(num: int, i: int, j: int, n: int):
    # Extract the bits at positions i and j
    bit_i = (num >> (n - 1 - i)) & 1
    bit_j = (num >> (n - 1 - j)) & 1
    # XOR the bits to swap them
    xor_result = bit_i ^ bit_j
    # Use XOR to flip the bits at positions i and j
    num ^= (xor_result << (n - 1 - i)) | (xor_result << (n - 1 - j))
    return num

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

def combine_gates(i : int, n):
     gate_i = np.array([])
     state1 = True
     for k in range(i):
       if state1:
         gate_i = expand_gate(conditional_phase_shift(i-k), i, n +1)
         #print(gate_i)
         state1 = False
       else:
         gate_i = np.matmul(gate_i, expand_gate(conditional_phase_shift(i-k), i, n +1))
     return gate_i

#--------------------------------------------ADD-----------------------------------------------
# constructs the full add gate where a = size of register a 
def add_calc_gate( a : int):
    len_a = a
    gate_a = np.array([])
    add_gate = np.array([])
    for i in range( 0, len_a ):
        # A( stair_h, stair_w ) combining "stairsteps" from 1 to stair_w, ends with stair_w = 1
        gate_a = A( len_a + 1, (len_a - i) ) 
        print(len ( gate_a ) )
        # fill under A
        if(i != len_a -1):
          gate_a = np.kron( gate_a, gen_I( len_a - 1 - i ) )
        print(len ( gate_a ) )
        # fill above A
        if(i != 0):
          gate_a = np.kron( gen_I( i ) , gate_a )
        print(len ( gate_a ) )
        # modify add gate by current A
        print(len ( gate_a ) )
        if (i == 0):
            add_gate = gate_a
        else:
            add_gate = gate_a * add_gate 
    return add_gate

# Uses conditional phase shift to generate A
def A(stair_h : int, stair_w : int):
    gate=gen_I(stair_h)
    for i in range(1,stair_w + 1):
        control_qubit = i - 1 # upper "connected" index
        target_qubit = stair_h # index of the gate box 
        phase_shift=conditional_phase_shift(i) 
        # Move target qubit (also expands it) -> -1 since phase_shift is 4x4
        modified_phase_shift = gate_change_connections(phase_shift, control_qubit, target_qubit - 1)
        # Apply gate
        gate = gate * modified_phase_shift
    return gate

a = 2
add_a = add_calc_gate(a)
print(len(add_a))
#print(add_a)

for i in range(0, len(add_a)):
    row = np.array([])
    for j in range(len(add_a)):
        if (add_a[i][j] == 0.0000000e+00+0.j):
            row = np.append(row, 0)
        elif (add_a[i][j] == 1.0000000e+00+0.j):
            row = np.append(row, 1)
        else:
             row = np.append(row, str(add_a[i][j]))       
    print(row)
