# File for benchmarking various functions
# ----------------------------------------------------------------------------------------
import numpy as np
from random import *
import time
import matplotlib.pyplot as plt
import Gates
import math

def get_probability(state_vector, qubit_index, qubits):
    mask = 1 << (qubits - qubit_index - 1)
    probability = 0
    for i, state in enumerate(state_vector):
        if (i & mask) != 0:
            probability += abs(state)**2
    return probability

def get_probability2(state_vector, qubit_index, qubits):
    m1 = Gates.collapsed_vector([0,1], qubit_index, qubits)
    probability = np.sum(abs(m1 * state_vector)**2)
    return probability

def get_probability3(state_vector, qubit_index, qubits):
    mask = 1 << (qubits - qubit_index - 1)
    masked_states = state_vector[np.bitwise_and(np.arange(len(state_vector)), mask) != 0]
    return np.sum(np.abs(masked_states) ** 2)

def measure(state_vector, qubit_index):
    # Find probability of qubit collapsing to |1>
    probability = get_probability(state_vector, qubit_index)
    # Create two state_vectors for the outcomes of the measurement
    remaining_state_vector = np.zeros(len(state_vector)/2)
    if random(1) > probability:
        # Qubit collapsed to |1>
        measured_qubit_state_vector = [0,1]
        mask = i << qubit_index
        new_i = 0
        for i, state in enumerate(state_vector):
            if (i & mask) != 0:
                remaining_state_vector[new_i] = state
                new_i += 1
    else:
        # Qubit collapsed to |0>
        measured_qubit_state_vector = [1,0]
        mask = i << qubit_index
        new_i = 0
        for i, state in enumerate(state_vector):
            if (i & mask) == 0:
                remaining_state_vector[new_i] = state
                new_i += 1
    # Normalise
    remaining_state_vector = normalise(remaining_state_vector)
    return [remaining_state_vector, measured_qubit_state_vector]

def normalise(vector : np.array)->np.array:
    scaler = np.sqrt(np.sum(np.abs(vector)**2))
    return vector/scaler

# benchmark_get_probability1(range(1,16), 1000)
# benchmark_get_probability2(range(1,20), 1000)

def benchmark_get_probability_combined(n_qubits_range, n_trials):
    times1 = []
    times2 = []
    times3 = []
    for n_qubits in n_qubits_range:
        state_vector = np.random.uniform(-1, 1, size=2**n_qubits) + np.random.uniform(-1, 1, size=2**n_qubits) * 1j   

        start_time = time.time()
        for _ in range(n_trials):
            qubit_index = randint(0, n_qubits - 1)
            get_probability(state_vector, qubit_index, n_qubits)
        end_time = time.time()
        total_time = end_time - start_time
        average_time_per_trial1 = (total_time / n_trials) * 1000  # Convert to ms
        times1.append(average_time_per_trial1)
        
        start_time = time.time()
        for _ in range(n_trials):
            qubit_index = randint(0, n_qubits - 1)
            get_probability2(state_vector, qubit_index, n_qubits)
        end_time = time.time()
        total_time = end_time - start_time
        average_time_per_trial2 = (total_time / n_trials) * 1000  # Convert to ms
        times2.append(average_time_per_trial2)
        
        start_time = time.time()
        for _ in range(n_trials):
            qubit_index = randint(0, n_qubits - 1)
            get_probability3(state_vector, qubit_index, n_qubits)
        end_time = time.time()
        total_time = end_time - start_time
        average_time_per_trial1 = (total_time / n_trials) * 1000  # Convert to ms
        times3.append(average_time_per_trial1)

        print(f"Time taken for {n_qubits} qubits: get_probability1 - {average_time_per_trial1:.6f} ms, get_probability2 - {average_time_per_trial2:.6f} ms")

    plt.plot(n_qubits_range, times1, marker='o', label='get_probability1')
    plt.plot(n_qubits_range, times2, marker='o', label='get_probability2')
    plt.plot(n_qubits_range, times3, marker='o', label='get_probability3')
    plt.xlabel('Number of Qubits')
    plt.ylabel('Time (milliseconds)')
    plt.title('Time taken for get_probability()')
    plt.legend()
    plt.show()

def verify_algorithms(n_qubits):
    state_vector = np.random.rand(2**n_qubits) + np.random.rand(2**n_qubits) * 1j
    results = []
    for qubit_index in range(n_qubits):
        prob1 = get_probability(state_vector, qubit_index, n_qubits)
        prob2 = get_probability2(state_vector, qubit_index, n_qubits)
        prob3 = get_probability3(state_vector, qubit_index, n_qubits)
        # Check if the probabilities are equal within a small tolerance
        tolerance = 1e-10
        if abs(prob1 - prob2) < tolerance and abs(prob1 - prob3) < tolerance:
            results.append(True)
        else:
            results.append(False)
            print(f"Algorithms produce different results for qubit index {qubit_index}:")
            print("get_probability:", prob1)
            print("get_probability2:", prob2)
            print("get_probability3:", prob3)
    if all(results):
        print("All algorithms return the same result for all qubit indices.")
    else:
        print("Some algorithms produce different results for certain qubit indices.")

def verify_algorithms2(state_vector, qubit_index, n_qubits):
    prob1 = get_probability(state_vector, qubit_index, n_qubits)
    prob2 = get_probability2(state_vector, qubit_index, n_qubits)
    prob3 = get_probability3(state_vector, qubit_index, n_qubits)

    # Check if the probabilities are equal within a small tolerance
    tolerance = 1e-10
    if abs(prob1 - prob2) < tolerance and abs(prob1 - prob3) < tolerance:
        print("All algorithms return the same result.")
    else:
        print("Algorithms produce different results.")
        print("get_probability:", prob1)
        print("get_probability2:", prob2)
        print("get_probability3:", prob3)

# Example usage:
"""n_qubits = 2
state_vector = np.array([0,0,1,0])
qubit_index = 0
verify_algorithms2(state_vector, qubit_index, n_qubits)"""


verify_algorithms(8)
benchmark_get_probability_combined(range(1, 20), 500)
