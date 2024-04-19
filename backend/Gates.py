import numpy as np
import ast

# Stores the different gates TODO More gates
# Identity
I = np.array([[1,0],[0,1]]) 
# Pauli gates
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex) 
Z = np.array([[1,0],[0,-1]], dtype=complex) 
# Controlled gates
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
Toffoli = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1, 0]])
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

# def QFTinv(N):


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
    # TODO Dont use eval lol
    return eval(gate_str)

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

# Uses conditional phase shift to generate A
def A(n):
    gate=gen_I(n)
    for i in range(0,n):
        control_qubit = i
        target_qubit = n+1
        phase_shift=conditional_phase_shift(i+1) # Note i+1 goes from 1 to n
        # Move target qubit (also expands it)
        modified_phase_shift = gate_change_connections(phase_shift, control_qubit, target_qubit)
        # Apply gate
        gate = gate * modified_phase_shift
    return gate


def function_ax_mod_N(a,x,N):
    return (a*x)%N

def gate_a_mod_N(a,N):
    number_of_qubits = int(np.ceil(np.log2(N)))
    number_of_states = 2**number_of_qubits
    matrix = np.zeros((number_of_states, number_of_states))
    for col in range(number_of_states):
        row = function_ax_mod_N(a,col,N)
        matrix[row, col] = 1
    return matrix

def function_exponentiation(a,i,N):
    return (a**2**i)%N

def gate_Ua(a, i, N):
    number_of_qubits = int(np.ceil(np.log2(N)))
    number_of_states = 2**number_of_qubits
    matrix = np.zeros((number_of_states, number_of_states))
    for row in range(number_of_states):
        num_1 = function_exponentiation(a,i,N) * row
        col = num_1 % N
        print(f"state: {row} maps to {col}")
        matrix[row, col] = 1
    return matrix

# print(gate_a_mod_N(7,15))
print(gate_Ua(3,1,5))

# Grovers algorithm
# https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/grovers-algorithm
def grover_op(num_qubits, states : list[int]):
    """
    Description:
        This Grover operator combines oracle and amplifier into a single function.

    Input:
        num_qubits - Number of qubits in system
        states - List of integers, where the binary representation represents the states that we're searching for.
    
    Example:
        grover_op(3, [0b101])
    """
    small_val = 0.5**(num_qubits-1) # 2 qubits => 1/2, 3 qubits => 1/4, 4 qubits => 1/8, 5 qubits => 1/16 ...
    big_val   = 1-small_val # Big value is placed on diagonal
    N = 2**num_qubits # Columns and rows
    matrix = np.full((N, N), small_val)
    np.fill_diagonal(matrix, -big_val)
    # Flip target states columns
    for column in states:
        matrix[:, column] = -matrix[:, column] # Negates the column
    return matrix



def normalize(vector : np.array)->np.array:
        scaler = np.sqrt(np.sum(np.abs(vector)**2))
        new_vector = vector/scaler
        return new_vector

# -----------------------------------------------------------------------------
# GATE MODIFIERS
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
