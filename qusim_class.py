# Revised version of qusim class
# Supports smaller vector sizes
# ----------------------------------------------------------------------------------------------------
# IMPORTS
import numpy as np
import Gates
# ----------------------------------------------------------------------------------------------------
# CLASSES
# A single qubit


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
    def __init__(self):
        self.qubits = []  # Used to store order of qubits
        self.registers = []

    def add_qubit(self, qubit: Qubit, vector: np.array):
        # self.qubits.append(qubit)
        self.registers.append(Register([qubit], vector))

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
        # swap so that registers are next to each other
        # qubit_b should be placed at index_qubit_a+1
        index_qubit_a = register.qubits.index(qubit_a)
        target_index = index_qubit_a+1
        qubit_at_target = register.qubits[target_index]
        register = swap(register, qubit_at_target, qubit_b)
        # apply expanded gate
        gate = expand_gate(gate, index_qubit_a, len(register.qubits))
        register.vector = register.vector.dot(gate)
        # swap back
        register = swap(register, qubit_at_target, qubit_b)
        # update our state
        # set register_a to register to update state
        self.registers[self.registers.index(register_a)] = register
        # delete register_b if theyre different
        if register_a != register_b:
            self.registers.remove(register_b)

    # Combines all registers to one register and updates state
    def register_combined(self):
        register = self.as_register()
        self.registers = [register]

    # Returns all registers as a single register (does not update system state)
    def as_register(self):
        vector = self.registers[0].vector
        qubits = self.registers[0].qubits
        for i in range(1, len(self.registers)):
            register = self.registers[i]
            vector = np.kron(vector, register.vector)
            qubits += register.qubits
        return Register(vector=vector, qubits=qubits)

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
