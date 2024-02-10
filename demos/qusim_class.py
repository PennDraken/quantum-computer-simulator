import numpy as np
import random 

# Our quantum circuit manager
class Quantum:
    def __init__(self, qubit_count):
        self.qubit_count = qubit_count
        # self.state_matrix = np.zeros(2**qubit_count, dtype=complex) # vector representing the probability state of the systems qubits
        state_matrix = np.array([1,0],dtype=complex)
        for i in range(0,qubit_count-1):
            state_matrix = np.kron(state_matrix, np.array([1,0],dtype=complex))
        self.state_matrix = state_matrix

    # We can create a collapsed vector corresponding to the qubit that we collapsed
    # Used to apply measurement to a qubit state matrix by setting collapses states to 0
    def collapsed_vector(self, single_qubit_state, qubit_index, qubit_count)->np.array:
        m = np.array([1,1])
        if qubit_index==0:
            vector = single_qubit_state
        else:
            vector = m
        for i in range(1, qubit_count):
            if i == qubit_index:
                vector = np.kron(vector, single_qubit_state)
            else:
                vector = np.kron(vector, m)
        return vector
    
    # Implementation of measurement algorithm for arbitrarily sized state matrix
    def measure(self, qubit_index):
        qubit_count = int(np.log2(len(self.state_matrix)))
        # Matrices used to remove states from matrix
        m0 = self.collapsed_vector([1,0], qubit_index, qubit_count)
        m1 = self.collapsed_vector([0,1], qubit_index, qubit_count)
        # Probabilites for given qubit to be 0 or 1
        p0 = np.sum(np.abs(m0*self.state_matrix)**2)
        p1 = np.sum(np.abs(m1*self.state_matrix)**2)
        # Collapsing qubit based on probabilites p0 or p1
        p = np.random.choice([0,1], p=[p0,p1])
        # Set probability to 0 for all states where qubit is equal to 0
        measured_state = None
        if p==0:
            measured_state=m0*self.state_matrix
        else:
            measured_state=m1*self.state_matrix
        # Normalise the measurement to fulfill property |a|^2+|b|^2+...==1
        scaler = np.sqrt(np.sum(np.abs(measured_state)**2)) # Sum of the abs squares of matrix
        measured_state = measured_state/scaler # Divide by scaler so |sum of ^2| == 1
        self.state_matrix = measured_state # Update state_matrix
    
    # Applies gate
    # TODO This only handes 2x2 gates at the moment (single qubit)
    def applyGate(self, gate, qubit_index):
        # Expand gate to fit given qubit using identity matrix
        if qubit_index==0:
            matrix = gate
        else:
            matrix = Gates.I
        for i in range(1, self.qubit_count):
            if i == qubit_index:
                matrix = np.kron(matrix, gate)
            else:
                matrix = np.kron(matrix, Gates.I)
        # Multiply this new gate with the state_matrix
        self.state_matrix = matrix.dot(self.state_matrix)

    # Applies gate to multiple qubits
    # TODO Probably somewhat buggy with different matrix sizes
    # TODO Overload other apply gate to handle list of indices + single indices
    def applyGateQubits(self, gate, qubit_index_arr):
        if 0 in qubit_index_arr:
            matrix = gate
        else:
            matrix = Gates.I
        for i in range(int(np.log2(len(gate))), self.qubit_count):
            if i in qubit_index_arr:
                matrix = np.kron(matrix, gate)
            else:
                matrix = np.kron(matrix, Gates.I)
        # Multiply this new gate with the state_matrix
        self.state_matrix = matrix.dot(self.state_matrix)

# Stores the different gates
class Gates:
    # Identity
    I = np.array([[1,0],[0,1]], dtype=complex) 
    # Pauli gates
    X = np.array([[0,1],[1,0]], dtype=complex)
    Y = np.array([[0,-1j],[1j,0]], dtype=complex) 
    Z = np.array([[1,0],[0,-1]], dtype=complex) 
    # Controlled gates
    CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
    # Hadamard gate
    H = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)
    # Swap gate
    SWAP = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], dtype=complex)

# Bell state demo
q = Quantum(2) # Create 2 qubits
q.applyGate(Gates.H, 0) # Apply Hadamard to qubit 0
print(f"Hadamard applied to first qubit \n {q.state_matrix}")

q.applyGateQubits(Gates.CNOT, [0,1]) # Apply CNOT to qubit 0 and 1
print(f"CNOT applied to both qubits \n {q.state_matrix}")

q.measure(0) # Measure qubit 0
print(f"Qubit 0 measured \n {q.state_matrix}")