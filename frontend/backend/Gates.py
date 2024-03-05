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
def QFT(N : int)->np.array:
    #W = np.power(np.e, np.complex(-2* np.pi))
    W = np.power(np.e, (2 * np.pi*1j)/N)
    constant = 1/np.sqrt(N)
    Matrix = np.ones((N,N), dtype= complex)
    n = int(N/2)
    for n in range(1,N):
        for m in range(1, N):
            temp = np.power(W, n * m)
            Matrix[n][m] = temp
            #Matrix[m][n] = temp
    #print(Matrix[3][3])
    Matrix *= constant

QFT(4)
def DFT(N : int)-> np.array:
    W = np.power(np.e, (-2 * np.pi*1j)/N)
    constant = 1/np.sqrt(N)
    Matrix = np.ones((N,N), dtype= complex)
    for n in range(1,N):
        for m in range(1, N):
            Matrix[n][m] = np.power(W, n * m)
    Matrix *= constant
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
