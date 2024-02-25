# Revised version of qusim class
# Supports smaller vector sizes
# ----------------------------------------------------------------------------------------------------
# IMPORTS
import numpy as np
import Gates
# ----------------------------------------------------------------------------------------------------
# CLASSES
# A single qubit (currently unused)
class Qubit():
    def __init__(self, name):
        self.name = name

# System of a single/ multiple qubits
class Register():
    def __init__(self, qubits,  vector: np.array):
        self.qubits = qubits
        self.vector = vector

# System of all registers of qubits
class System():
    history : bool = False # If previous states should be stored
    def __init__(self):
        self.qubits = []  # Used to keep track of qubits
        self.registers = []

    def add_qubit(self, qubit: Qubit, vector: np.array):
        self.registers.append(Register([qubit], vector))
        self.qubits.append(qubit)

    # Apply a gate to a single qubit
    def apply_gate(self, gate, qubit):
        register = find_register(self, qubit)
        register_index = self.registers.index(register)
        register = apply_gate_register(register, qubit, gate)
        self.registers[register_index] = register

    # Applies a 2 input gate to 2 qubits
    def apply_gate_multiple(self, gate: np.array, qubit_a, qubit_b):
        # Find registers
        register_a = find_register(self, qubit_a)
        register_b = find_register(self, qubit_b)
        register = register_a
        # merge registers into a single register if theyre not already merged
        if register_a != register_b:
            register = combine_registers(register_a, register_b)
            self.registers.remove(register_b)

        # swap so that registers are next to each other
        # qubit_b should be placed at index_qubit_a+1
        index_qubit_a = register.qubits.index(qubit_a)
        target_index = index_qubit_a+1
        qubit_at_target = register.qubits[target_index]
        register = swap(register, qubit_at_target, qubit_b)
        # apply expanded gate
        gate = expand_gate(gate, index_qubit_a, len(register.qubits))
        register.vector = gate.dot(register.vector)
        # swap back
        register = swap(register, qubit_at_target, qubit_b)
        # update our state
        # set register_a to register to update state
        self.registers[self.registers.index(register_a)] = register


    # Merges all registers to one register and updates state
    def register_combined(self):
        register = self.get_as_register()
        self.registers = [register]
        return register

    # Returns all registers merged as a single register (does not update system state)
    def get_as_register(self):
        vector = self.registers[0].vector
        qubits = self.registers[0].qubits.copy() # Needs to be copied so we dont have side effects
        for i in range(1, len(self.registers)):
            register = self.registers[i]
            vector = np.kron(vector, register.vector)
            qubits += register.qubits
        return Register(vector=vector, qubits=qubits)

    # Sorts a register based on a qubit list to move qubit states to order given in qubits
    # Useful as final state may be shown in wrong order otherwise
    def sort_register(self, register : Register, sorted_qubits)->Register:
        # find bits to shift
        unsorted_qubits = register.qubits
        unsorted_vector = register.vector
        sorted_vector = []
        sorted_register = register
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
    
    # Measures a qubit
    # returns status of qubit after measurement as 0 or 1
    def measure(self, qubit):
        # Find register
        register = None
        register_index = None
        for r in self.registers:
            if qubit in r.qubits:
                register = r
                register_index = self.registers.index(r)
                break
        # Matrices used to remove states from matrix
        qubit_index = register.qubits.index(qubit)
        m0 = Gates.collapsed_vector([1,0], qubit_index, len(register.qubits))
        m1 = Gates.collapsed_vector([0,1], qubit_index, len(register.qubits))
        # Probabilites for given qubit to be 0 or 1
        p0 = np.sum(np.abs(m0*register.vector)**2)
        p1 = np.sum(np.abs(m1*register.vector)**2)
        # Collapsing qubit based on probabilites p0 or p1
        p = np.random.choice([0,1], p=[p0,p1])
        # Set probability to 0 for all states where qubit is equal to 0
        measured_state = None
        if p==0:
            measured_state=m0*register.vector
        else:
            measured_state=m1*register.vector
        # Normalise the measurement to fulfill property |a|^2+|b|^2+...==1
        norm_register = self.normalize(register)
        self.registers[register_index] = norm_register # Should update self as well
        return p # Returns probability of q_n=1 for qubit n
    
    # Normalises probabilities of register to 1 and returns resulting register
    def normalize(self, register : Register)->Register:
        scaler = np.sqrt(np.sum(np.abs(register.vector)**2))
        new_vector = register.vector/scaler
        return Register(register.qubits, new_vector)

    """def print_qubits(self):
        register = self.get_as_register()
        sorted_register = self.sort_register(register, self.qubits)
        for qubit in self.qubits:
            print(f"Qubit {qubit}:{self.getQubit(qubit)}")"""

    # Prints all registers
    def print_registers2(self):
        print("-------State of registers:---------------------------------------")
        for register in self.registers:
            print(f"Qubits:")
            for qubit in register.qubits:
                print(f"{qubit}: {self.get_probability(register, qubit)*100:.4}%")
            print(f"State:\n {register.vector}\n")
        print("-----------------------------------------------------------------")        

    # This has side effects
    def print_registers(self):
        print("-------State of registers:---------------------------------------")
        register = self.get_as_register()
        print(f"Qubits:")
        for qubit in register.qubits:
            print(f"{qubit}: {self.get_probability(register, qubit)*100:.4}%")
        print(f"State:\n {register.vector}\n")
        print("-----------------------------------------------------------------")        


    def get_probability(self, register, qubit)->float:
        qubit_index = register.qubits.index(qubit)
        m1 = Gates.collapsed_vector([0,1], qubit_index, len(register.qubits))
        p1 = np.sum(np.abs(m1*register.vector)**2)
        return p1

