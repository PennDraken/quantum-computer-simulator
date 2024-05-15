import numpy as np
import random
import fractions
import math
from qiskit import *
import qiskit.quantum_info as qi
import numpy as np
from qiskit.circuit.library import QFT
import Gates

def matrix_string(matrix: np.array):
    matrix_string = ""
    spacing = 14  # Distance between each number (number centered every 8 characters)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            num = matrix[i][j]
            real = round(num.real, 2)
            imag = round(num.imag, 2)
            if real == 0 and imag == 0:
                formatted_num = "0"
                padding = spacing - 1  # Account for single character
            else:
                formatted_num = f"{real} + {imag}j"  # Format real and imaginary parts
                padding = spacing - len(formatted_num)
            if padding % 2 == 0:
                left_padding = right_padding = padding // 2
            else:
                left_padding  = padding // 2 + 1
                right_padding = padding // 2
            matrix_string += " " * left_padding + formatted_num + " " * right_padding
        matrix_string += "\n"  # Add newline after each row
    print(matrix_string)


def swap_bits(num: int, i: int, j: int, n: int):
    # Extract the bits at positions i and j
    bit_i = (num >> (n - 1 - i)) & 1
    bit_j = (num >> (n - 1 - j)) & 1
    # XOR the bits to swap them
    xor_result = bit_i ^ bit_j
    # Use XOR to flip the bits at positions i and j
    num ^= (xor_result << (n - 1 - i)) | (xor_result << (n - 1 - j))
    return num

def swap(state_vector, index_qubit_a, index_qubit_b, qubit_count):
    # Iterate through states vector and swap states
    for state_index in range(1, len(state_vector) - 1):
        # Calculate which element our current element should be replaced by
        new_state_index = swap_bits(state_index, index_qubit_a, index_qubit_b, qubit_count)
        # Check if index already has been swapped
        if new_state_index > state_index:
            # Perform swap
            state_vector[state_index], state_vector[new_state_index] = state_vector[new_state_index], state_vector[state_index]
    return state_vector

# Vector containing all states corresponding to a qubit
def collapsed_vector(single_qubit_state, qubit_index, qubit_count)->np.array:
    m = np.array([1, 1])
    vector = single_qubit_state if qubit_index == 0 else m
    for i in range(1, qubit_count):
        vector = np.kron(vector, single_qubit_state if i == qubit_index else m)
    return vector

def get_probability2(state_vector, index):
    assert 2**index<len(state_vector), f"Qubit index out of bounds {index}"
    m1 = collapsed_vector([0,1], index, int(np.log2(len(state_vector)))) # len 8 -> 3 qubits
    p = np.sum(np.abs(m1*state_vector)**2)
    return np.round(p, 8)

def get_probability(state_vector, qubit_index, qubits):
    mask = 1 << (qubits - qubit_index - 1)
    masked_states = state_vector[np.bitwise_and(np.arange(len(state_vector)), mask) != 0]
    return np.sum(np.abs(masked_states) ** 2)

def get_number_list(state_vector, qubit_index_start, qubit_index_end):
    number_list = []
    for i in range(qubit_index_start, qubit_index_end):
        number_list.append(get_probability(state_vector, i, int(np.log2(len(state_vector)))))
    return number_list

def is_unitary(matrix):
    # Check if the matrix is square
    if matrix.shape[0] != matrix.shape[1]:
        return False
    # Compute the product of the matrix and its conjugate transpose
    product = np.dot(matrix, np.conj(matrix.T))
    # Check if the product is close to the identity matrix
    return np.allclose(product, np.eye(matrix.shape[0]))

I = np.array([[1,0],[0,1]]) 

# Expands a gate to match size and position when applying
def expand_gate(gate, index, qubit_count):
    # Check that gate fits at given index
    width = int(np.log2(len(gate)))
    assert index+width-1 < qubit_count, "Error! Gate does not fit."
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

# Normalise a state_vector
def normalize(state_vector : np.array):
        scaler = np.sqrt(np.sum(np.abs(state_vector)**2))
        new_vector = state_vector / scaler
        return new_vector

# Measuers a qubit
def measure(state_vector, qubit_index):
    p = get_probability(state_vector, qubit_index, int(np.log2(len(state_vector))))
    if random.random() <= p:
        state_vector = state_vector * collapsed_vector([0,1], qubit_index, int(np.log2(len(state_vector))))
    else:
        state_vector = state_vector * collapsed_vector([1,0], qubit_index, int(np.log2(len(state_vector))))
    # Normalize
    state_vector = normalize(state_vector)
    return state_vector


# Generates a Quantum Fourier Transform matrix
def QFT2(N : int)->np.array:
    N = 2**N
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

def QFT_inv2(N : int):
    return np.linalg.inv(QFT(N))

