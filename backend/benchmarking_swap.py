# File for benchmarking various functions
# ----------------------------------------------------------------------------------------
import numpy as np
from random import *
import time
import matplotlib.pyplot as plt
import Gates
import math
from memory_profiler import profile
# ----------------------------------------------------------------------------------------
def gate():
    pass

def swap_gate(state_vector, index_qubit_a, index_qubit_b, qubit_count):
    gate = Gates.expand_gate(Gates.CNOT, index_qubit_a, qubit_count)
    if index_qubit_a==index_qubit_b:
        return state_vector
    else:
        return state_vector.dot
    

# ----------------------------------------------------------------------------------------
# Swaps bits located at i and j
# swaps bits (most significant bit has index 0, least significant has index n)
def swap_bits(num: int, i: int, j: int, n: int):
    # Extract the bits at positions i and j
    bit_i = (num >> (n - 1 - i)) & 1
    bit_j = (num >> (n - 1 - j)) & 1
    # XOR the bits to swap them
    xor_result = bit_i ^ bit_j
    # Use XOR to flip the bits at positions i and j
    num ^= (xor_result << (n - 1 - i)) | (xor_result << (n - 1 - j))
    return num

def swap1(state_vector, index_qubit_a, index_qubit_b, qubit_count):
    new_state_vector = state_vector
    # Iterate through states vector and swap states
    for state_index in range(1, len(state_vector) - 1):
        # Calculate which element our current element should be replaced by
        new_state_index = swap_bits(state_index, index_qubit_a, index_qubit_b, qubit_count)
        # Perform swap
        new_state_vector[new_state_index] = state_vector[state_index]
    return state_vector

def swap2(state_vector, index_qubit_a, index_qubit_b, qubit_count):
    # Iterate through states vector and swap states
    for state_index in range(1, len(state_vector) - 1):
        # Calculate which element our current element should be replaced by
        new_state_index = swap_bits(state_index, index_qubit_a, index_qubit_b, qubit_count)
        # Check if index already has been swapped
        if new_state_index > state_index:
            # Perform swap
            state_vector[state_index], state_vector[new_state_index] = state_vector[new_state_index], state_vector[state_index]
    return state_vector

# Swaps two qubits in a register
def swap3(state_vector, index_qubit_a, index_qubit_b, qubit_count):
    # Iterate through states vector and swap states
    state_vector_length = len(state_vector)
    for state_index in range(1, state_vector_length//2):
        # Calculate which element our current element should be replaced by
        new_state_index = swap_bits(state_index, index_qubit_a, index_qubit_b, qubit_count)
        # Check if index already has been swapped
        if new_state_index > state_index:
            # Perform swap
            state_vector[state_index], state_vector[new_state_index] = state_vector[new_state_index], state_vector[state_index]
            # Find symmetrical swap pair
            state_vector[state_vector_length - state_index], state_vector[state_vector_length - new_state_index] = state_vector[state_vector_length - new_state_index], state_vector[state_vector_length - state_index]
    return state_vector

def swap4(state_vector, index_qubit_a, index_qubit_b, qubit_count):
    state_vector_length = len(state_vector)
    # Create an array representing the binary representation of each state index
    binary_indices = np.arange(state_vector_length)[:, np.newaxis] >> np.arange(qubit_count - 1, -1, -1) & 1
    # XOR the bits at index_qubit_a and index_qubit_b to determine which indices to swap
    xor_result = binary_indices[:, index_qubit_a] ^ binary_indices[:, index_qubit_b]
    # Find the indices where bits at index_qubit_a and index_qubit_b differ
    swap_indices = np.nonzero(xor_result)[0]
    # Perform the swaps
    state_vector[swap_indices], state_vector[state_vector_length - swap_indices - 1] = (
        state_vector[state_vector_length - swap_indices - 1], state_vector[swap_indices]
    )
    return state_vector

# ----------------------------------------------------------------------------------------
# Verifying

def verify_algorithms(n_qubits):
    state_vector = np.random.rand(2**n_qubits) + np.random.rand(2**n_qubits) * 1j
    results = []
    for qubit_index in range(2,n_qubits):
        # Generate random indices for qubit_a and qubit_b
        qubit_a = np.random.randint(0, n_qubits)
        qubit_b = np.random.randint(0, n_qubits)
        # Ensure qubit_a and qubit_b are not equal
        while qubit_b == qubit_a:
            qubit_b = np.random.randint(0, n_qubits)
        state1  = swap2(state_vector, qubit_a, qubit_b, n_qubits)
        state2  = swap3(state_vector, qubit_a, qubit_b, n_qubits)
        state3  = swap4(state_vector, qubit_a, qubit_b, n_qubits)
        # Check if the probabilities are equal within a small tolerance
        tolerance = 1e-10
        if np.array_equal(state1, state2) and np.array_equal(state2, state3):
            results.append(True)
        else:
            results.append(False)
            print(f"Algorithms produce different results for qubit index {qubit_index}:")
            print("swap1:", state1)
            print("swap2:", state2)
            print("swap3:", state3)
    if all(results):
        print("All algorithms return the same result for all qubit indices.")
    else:
        print("Some algorithms produce different results for certain qubit indices.")
# verify_algorithms(16)

# ----------------------------------------------------------------------------------------
# Benchmarking
def benchmark_swap(n_qubits_range, n_trials):
    print("benchmark started")
    times1 = []
    times2 = []
    times3 = []
    for n_qubits in n_qubits_range:
        state_vector = np.random.uniform(-1, 1, size=2**n_qubits) + np.random.uniform(-1, 1, size=2**n_qubits) * 1j   
        # Generate random indices for qubit_a and qubit_b
        qubit_a = np.random.randint(0, n_qubits)
        qubit_b = np.random.randint(0, n_qubits)
        # Ensure qubit_a and qubit_b are not equal
        while qubit_b == qubit_a:
            qubit_b = np.random.randint(0, n_qubits)

        start_time = time.time()
        for _ in range(n_trials):
            swap2(state_vector, qubit_a, qubit_b, n_qubits)
            # swap(state_vector, qubit_index, n_qubits)
        end_time = time.time()
        total_time = end_time - start_time
        average_time_per_trial1 = (total_time / n_trials) * 1000  # Convert to ms
        times1.append(average_time_per_trial1)
        
        start_time = time.time()
        for _ in range(n_trials):
            swap3(state_vector, qubit_a, qubit_b, n_qubits)
        end_time = time.time()
        total_time = end_time - start_time
        average_time_per_trial2 = (total_time / n_trials) * 1000  # Convert to ms
        times2.append(average_time_per_trial2)
        
        start_time = time.time()
        for _ in range(n_trials):
            swap4(state_vector, qubit_a, qubit_b, n_qubits)
        end_time = time.time()
        total_time = end_time - start_time
        average_time_per_trial1 = (total_time / n_trials) * 1000  # Convert to ms
        times3.append(average_time_per_trial1)

        print(f"Time taken for {n_qubits} qubits: swap1 - {average_time_per_trial1:.6f} ms, swap2 - {average_time_per_trial2:.6f} ms")

    plt.plot(n_qubits_range, times1, marker='o', label='swap1')
    plt.plot(n_qubits_range, times2, marker='o', label='swap2')
    plt.plot(n_qubits_range, times3, marker='o', label='swap3')
    plt.xlabel('Number of Qubits')
    plt.ylabel('Time (milliseconds)')
    plt.title('Time taken for swapping two qubits in a state vector for three different algorithms.')
    plt.legend()
    plt.show()

benchmark_swap(range(16,17), 1)