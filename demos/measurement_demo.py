import numpy as np
import random

# This is a general implementation of a measurement algorithm that should work for any 2x2 matrix
# Input: matrix containing values of qubits, qubit index is the index of the qubit we want to measure (0-indexed)
# Returns the collapsed normalised matrix
# https://quantumcomputing.stackexchange.com/questions/1206/how-does-measurement-of-one-qubit-affect-the-others/4133#4133
def measure(state_matrix, qubit_index):
    if qubit_index==0:
        p0 = np.abs(state_matrix[0])**2+np.abs(state_matrix[1])**2
        p1 = np.abs(state_matrix[2])**2+np.abs(state_matrix[3])**2
        p = np.random.choice([0,1], p=[p0,p1])
        if p==0:
            state_matrix[2] = 0
            state_matrix[3] = 0
        elif p==1:
            state_matrix[0] = 0
            state_matrix[1] = 0
    elif qubit_index==1:
        p0 = np.abs(state_matrix[0])**2+np.abs(state_matrix[2])**2
        p1 = np.abs(state_matrix[1])**2+np.abs(state_matrix[3])**2
        p = np.random.choice([0,1], p=[p0,p1])
        if p==0:
            state_matrix[0] = 0
            state_matrix[2] = 0
        elif p==1:
            state_matrix[1] = 0
            state_matrix[3] = 0
    # normalise the matrix
    scaler = np.sqrt(np.abs(state_matrix[0])**2 + np.abs(state_matrix[1])**2 + np.abs(state_matrix[2])**2 + np.abs(state_matrix[3])**2)
    state_matrix = state_matrix/scaler
    return state_matrix

print(measure(np.array([1/2,1/2,1/2,1/2]), 0))
print(measure(np.array([1/2,1/2,1/2,1/2]), 1))