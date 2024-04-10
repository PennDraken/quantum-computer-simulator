import numpy as np
import copy

if __name__ == "__main__":
    import Gates
    from system import System
    from bit_operations import swap_bits
else:
    from . import Gates # Import in same directory as qusim_class
    from .bit_operations import swap_bits

# System of a single/ multiple qubits
class Register():
    def __init__(self, qubits,  vector: np.array):
        self.qubits = qubits
        self.vector = vector
        self.label = None # TODO init this to a value
        self.state_str = None

    def get_label(self)->str:
        qubit_copy = copy.deepcopy(self.qubits)
        reversed_qubit_list = qubit_copy[::-1]
        label = f"|{''.join(reversed_qubit_list)}>"
        return label
    
    def get_state_str(self)->str:
        qubit_copy = copy.deepcopy(self.qubits)
        reversed_qubit_list = qubit_copy[::-1]
        register_reversed = self.sort_register(reversed_qubit_list)
        output_str = ""
        for i in range(0, len(self.vector)):
            state_val = register_reversed.vector[i].astype(complex) # Load state value as complex
            # binary_str = bin(i)[2:].zfill(len(self.qubits))
            # state_str = f"|{binary_str}> = {state_val}\n"
            state_val_real = state_val.real
            state_val_imag = state_val.imag
            state_str = f"{np.round(state_val_real, decimals=2)} + {np.round(state_val_imag, decimals=2)}j\n"
            output_str += state_str
        self.state_str = output_str
        return output_str
    
    # Sorts a register based on a qubit list to move qubit states to order given in qubits
    # Useful as final state may be shown in wrong order otherwise
    # Does not impact original state
    def sort_register(self, sorted_qubits):#->Register
        register = copy.deepcopy(self)
        # find bits to shift
        unsorted_qubits = register.qubits
        sorted_register = copy.deepcopy(register)
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
            sorted_register = swap(register, unsorted_qubits[i_a], unsorted_qubits[i_b])
        # Finished
        return sorted_register
    
    # Checks if probability adds up to 1 for all cases
    def verify(self, note : str = ""):
        probability = np.sum(np.abs(self.vector)**2)
        assert np.isclose(probability, 1), f"Register did not pass test: Probability = {probability}\n Note associated with this message: \n{note}"

# Applies gate to a single qubit in a register
def apply_gate_register(register, qubit, gate: np.array):
    # Expand gate based on index of qubit
    qubit_index = register.qubits.index(qubit)
    expanded_gate = gate if qubit_index == 0 else Gates.I  # initialize matrix correctly
    for i in range(1, len(register.qubits)):
        if i == qubit_index:
            expanded_gate = np.kron(expanded_gate, gate)
        else:
            expanded_gate = np.kron(expanded_gate, Gates.I)
    # Multiply this new gate with the state_vector
    register.vector = expanded_gate.dot(register.vector)
    register.verify(gate)
    return register

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

# Checks if two qubits are adjacent in a register. Not really used for anything right now.
def check_adjacent(register, qubit_a, qubit_b):
    index_a = register.qubits.index(qubit_a)
    index_b = register.qubits.index(qubit_b)
    return abs(index_a-index_b) == 1

def merge_registers(register_a, register_b):
    vector = np.kron(register_a.vector, register_b.vector)
    qubits = register_a.qubits + register_b.qubits
    return Register(qubits, vector)