def circuit_to_gate(circuit):
    op1=qi.Operator(circuit.reverse_bits())
    op2=qi.Operator(circuit)
    matrix1 = op1.data
    matrix2 = op2.data
    matrix2 = Gates.reverse_qubit_order(matrix2)
    assert np.allclose(matrix1, matrix2), f"not equal\n {matrix1[0:4,0:4]}\n\n {matrix2[0:4,0:4]}"
    return op1.data

def QFT_dagger_qiskit(n):
    qc = QuantumCircuit(n)
    qc.append(QFT(n), range(n))
    qft_gate_matrix = circuit_to_gate(qc)
    dagger_qft = np.conj(qft_gate_matrix).T
    return dagger_qft

def QFT_qiskit(n):
    qc = QuantumCircuit(n)
    qc.append(QFT(n), range(n))
    qft_gate_matrix = circuit_to_gate(qc)
    return qft_gate_matrix

def QFT_our(n):
    N = 2**n
    W = np.power(np.e, (2 * np.pi*1j)/N)
    constant = 1/np.sqrt(N)
    matrix = np.ones((N,N), dtype= complex)
    for n in range(N):
        for m in range(n, N):
            value = np.power(W, n * m)
            matrix[n][m] = value
            matrix[m][n] = value
    matrix *= constant
    return matrix

# our implementation
def QFT_dagger_our(n: int)->np.array:
    N = 2**n
    W = np.power(np.e, (-2 * np.pi*1j)/N)
    constant = 1/np.sqrt(N)
    matrix = np.ones((N,N), dtype= complex)
    for n in range(N):
        for m in range(n, N):
            value = np.round(np.power(W, n * m), 5)
            matrix[n][m] = value
            matrix[m][n] = value
    matrix *= constant
    return np.linalg.inv(matrix)

"""n=2
qisk = QFT_qiskit(n)
our  = QFT_our(n)
matrix_string(qisk)
matrix_string(our)

if np.array_equal(qisk, our):
    print("Success!")
else:
    print("fail")
exit()"""

def Ua2(a, i, N):
    number_of_qubits = int(np.ceil(np.log2(N)))
    number_of_states = 2**number_of_qubits
    matrix = np.zeros((number_of_states, number_of_states))
    highest_state = N
    # Map matrix
    for input_state in range(number_of_states):
        output_state = function_exponentiation(a, i, N, input_state)
        matrix[output_state, input_state] = 1
    # assert is_unitary(matrix), f"Gate is not unitary\n {matrix}"
    return matrix

def function_exponentiation(a,power,N,x):
    return (x*a**power)%N


def Ua(a, power, N):
    number_of_qubits = int(np.ceil(np.log2(N)))
    number_of_states = 2**number_of_qubits
    matrix = np.zeros((number_of_states,number_of_states))
    highest_state = N
    # Map matrix
    for input_state in range(highest_state):
        output_state = function_exponentiation(a,power,N,input_state)
        matrix[output_state, input_state] = 1
    # Add remaining states (ensures unitary)
    for i in range(highest_state, number_of_states):
        matrix[i,i]=1
    assert is_unitary(matrix), f"Gate is not unitary\n {matrix}"
    return matrix


# assert (np.allclose(gate_Ua305, Ua(3,0,5))), f"Not close \n{Ua(3, 0, 5)}"
# assert (np.allclose(Ua(3,0,5).dot(vector), np.array([1,0,0,0,0,0,0,0]))), f"Not close \n{Ua(3,0,5).dot(vector)}"

# Makes a gate controlled
def controlled2(matrix, index=1):
    m, n = matrix.shape
    if index==0:
        return matrix
    new_matrix = np.hstack((np.eye(m, n), np.zeros((m, n), dtype=complex)))
    new_matrix = np.vstack((new_matrix, np.hstack((np.zeros((m, n)), matrix), dtype=complex)))
    return controlled(new_matrix, index-1)

def controlled(matrix, index=1):
    new_matrix_size = 2**(int(np.log2(len(matrix)))+index)
    new_matrix = np.diag(np.ones(new_matrix_size))
    # len(matrix) is the position where our matrix should be inserted
    start_index = new_matrix_size - len(matrix)
    end_index   = new_matrix_size
    new_matrix[start_index:end_index, start_index:end_index] = matrix
    return new_matrix


