import numpy as np
import random

# functions
# Reads a qubit. Returns new qubit state that is collapsed.
def read_qubit(qubit_state) -> np.array:
    probability_alpha = (np.absolute(qubit_state[0]))**2
    random_value = random.uniform(0,1)
    if random_value <= probability_alpha:
        return np.array([1,0])
    else:
        return np.array([0,1])

# create gates
hadamard_gate = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)
# create qubit
qubit_state = np.array([1,0], dtype=complex)
# apply Hadamard gate though dot product
qubit_state = hadamard_gate.dot(qubit_state)
print(read_qubit(qubit_state))