import numpy as np
import copy
import Gates

# A register contains states for a set of qubits
class Register():
    def __init__(self, qubits,  vector: np.array):
        self.qubits = qubits
        self.vector = vector
        self.label = None # TODO init this to a value
        self.state_str = None

    # Applies gate to a single qubit in a register
    def apply_gate(self, qubit, gate: np.array):
        # Expand gate based on index of qubit
        qubit_index = self.qubits.index(qubit)
        expanded_gate = gate if qubit_index == 0 else Gates.I  # initialize matrix correctly
        for i in range(1, len(self.qubits)):
            if i == qubit_index:
                expanded_gate = np.kron(expanded_gate, gate)
            else:
                expanded_gate = np.kron(expanded_gate, Gates.I)
        # Multiply this new gate with the state_vector
        self.vector = expanded_gate.dot(self.vector)
        return self
    
    # Swaps two qubits in a register
    def swap(self, qubit_a, qubit_b):
        if qubit_a==qubit_b:
            return self # early return
        index_qubit_a = self.qubits.index(qubit_a)
        index_qubit_b = self.qubits.index(qubit_b)
        new_vector : np.array = self.vector.copy()
        # Iterate through states vector and swap states
        for index in range(0, len(self.vector)):
            # Calculate wich element our current element should be replaced by
            new_index = swap_bits(index, index_qubit_a, index_qubit_b, len(self.qubits))
            new_vector[index] = self.vector[new_index]
        # Update order of our qubits list
        self.qubits[index_qubit_a] = qubit_b
        self.qubits[index_qubit_b] = qubit_a
        self.vector = new_vector
        return self

    # Sorts a register based on a qubit list to move qubit states in accordance of order given in qubits
    # Note: This is applied directly to register, if you want to sort without side effects (for example for printing), you need to create a copy of the register first
    def sort(self, sorted_qubits):
        # find bits to shift
        unsorted_qubits = self.qubits
        sorted_register = copy.deepcopy(self)
        # find all bits that should be swapped
        bits_to_swap = []
        for i in range(len(unsorted_qubits)):
            q = unsorted_qubits[i]
            # find where this q should be moved to in sorted_qubits
            target_i = sorted_qubits.index(q)
            # check if swap is not already in bits_to_swap (no duplicate swaps)
            if not (target_i, i) in bits_to_swap:
                bits_to_swap.append((i, target_i))
        # swap state vector
        for swap_pair in bits_to_swap:
            i_a = swap_pair[0]
            i_b = swap_pair[1]
            sorted_register = swap(self, unsorted_qubits[i_a], unsorted_qubits[i_b])
        # Finished
        self = sorted_register
        return sorted_register

    # Returns a string representing the qubits in a register.
    # Example: |ABC>
    def get_label(self)->str:
        qubit_copy = copy.deepcopy(self.qubits)
        reversed_qubit_list = qubit_copy[::-1]
        label = f"|{''.join(reversed_qubit_list)}>"
        return label
    
    # Returns a string representing all states in a register
    def get_state_str(self)->str:
        qubit_copy = copy.deepcopy(self.qubits)
        reversed_qubit_list = qubit_copy[::-1]
        register_copy = copy.deepcopy(self)
        register_reversed = register_copy.sort(reversed_qubit_list)
        output_str = ""
        for i in range(0, len(self.vector)):
            state_val = register_reversed.vector[i].astype(complex) # Load state value as complex
            state_val_real = state_val.real
            state_val_imag = state_val.imag
            state_str = f"{np.round(state_val_real, decimals=2)} + {np.round(state_val_imag, decimals=2)}j\n"
            output_str += state_str
        # self.state_str = output_str # TODO Better performance by not recalculating every frame
        return output_str

# Swaps two qubits in a register
def swap(register: Register, qubit_a, qubit_b):
    if qubit_a==qubit_b:
        return register # early return
    index_qubit_a = register.qubits.index(qubit_a)
    index_qubit_b = register.qubits.index(qubit_b)
    new_vector : np.array = register.vector.copy()
    # Iterate through states vector and swap states
    for index in range(0, len(register.vector)):
        # Calculate wich element our current element should be replaced by
        new_index = swap_bits(index, index_qubit_a, index_qubit_b, len(register.qubits))
        new_vector[index] = register.vector[new_index]
    # Update order of our qubits list
    register.qubits[index_qubit_a] = qubit_b
    register.qubits[index_qubit_b] = qubit_a
    register.vector = new_vector
    return register

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

# Cheks if two qubits are adjacent in a register. Not really used for anything right now.
def check_adjacent(register, qubit_a, qubit_b):
    index_a = register.qubits.index(qubit_a)
    index_b = register.qubits.index(qubit_b)
    return abs(index_a-index_b) == 1

