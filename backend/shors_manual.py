import numpy as np
import random

# Vector containing all states corresponding to a qubit
def collapsed_vector(single_qubit_state, qubit_index, qubit_count)->np.array:
    m = np.array([1, 1])
    vector = single_qubit_state if qubit_index == 0 else m
    for i in range(1, qubit_count):
        vector = np.kron(vector, single_qubit_state if i == qubit_index else m)
    return vector

def get_qubit(state_vector, index):
    assert 2**index<len(state_vector), f"Qubit index out of bounds {index}"
    m1 = collapsed_vector([0,1], index, int(np.log2(len(state_vector)))) # len 8 -> 3 qubits
    p = np.sum(np.abs(m1*state_vector)**2)
    return np.round(p, 8)

def get_number_list(state_vector, qubit_index_start, qubit_index_end):
    number_list = []
    for i in range(qubit_index_start, qubit_index_end):
        number_list.append(get_qubit(state_vector, i))
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
    assert index+width-1 < qubit_count, "Error! Gate does not fit"
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
    p = get_qubit(state_vector, qubit_index)
    if random.random() <= p:
        state_vector = state_vector * collapsed_vector([0,1], qubit_index, int(np.log2(len(state_vector))))
    else:
        state_vector = state_vector * collapsed_vector([1,0], qubit_index, int(np.log2(len(state_vector))))
    # Normalize
    state_vector = normalize(state_vector)
    return state_vector



# Generates a Quantum Fourier Transform matrix
def QFT(N : int)->np.array:
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

def QFT_inv(N : int):
    return np.linalg.inv(QFT(N))

def function_exponentiation(a,i,N,x):
    return (x*(a**2)**i)%N

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


def Ua(a, i, N):
    number_of_qubits = int(np.ceil(np.log2(N)))
    number_of_states = 2**number_of_qubits
    matrix = np.zeros((number_of_states,number_of_states))
    highest_state = N
    # Map matrix
    for input_state in range(highest_state):
        output_state = function_exponentiation(a,i,N,input_state)
        matrix[output_state, input_state] = 1
    # Add remaining states (ensures unitary)
    for i in range(highest_state, number_of_states):
        matrix[i,i]=1
    assert is_unitary(matrix), f"Gate is not unitary\n {matrix}"
    return matrix


# assert (np.allclose(gate_Ua305, Ua(3,0,5))), f"Not close \n{Ua(3, 0, 5)}"
# assert (np.allclose(Ua(3,0,5).dot(vector), np.array([1,0,0,0,0,0,0,0]))), f"Not close \n{Ua(3,0,5).dot(vector)}"

# Makes a gate controlled
def controlled(matrix, index=0):
    m, n = matrix.shape
    new_matrix = np.hstack((np.eye(m, n), np.zeros((m, n), dtype=complex)))
    new_matrix = np.vstack((new_matrix, np.hstack((np.zeros((m, n)), matrix), dtype=complex)))
    if index!=0:
        return controlled(new_matrix, index-1)
    return new_matrix

# ----------------------------------------------------------------------------------------------------------------------------------------
# Worked example for a=3 N=5
def shors_3_5():
    a=3
    n=3
    N=5

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
    # 3 final qubits set to 1
    qubits_state = np.kron(qubits_state, np.array([0,1]))
    qubits_state = np.kron(qubits_state, np.array([1,0]))
    qubits_state = np.kron(qubits_state, np.array([1,0]))
    print(qubits_state)
    print(len(qubits_state))

    print(f"Iteration init")
    print(f"Probability number list is: {get_number_list(qubits_state, 0, 6)}")
    print(f"Probability number for lower list is: {get_number_list(qubits_state, 6, 9)}")
    print("-------------------------------------------------------------------------------------")

    for i in range(0,6):
        gate = expand_gate(controlled(Ua(3,i,5), index=i), (5-i), n*3)
        qubits_state = gate.dot(qubits_state)
        print(f"Iteration {i}")
        print(f"Probability upper qubits are: {get_number_list(qubits_state, 0, 6)}")
        print(f"Probability lower qubits are: {get_number_list(qubits_state, 6, 9)}")
        print("-------------------------------------------------------------------------------------")

    # Apply QFT^-1
    gate = expand_gate(QFT_inv(6), 0, 9)
    qubits_state = gate.dot(qubits_state)
    print(f"QFT^-1 applied")
    print(f"Probability upper qubits are: {get_number_list(qubits_state, 0, 6)}")
    print(f"Probability lower qubits are: {get_number_list(qubits_state, 6, 9)}")
    print("-------------------------------------------------------------------------------------")

    # Measurement
    for i in range(0,6):
        qubits_state = measure(qubits_state, i)
        print(f"Measurement of qubit {i}")
        print(f"Probability upper qubits are: {get_number_list(qubits_state, 0, 6)}")
        print(f"Probability lower qubits are: {get_number_list(qubits_state, 6, 9)}")
        print("-------------------------------------------------------------------------------------")

    return qubits_state


shors_3_5()





