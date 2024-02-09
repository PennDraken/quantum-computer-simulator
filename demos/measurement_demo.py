import numpy as np
import random

# This is a general implementation of a measurement algorithm that should work for any 2x2 matrix
# Input: matrix containing values of qubits, qubit index is the index of the qubit we want to measure (0-indexed)
# Returns the collapsed normalised matrix
# https://quantumcomputing.stackexchange.com/questions/1206/how-does-measurement-of-one-qubit-affect-the-others/4133#4133
def measure2x2(state_matrix, qubit_index):
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

# Generic implementation of measurement algorithm
def measure(state_matrix, qubit_index):
    qubit_count = int(np.log2(len(state_matrix)))
    # Matrices used to remove states from matrix
    m0 = collapsed_vector([1,0], qubit_index, qubit_count)
    m1 = collapsed_vector([0,1], qubit_index, qubit_count)
    # Probabilites for given qubit to be 0 or 1
    p0 = np.sum(np.abs(m0*state_matrix)**2)
    p1 = np.sum(np.abs(m1*state_matrix)**2)
    # Collapsing qubit based on probabilites p0 or p1
    p = np.random.choice([0,1], p=[p0,p1])
    # Set probability to 0 for all states where qubit is equal to 0
    measured_state = None
    if p==0:
        measured_state=m0*state_matrix
    else:
        measured_state=m1*state_matrix
    # Normalise the measurement to fulfill property |a|^2+|b|^2+...==1
    scaler = np.sqrt(np.sum(np.abs(state_matrix)**2)) # Sum of the abs squares of matrix
    measured_state = measured_state/scaler # Divide by scaler so |sum of ^2| == 1
    return measured_state

# We can create a collapsed vector corresponding to the qubit that we collapsed
# Used to apply measurement to a qubit state matrix
def collapsed_vector(single_qubit_state, qubit_index, qubit_count):
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

print(measure(np.array([1/2,1/2,1/2,1/2]), 1))