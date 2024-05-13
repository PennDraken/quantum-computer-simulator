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
    
    # note qubit_list contains the specific qubits
    def apply_gate(self, gate, qubit_list):
        # print("before swap--------------------")
        # for qubit in self.qubits:
        #     print(f"{qubit} {self.get_probability(qubit)}")
        # sort state vector and qubits based on qubit list
        self.sort_register(qubit_list)
        # print("after swap----------------------")
        # for qubit in self.qubits:
        #     print(f"{qubit} {self.get_probability(qubit)}")
        # expand gate
        first_qubit_index = self.qubits.index(qubit_list[0])
        gate = Gates.expand_gate(gate, first_qubit_index, len(self.qubits))
        # apply gate
        self.vector = gate.dot(self.vector)
        # print results
        # print("after gate applied----------------------")
        # for qubit in self.qubits:
        #     print(f"{qubit} {self.get_probability(qubit)}")
    
    # Merges a register with another register
    def merge(self, register):
        self.vector = np.kron(self.vector, register.vector)
        self.qubits = self.qubits + register.qubits
        return self


    def get_state_str(self)->str:
        return ""
        qubit_copy = copy.deepcopy(self.qubits)
        reversed_qubit_list = qubit_copy[::-1]
        register_reversed = self.sort_register(reversed_qubit_list) # TODO sort by indices
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
    
    def get_probability(self, qubit):
        qubit_index = self.qubits.index(qubit)
        qubit_count = len(self.qubits)
        state_vector = self.vector
        mask = 1 << (qubit_count - qubit_index - 1)
        masked_states = state_vector[np.bitwise_and(np.arange(len(state_vector)), mask) != 0]
        return np.sum(np.abs(masked_states) ** 2)    
    
    # Sorts a register based on a qubit list to move qubit states to order given in qubits
    # Useful as final state may be shown in wrong order otherwise
    # Updates registers original state
    def sort_register(self, sorted_qubits: list):#->Register
        # Note that sorted_qubits might not be the same size so we need to add the missing qubits
        register = copy.deepcopy(self)
        # find bits to shift
        unsorted_qubits = register.qubits
        for qubit in unsorted_qubits:
            if qubit not in sorted_qubits:
                sorted_qubits.append(qubit) # TODO more efficient possible
        sorted_register = copy.deepcopy(register)
        # swap state vector
        for i, source_qubit in enumerate(unsorted_qubits):
            target_qubit = sorted_qubits[i]
            if source_qubit!=target_qubit:
                # swap these two qubits
                source_i = unsorted_qubits.index(source_qubit) # same as i from for loop btw
                target_i = unsorted_qubits.index(target_qubit)
                sorted_register.vector = swap_vector(sorted_register.vector, source_i, target_i, len(sorted_qubits))
                # swap in our reference list
                unsorted_qubits[source_i] = target_qubit
                unsorted_qubits[target_i] = source_qubit
        # Finished
        self.vector = sorted_register.vector
        self.qubits = sorted_qubits
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
    # Swap state vector
    new_vector = swap_vector(new_vector, index_qubit_a, index_qubit_b, len(register.qubits))
    # Update order of our qubits list
    register.qubits[index_qubit_a] = qubit_b
    register.qubits[index_qubit_b] = qubit_a
    register.vector = new_vector
    return register

def swap_vector(state_vector, index_qubit_a, index_qubit_b, qubit_count):
    # Iterate through states vector and swap states
    for state_index in range(1, len(state_vector) - 1):
        # Calculate which element our current element should be replaced by
        new_state_index = swap_bits(state_index, index_qubit_a, index_qubit_b, qubit_count)
        # Check if index already has been swapped
        if new_state_index > state_index:
            # Perform swap
            state_vector[state_index], state_vector[new_state_index] = state_vector[new_state_index], state_vector[state_index]
    return state_vector

# Checks if two qubits are adjacent in a register. Not really used for anything right now.
def check_adjacent(register, qubit_a, qubit_b):
    index_a = register.qubits.index(qubit_a)
    index_b = register.qubits.index(qubit_b)
    return abs(index_a-index_b) == 1

def merge_registers(register_a, register_b):
    vector = np.kron(register_a.vector, register_b.vector)
    qubits = register_a.qubits + register_b.qubits
    return Register(qubits, vector)