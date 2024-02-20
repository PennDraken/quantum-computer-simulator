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
        self.name=name

# System of a single/ multiple qubits
class Register():
    def __init__(self, qubits,  vector : np.array):
        self.qubits=qubits
        self.vector=vector

# System of all registers of qubits
class System():
    def __init__(self):
        # self.qubits=[]
        self.registers=[]

    def add_qubit(self, qubit : Qubit, vector : np.array):
        # self.qubits.append(qubit)
        self.registers.append(Register([qubit]), vector)


# ----------------------------------------------------------------------------------------------------
# METHODS
# Find a register where qubit is stored
def find_register(system : System, qubit : Qubit):
    for register in System:
        if qubit in register.qubits:
            return qubit
    return "Qubit not found"

# Applies gate to a single qubit
def apply_gate(system : System, qubit : Qubit, gate : np.array):
    # Find which register the qubit is linked to
    register : Register = find_register(system, qubit)
    # Expand gate based on index of qubit
    qubit_index = register.qubits.index(qubit)
    expanded_gate = gate if qubit_index == 0 else Gates.I # initialize matrix correctly
    for i in range(1, len(register.qubits)):
        if i == qubit_index:
            expanded_gate = np.kron(expanded_gate, gate)
        else:
            expanded_gate = np.kron(expanded_gate, Gates.I)
    # Multiply this new gate with the state_vector
    return expanded_gate.dot(register.vector)

# ----------------------------------------------------------------------------------------------------
# DEMO
# Bell state
q = System()
q.add_qubit(Qubit("A"), np.array([1,0]))
q.add_qubit(Qubit("B"), np.array([1,0]))
