import numpy as np

def make_unitary(matrix):
    # Compute the product of the matrix and its conjugate transpose
    product = np.dot(matrix, np.conj(matrix.T))
    
    # Check if the product is close to the identity matrix
    if np.allclose(product, np.eye(matrix.shape[0])):
        return matrix
    else:
        # If the matrix is not unitary, try to make it unitary
        # Normalize each column vector
        normalized_matrix = matrix / np.sqrt(np.sum(np.abs(matrix)**2, axis=0))
        return normalized_matrix

# Given gate matrix
gate_matrix = np.array([[1., 0., 0., 0., 0., 0., 0., 0.],
                        [0., 0., 0., 0., 1., 0., 0., 0.],
                        [0., 0., 0., 1., 0., 0., 0., 0.],
                        [0., 0., 1., 0., 0., 0., 0., 0.],
                        [0., 1., 0., 0., 0., 0., 0., 0.],
                        [0., 0., 0., 0., 0., 1., 0., 0.],
                        [0., 0., 0., 0., 0., 0., 1., 0.],
                        [0., 0., 0., 0., 0., 0., 0., 1.]])

# Make the gate matrix unitary
unitary_gate_matrix = make_unitary(gate_matrix)
print("Unitary gate matrix:\n", unitary_gate_matrix)

def is_unitary(matrix):
    # Check if the matrix is square
    if matrix.shape[0] != matrix.shape[1]:
        return False
    
    # Compute the product of the matrix and its conjugate transpose
    product = np.dot(matrix, np.conj(matrix.T))
    
    # Check if the product is close to the identity matrix
    return np.allclose(product, np.eye(matrix.shape[0]))

print(is_unitary(unitary_gate_matrix))