# Stores a quantum circuit
class Circuit():
    history : bool = False # If previous states should be stored
    def __init__(self):
        self.qubits = []  # Used to keep track of qubits
        self.registers = []


# ----------------------------------------------------------------------------------------------------
# METHODS
# Find a register where qubit is stored
def find_register(system, qubit):
    for register in system.registers:
        if qubit in register.qubits:
            return register
    return "Qubit not found"


def combine_registers(register_a, register_b):
    vector = np.kron(register_a.vector, register_b.vector)
    qubits = register_a.qubits + register_b.qubits
    return Register(qubits, vector)


def expand_gate(gate, index, qubit_count):
    # Check that gate fits at given index
    width = int(np.log2(len(gate)))
    assert index+width-1 < qubit_count, "Error! Gate does not fit"
    if index == 0:
        expanded_gate = gate
        i = width  # start position
        while i < qubit_count:
            expanded_gate = np.kron(expanded_gate, Gates.I)
            i += 1
    else:
        expanded_gate = Gates.I
        i = 1
        while i < qubit_count:
            if i == index:
                expanded_gate = np.kron(expanded_gate, gate)
                i += width  # increment counter by size of gate
            else:
                expanded_gate = np.kron(expanded_gate, Gates.I)
                i += 1
    return expanded_gate

# Swaps two qubits in a register
def swap(register: Register, qubit_a, qubit_b):
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

def check_adjacent(register, qubit_a, qubit_b):
    index_a = register.qubits.index(qubit_a)
    index_b = register.qubits.index(qubit_b)
    return abs(index_a-index_b) == 1

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
    return register

# ----------------------------------------------------------------------------------------------------
# DEMO
# Bell state
# q = System()
# q.add_qubit("A", np.array([1,0]))
# q.add_qubit("B", np.array([1,0]))
# q.apply_gate(Gates.H, "A")
# print(q.registers[0].vector)
# print(q.registers[1].vector)
# q.apply_gate_multiple(Gates.CNOT, ["A","B"])

# q = System()
# q.add_qubit("A", np.array([1,0]))
# q.add_qubit("B", np.array([1,0]))
# q.apply_gate(Gates.H, "A")
# print(q.registers[0].vector)
# print(q.registers[1].vector)
# q.apply_gate_multiple(Gates.CNOT, "A", "B")
# print(q.registers[0].vector)
# print(swap_bits(0, 0, 2))
# print(swap_bits(1, 0, 2))
# print(swap_bits(2, 0, 2))
