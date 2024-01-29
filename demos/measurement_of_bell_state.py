import numpy as np
import random

# reduces the probability matrix to a single state
def measure(state_matrix : np.array)->np.array:
    weights = np.absolute(state_matrix)**2 # probability weights
    state_index = np.random.choice(len(state_matrix), p=weights)
    collapsed_state = np.zeros(len(state_matrix)) # create vector padded with zeros
    collapsed_state[state_index] = 1 # place 1 at corresponding state
    return collapsed_state

# gates initialization
cnot_gate = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
hadamard_gate = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)

# qubits
qubit1_state = np.array([1,0], dtype=complex)
qubit2_state = np.array([1,0], dtype=complex)

# creating the bell state
qubit1_state = hadamard_gate.dot(qubit1_state)
two_qubit_state = np.kron(qubit1_state, qubit2_state) # np.kron() is the tensor product
bell_state = cnot_gate.dot(two_qubit_state)

print(bell_state)
print(measure(bell_state))