def gate_experimentation7_15():
    # Apply our gates
    a=7
    N=15
    gate_0 = Ua(a,0,15)
    print(f"Gate i=0\n{gate_0}")

    gate_1 = Ua(a,1,15)
    print(f"Gate i=1\n{gate_1}")

    gate_2 = Ua(a,2,15)
    print(f"Gate i=2\n{gate_2}")

    gate_3 = Ua(a,3,15)
    print(f"Gate i=3\n{gate_3}")

    gate_4 = Ua(a,4,15)
    print(f"Gate i=4\n{gate_4}")

    gate_5 = Ua(a,5,15)
    print(f"Gate i=5\n{gate_5}")

    gate_6 = Ua(a,6,15)
    print(f"Gate i=5\n{gate_6}")

    gate_7 = Ua(a,7,15)
    print(f"Gate i=5\n{gate_7}")

    print("Statevectors---------------")
    # statevector_lower = np.array([0, 0, 0, 0, 0, 0, 0, 1]) # x0,x1,x2
    # statevector_lower = np.kron(np.kron(np.array([0,1]),np.array([1,0])), np.array([1,0]))
    statevector_lower = np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]) # 0b0111
    print(f"Statevector lower input: {statevector_lower}")

    statevector_index_0 = gate_0.dot(statevector_lower)
    print(statevector_index_0)

    statevector_index_1 = gate_1.dot(statevector_index_0)
    print(statevector_index_1)

    statevector_index_2 = gate_2.dot(statevector_index_1)
    print(statevector_index_2)

    statevector_index_3 = gate_3.dot(statevector_index_2)
    print(statevector_index_3)

    statevector_index_4 = gate_4.dot(statevector_index_3)
    print(statevector_index_4)

    statevector_index_5 = gate_5.dot(statevector_index_4)
    print(statevector_index_5)

    statevector_index_6 = gate_6.dot(statevector_index_5)
    print(statevector_index_6)

    statevector_index_7 = gate_7.dot(statevector_index_6)
    print(statevector_index_7)

# gate_experimentation7_15()
# exit()


def gate_experimentation():
    # Apply our gates
    gate_0 = Ua(3,0,5)
    print(f"Gate i=0\n{gate_0}")
    # Control qubit index = 5
    # q0 q1 q2 q3 q4 q5 x0 x1 x2

    gate_1 = Ua(3,1,5)
    print(f"Gate i=1\n{gate_1}")

    gate_2 = Ua(3,2,5)
    print(f"Gate i=2\n{gate_2}")

    gate_3 = Ua(3,3,5)
    print(f"Gate i=3\n{gate_3}")

    gate_4 = Ua(3,4,5)
    print(f"Gate i=4\n{gate_4}")

    gate_5 = Ua(3,5,5)
    print(f"Gate i=5\n{gate_5}")

    print("Statevectors---------------")
    # statevector_lower = np.array([0, 0, 0, 0, 0, 0, 0, 1]) # x0,x1,x2   1 1 0 x2 
    # statevector_lower = np.kron(np.kron(np.array([0,1]),np.array([1,0])), np.array([1,0]))
    #                             0  1  2  3  4  5  6  7
    statevector_lower = np.array([0, 0, 0, 0, 0, 0, 0, 0])
    print(f"Statevector lower input: {statevector_lower}")

    statevector_index_0 = gate_0.dot(statevector_lower)
    print(statevector_index_0)

    statevector_index_1 = gate_1.dot(statevector_index_0)
    print(statevector_index_1)

    statevector_index_2 = gate_2.dot(statevector_index_1)
    print(statevector_index_2)

    statevector_index_3 = gate_3.dot(statevector_index_2)
    print(statevector_index_3)

    statevector_index_4 = gate_4.dot(statevector_index_3)
    print(statevector_index_4)

    statevector_index_5 = gate_5.dot(statevector_index_4)
    print(statevector_index_5)
        
# gate_experimentation()

# 3^2^0 mod 5 = 1
# AC = 0b110 6 -> (6 * 3^2^0) mod 5 = 1
# if ABC = 111 7 -> 1 * 7 mod 5 = 010

#      q.apply_gate_qubit_list(Gates.U(3^2^1 mod 5))
#      this: Gates.U(3^2^1 mod 5) * [0,0,0,0,0,0,0,1] = 7 ----> [0,0,1,0,0,0,0,0] = ABC 010
 
        
# 3^2^1 mod 5 = 4

# if ABC = 111 7 -> 4 * 2 mod 5 = 011

#      q.apply_gate_qubit_list(Gates.U(3^2^1 mod 5))
#      this: Gates.U(3^2^1 mod 5) * [0,0,1,0,0,0,0,1] = 2 ----> [0,0,0,1,0,0,0,0] = ABC 011


# 3^2^2 mod 5 = 1

# if ABC = 011 3 -> 1 * 3 mod 5 = 011

#      q.apply_gate_qubit_list(Gates.U(3^2^1 mod 5))
#      this: Gates.U(3^2^1 mod 5) * [0,0,0,1,0,0,0,0] = 3 ----> [0,0,0,1,0,0,0,0] = ABC 011


# 3^2^3 mod 5 = 4

# if ABC = 011 3 -> 4 * 3 mod 5 = 010

#      q.apply_gate_qubit_list(Gates.U(3^2^1 mod 5))
#      this: Gates.U(3^2^1 mod 5) * [0,0,0,1,0,0,0,0] = 3 ----> [0,0,0,1,0,0,0,0] = ABC 010


# 3^2^4 mod 5 = 1

# if ABC = 011 3 -> 1 * 2 mod 5 = 010

#      q.apply_gate_qubit_list(Gates.U(3^2^1 mod 5))
#      this: Gates.U(3^2^1 mod 5) * [0,0,1,0,0,0,0,0] = 2 ----> [0,0,1,0,0,0,0,0] = ABC 010


# 3^2^5 mod 5 = 4

# if ABC = 011 3 -> 4 * 2 mod 5 = 011

#      q.apply_gate_qubit_list(Gates.U(3^2^1 mod 5))
#      this: Gates.U(3^2^1 mod 5) * [0,0,1,0,0,0,0,0] = 2 ----> [0,0,0,1,0,0,0,0] = ABC 011

