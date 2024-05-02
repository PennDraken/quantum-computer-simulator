import numpy as np
import random
import fractions
import math

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
def shors_5(a):
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
        gate = expand_gate(controlled(Ua(a,i,5), index=i), (5-i), n*3)
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

    # Find period
    val = get_qubit(qubits_state, 0)*2**0 + get_qubit(qubits_state, 1)*2**1 + get_qubit(qubits_state, 2)*2**2 + get_qubit(qubits_state, 3)*2**3 + get_qubit(qubits_state, 4)*2**4 + get_qubit(qubits_state, 5)*2**5
    phase = val / 2**(n-1) # b / c
    # frac = fractions.Fraction(phase).limit_denominator(N-1) # frac = j / r
    r = fractions.Fraction(phase).limit_denominator(N-1).denominator
    if r==3:
        pass
    print(r)
    return r

def shors_7_15():
    a=7
    n=4
    N=15

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
    qubits_state = np.kron(qubits_state, np.array([0,1]))
    qubits_state = np.kron(qubits_state, np.array([1,0]))
    qubits_state = np.kron(qubits_state, np.array([1,0]))
    qubits_state = np.kron(qubits_state, np.array([1,0]))

    print(qubits_state)
    print(len(qubits_state))

    print(f"Iteration init")
    print(f"Probability number list is: {get_number_list(qubits_state, 0, 6)}")
    print(f"Probability number for lower list is: {get_number_list(qubits_state, 6, 9)}")
    print("-------------------------------------------------------------------------------------")

    for i in range(0,8):
        gate = expand_gate(controlled(Ua(a,i,N), index=7-i), index=i, qubit_count=3*n) # TODO double check this
        qubits_state = gate.dot(qubits_state)
        print(f"Iteration {i}")
        print(f"Probability upper qubits are: {get_number_list(qubits_state, 0, 2*n)}")
        print(f"Probability lower qubits are: {get_number_list(qubits_state, 2*n, 3*n)}")
        print("-------------------------------------------------------------------------------------")

    # Apply QFT^-1
    gate = expand_gate(QFT_inv(2*n), 0, 3*n)
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
    val = get_qubit(qubits_state, 0)*2**0 + get_qubit(qubits_state, 1)*2**1 + get_qubit(qubits_state, 2)*2**2 + get_qubit(qubits_state, 3)*2**3 + get_qubit(qubits_state, 4)*2**4 + get_qubit(qubits_state, 5)*2**5 + get_qubit(qubits_state, 6)*2**6 + get_qubit(qubits_state, 7)*2**7
    # phase = val / 2**(n-1) # b / c
    phase = val / 2**(2*n) # b / c
    # frac = fractions.Fraction(phase).limit_denominator(N-1) # frac = j / r
    r = fractions.Fraction(phase).limit_denominator(N).denominator
    if r==3:
        pass
    print(r)
    return r


# exit()
def shors():
    N = 5
    if N % 2 == 0:
        return 2

    while True:
        a = random.randrange(2, N)
        k = math.gcd(a, N)
        if k!=1:
            return k
        
        r = shors_5(a)
        if r%2 == 0:
            k = int((a**(r/2))%N)
            if k != (N - 1):
                factor1 = math.gcd(k-1, N)
                if factor1 != 1 and factor1 != N:
                    return factor1

def most_frequent(List):
    counter = 0
    num = List[0]
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
    return num

def least_frequent(List):
    min_counter = len(List) + 1  # Initialize minimum counter with a value greater than the list length
    least_freq_num = None  # Initialize the least frequent number
    for num in List:
        curr_frequency = List.count(num)
        if curr_frequency < min_counter:
            min_counter = curr_frequency
            least_freq_num = num
    return least_freq_num

# shors()
def shor_counter():
    r_list = []
    for i in range(0,200):
        r_list.append(shors_5(3))
    print(f"List: {r_list}\n")
    r_guess = most_frequent(r_list)
    print(f"Most frequent: {r_guess}")
    print(f"Amount: {r_list.count(r_guess)}")
    print(f"4 Amount: {r_list.count(4)}")
    print(f"LCM: {np.lcm.reduce(r_list)}")

def shor_7_15():
    r_list = []
    for i in range(0,20):
        r_list.append(shors_7_15())
    print(f"List: {r_list}\n")
    r_guess = most_frequent(r_list)
    print(f"Most frequent: {r_guess}")
    print(f"Amount: {r_list.count(r_guess)}")
    print(f"4 Amount: {r_list.count(4)}")
    print(f"LCM: {np.lcm.reduce(r_list)}")

shor_7_15()

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

