import numpy as np
import random

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