# ----------------------------------------------------------------------------------------------------------------------------------------
def shors_7_15():
    a=7
    n=4
    N=15

    # upper_register = np.kron(1/np.sqrt(2)*np.array([1,1]), 1/np.sqrt(2)*np.array([1,1]))
    # lower_register = np.array([0,1,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0])
    # state = np.kron(upper_register, lower_register)
    # print(get_number_list(state, 2, 6))
    # gate = controlled(Ua(7,1,15),1)
    # gate = np.kron(gate, np.array([[1,0],[0,1]]))
    # print("Gate---------------------------")
    # matrix_string(gate[16:,16:])
    # print("State--------------------------")
    # state = swap(state, 0,1,6)
    # state = gate.dot(state)
    # state = swap(state, 0,1,6)
    # print(state)
    # print(get_number_list(state, 2, 6))
    # exit()

    # Create state vector for all 3*n qubits
    hadamard_qubit = 1/np.sqrt(2)*np.array([1,1])
    # 2 qubits
    qubits_state = np.kron(hadamard_qubit, hadamard_qubit)
    # 3 qubits
    qubits_state = np.kron(qubits_state, hadamard_qubit)
    # 4 qubits
    qubits_state = np.kron(qubits_state, hadamard_qubit)
    # 5 qubits
    qubits_state = np.kron(qubits_state, hadamard_qubit)
    # 6 qubits
    qubits_state = np.kron(qubits_state, hadamard_qubit)
    # 7 qubits
    qubits_state = np.kron(qubits_state, hadamard_qubit)
    # 8 qubits
    qubits_state = np.kron(qubits_state, hadamard_qubit)

    # 4 final qubits set to |1>
    qubits_state = np.kron(qubits_state, np.array([1,0]))
    qubits_state = np.kron(qubits_state, np.array([1,0]))
    qubits_state = np.kron(qubits_state, np.array([1,0]))
    qubits_state = np.kron(qubits_state, np.array([0,1])) # X gate
    print(len(qubits_state))

    
    # gate = np.array([[1,0],[0,1]]) # 2 qubit
    # gate = np.kron(gate, np.array([[1,0],[0,1]])) # 3 qubit
    # gate = np.kron(gate, np.array([[1,0],[0,1]])) # 4 qubit
    # gate = np.kron(gate, np.array([[1,0],[0,1]])) # 5 qubit
    # gate = np.kron(gate, np.array([[1,0],[0,1]])) # 6 qubit
    # gate = np.kron(gate, np.array([[1,0],[0,1]])) # 7 qubit
    # gate = np.kron(gate, np.array([[1,0],[0,1]])) # 7 qubit
    # gate = np.kron(gate, controlled(Ua(7,1,15),1))
    # print("Gate---------------------------")
    # # matrix_string(gate[16:,16:])
    # print("State--------------------------")
    # qubits_state = swap(qubits_state, 0,7,12)
    # qubits_state = gate.dot(qubits_state)
    # qubits_state = swap(qubits_state, 0,7,12)
    # print(qubits_state)
    # print(get_number_list(qubits_state, 8, 12))
    # exit()
# 

    print(f"Iteration init")
    print(f"Probability number list is: {get_number_list(qubits_state, 0, 2*n)}")
    print(f"Probability number for lower list is: {get_number_list(qubits_state, 8, 12)}")
    print("-------------------------------------------------------------------------------------")
    for i in range(0,8):
        power = 2**i
        control_qubit_index = i
        ua_gate = controlled(Ua(a, power, N), 1)
        gate = expand_gate(ua_gate, index=7, qubit_count=12) 
        # swap qubits to correct position
        qubits_state = swap(qubits_state, control_qubit_index, 7, 12)
        # apply gate
        qubits_state = gate.dot(qubits_state)
        # swap back
        qubits_state = swap(qubits_state, control_qubit_index, 7, 12)

        print(f"Iteration {i}")
        print(f"Probability upper qubits are: {get_number_list(qubits_state, 0, 2*n)}")
        print(f"Probability lower qubits are: {get_number_list(qubits_state, 8, 12)}")
        print("-------------------------------------------------------------------------------------")

    # Apply QFT^-1
    gate = expand_gate(QFT_dagger_qiskit(2*n), 0, 3*n)
    qubits_state = gate.dot(qubits_state)
    print(f"QFT^-1 applied")
    print(f"Probability upper qubits are: {get_number_list(qubits_state, 0, 2*n)}")
    print(f"Probability lower qubits are: {get_number_list(qubits_state, 2*n, 3*n)}")
    print("-------------------------------------------------------------------------------------")

    # Measurement
    for i in range(0,2*n):
        qubits_state = measure(qubits_state, i)
        print(f"Measurement of qubit {i}")
        print(f"Probability upper qubits are: {get_number_list(qubits_state, 0, 2*n)}")
        print(f"Probability lower qubits are: {get_number_list(qubits_state, 2*n, 3*n)}")
        print("-------------------------------------------------------------------------------------")

    # Find period
    val = get_probability(qubits_state, 0, 12)*2**0 + get_probability(qubits_state, 1, 12)*2**1 + get_probability(qubits_state, 2, 12)*2**2 + get_probability(qubits_state, 3, 12)*2**3 + get_probability(qubits_state, 4, 12)*2**4 + get_probability(qubits_state, 5, 12)*2**5 + get_probability(qubits_state, 6, 12)*2**6 + get_probability(qubits_state, 7, 12)*2**7
    # phase = val / 2**(n-1) # b / c
    # phase = val / 2**(2*n) # b / c
    return val
    # frac = fractions.Fraction(phase).limit_denominator(N-1) # frac = j / r
    """r = fractions.Fraction(phase).limit_denominator(N).denominator
    if r==3:
        pass
    print(r)
    return r"""


