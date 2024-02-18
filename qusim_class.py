import numpy as np
import random 
import Gates

# Our quantum circuit manager
class Quantum:
    def __init__(self, qubit_count):
        self.qubit_count = qubit_count
        state_vector = np.array([1,0],dtype=complex)
        for i in range(0,qubit_count-1):
            state_vector = np.kron(state_vector, np.array([1,0],dtype=complex))
        self.state_vector = state_vector

    # We can create a collapsed vector corresponding to the qubit that we collapsed
    # Used to apply measurement to a qubit state matrix by setting collapses states to 0
    def collapsed_vector(self, single_qubit_state, qubit_index, qubit_count)->np.array:
        m = np.array([1, 1])
        vector = single_qubit_state if qubit_index == 0 else m
        for i in range(1, qubit_count):
            vector = np.kron(vector, single_qubit_state if i == qubit_index else m)
        return vector
    
    # Implementation of measurement algorithm for arbitrarily sized state matrix
    # Returns state as bit (0 or 1). Also collapses the matrix
    def measure(self, qubit_index)->int:
        # Matrices used to remove states from matrix
        m0 = self.collapsed_vector([1,0], qubit_index, self.qubit_count)
        m1 = self.collapsed_vector([0,1], qubit_index, self.qubit_count)
        # Probabilites for given qubit to be 0 or 1
        p0 = np.sum(np.abs(m0*self.state_vector)**2)
        p1 = np.sum(np.abs(m1*self.state_vector)**2)
        # Collapsing qubit based on probabilites p0 or p1
        p = np.random.choice([0,1], p=[p0,p1])
        # Set probability to 0 for all states where qubit is equal to 0
        measured_state = None
        if p==0:
            measured_state=m0*self.state_vector
        else:
            measured_state=m1*self.state_vector
        # Normalise the measurement to fulfill property |a|^2+|b|^2+...==1
        scaler = np.sqrt(np.sum(np.abs(measured_state)**2)) # Sum of the abs squares of matrix
        measured_state = measured_state/scaler # Divide by scaler so |sum of ^2| == 1
        self.state_vector = measured_state # Update state_vector
        return p # Returns probability of q_n=1 for qubit n

    # Applies gate
    # TODO This only handes 2x2 gates at the moment (single qubit)
    def applyGate(self, gate, qubit_index):
        # Expand gate to fit given qubit using identity matrix
        matrix = gate if qubit_index == 0 else Gates.I # initialize matrix correctly
        for i in range(1, self.qubit_count):
            if i == qubit_index:
                matrix = np.kron(matrix, gate)
            else:
                matrix = np.kron(matrix, Gates.I)
        # Multiply this new gate with the state_vector
        self.state_vector = matrix.dot(self.state_vector)

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
        # Multiply this new gate with the state_vector
        self.state_vector = matrix.dot(self.state_vector)

    # Gets alpha|0> beta|1> of a qubit
    # Returns a complex vector
    def getQubit(self, qubit_index)->np.array:
        qubit_count = int(np.log2(len(self.state_vector)))
        # Matrices used to remove states from matrix
        m0 = self.collapsed_vector([1,0], qubit_index, qubit_count)
        m1 = self.collapsed_vector([0,1], qubit_index, qubit_count)
        # Probabilites for given qubit to be 0 or 1
        alpha = np.sum(m0*self.state_vector)
        beta = np.sum(m1*self.state_vector)
        return np.array([alpha, beta])

    # Sets a given qubits probability vector
    # Input: vector = [alpha, beta]
    # Description: Applying a Pauli-X gate sets the qubit. We use tesnor product to select which qubit.
    def setQubit(self, qubit_index, vector):
        self.applyGate(Gates.X, qubit_index)

    # Sets the qubit state to a state vector (useful for debugging/ shortcuts)
    def setState(self, state_vector):
        self.qubit_count = int(np.log2(len(state_vector)))
        self.state_vector = state_vector


    # Helpful functions
    # ---------------------------------------------
    # Calculates sum(|q_state|^2)==1
    def totalProbability(self):
        return np.sum(np.abs(self.state_vector)**2)
    
    # Prints all qubits (useful for debugging)
    def printQubits(self):
        for i in range(0,self.qubit_count):
            print(f"Qubit {i}:{self.getQubit(i)}")

    # Converts alpha*|0>+beta*|1> to P(x, y, z)
    # Used for plotting on Bloch-sphere
    # Math from en.wikipedia.org/wiki/Bloch_sphere
    # TODO Research in how to plot on Q-sphere instead of Bloch
    def blochVector(self, alpha, beta)->list:
        u = complex(beta) / complex(alpha)
        ux = u.real
        uy = u.imag
        # Coordinates of point on Q-sphere
        px = (2*ux)/(1+ux**2+uy**2)
        py = (2*uy)/(1+ux**2+uy**2)
        pz = (1-ux**2-uy**2)/(1+ux**2+uy**2)
        return [px,py,pz]

# q = Quantum(2)
# q.applyGate(Gates.H, 0)
# q.applyGateQubits(Gates.CNOT, {0,1})
# print(q.measure(0))
# print(q.blochVector(0.5, 0.5))