# exit()


def shor_7_15_iterate():
    phase_list = []
    for i in range(0,10):
        phase_list.append(shors_7_15())
    print(f"List: {phase_list}\n")
    r_guess = most_frequent(phase_list)
    print(f"Most frequent: {r_guess}")
    print(f"Amount: {phase_list.count(r_guess)}")
    print(f"4 Amount: {phase_list.count(4)}")
    print(f"LCM: {np.lcm.reduce(phase_list)}")

shor_7_15_iterate()
exit()

a = 7
N = 15
# Create state vector for all 3*n qubits
hadamard_qubit = 1/np.sqrt(2)*np.array([1,1])
# 2 qubits
qubits_state = np.kron(hadamard_qubit, hadamard_qubit)
# 3 qubits
qubits_state = np.kron(qubits_state, hadamard_qubit)
# 4 qubits
qubits_state = np.kron(qubits_state, hadamard_qubit)
# 5 qubits
qubits_state = np.kron(qubits_state, hadamard_qubit)
# 6 qubits
qubits_state = np.kron(qubits_state, hadamard_qubit)
# 7 qubits
qubits_state = np.kron(qubits_state, hadamard_qubit)
# 8 qubits
qubits_state = np.kron(qubits_state, hadamard_qubit)

# 4 final qubits set to |1>
qubits_state = np.kron(qubits_state, np.array([1,0]))
qubits_state = np.kron(qubits_state, np.array([1,0]))
qubits_state = np.kron(qubits_state, np.array([1,0]))
qubits_state = np.kron(qubits_state, np.array([0,1])) # X gate

def kron_list(states):
    combined_vector = states[0]
    for state in states[1:]:
        combined_vector = np.kron(combined_vector, state)
    return combined_vector

# create state |q0q8q9q10q11>
lower_reg = np.array([0,1,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0,])
state = kron_list([hadamard_qubit, lower_reg])
# apply first gate
gate = controlled(Ua(a, 1, N))
state = gate.dot(state)
# show probabilites
print("-----------------------------------")
print(get_probability(state, 0, 5))
print(get_probability(state, 1, 5))
print(get_probability(state, 2, 5))
print(get_probability(state, 3, 5))
print(get_probability(state, 4, 5))
# create state |q1q8q9q10q11q0>
state = kron_list([hadamard_qubit, state])
print("-----------------------------------")
print(get_probability(state, 0, 6))
print(get_probability(state, 1, 6))
print(get_probability(state, 2, 6))
print(get_probability(state, 3, 6))
print(get_probability(state, 4, 6))
print(get_probability(state, 5, 6))
# perform swaps
state = swap(state, 1, 2, 6)
print("First swap-------------------------")
print(get_probability(state, 0, 6))
print(get_probability(state, 1, 6))
print(get_probability(state, 2, 6))
print(get_probability(state, 3, 6))
print(get_probability(state, 4, 6))
print(get_probability(state, 5, 6))

state = swap(state, 2, 3, 6)
print("Second swap-------------------------")
print(get_probability(state, 0, 6))
print(get_probability(state, 1, 6))
print(get_probability(state, 2, 6))
print(get_probability(state, 3, 6))
print(get_probability(state, 4, 6))
print(get_probability(state, 5, 6))

state = swap(state, 3, 4, 6)
print("Third swap-------------------------")
print(get_probability(state, 0, 6))
print(get_probability(state, 1, 6))
print(get_probability(state, 2, 6))
print(get_probability(state, 3, 6))
print(get_probability(state, 4, 6))
print(get_probability(state, 5, 6))

state = swap(state, 4, 5, 6)
print("Fourth swap-----------------------------------")
print(get_probability(state, 0, 6))
print(get_probability(state, 1, 6))
print(get_probability(state, 2, 6))
print(get_probability(state, 3, 6))
print(get_probability(state, 4, 6))
print(get_probability(state, 5, 6))

# apply gate
ua_gate = controlled(Ua(a, 2, N))
gate = expand_gate(ua_gate, index=0, qubit_count=6)
state = gate.dot(state)
# show probabilities
print("Gate applied---------------------------")
print(get_probability(state, 0, 6))
print(get_probability(state, 1, 6))
print(get_probability(state, 2, 6))
print(get_probability(state, 3, 6))
print(get_probability(state, 4, 6))
print(get_probability(state, 5, 6))