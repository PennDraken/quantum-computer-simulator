# Revised version of qusim class
# Supports smaller vector sizes
# ----------------------------------------------------------------------------------------------------
# IMPORTS
import numpy as np
import copy
import re
import Gates
from register import Register
from register_manager import Registers_Manager
from bit_functions import *

# ----------------------------------------------------------------------------------------------------
# CLASSES
# A single qubit (currently unused)
class Qubit():
    def __init__(self, name):
        self.name = name

# Stores a quantum circuit
class Circuit():
    history : bool = False  # If previous states should be stored
    def __init__(self, description):
        self.systems = []  # Index corresponds to state in circuit
        self.history : bool = True
        self.show_output : bool = False
        # First element is qubit list, rest are gate operations
        # self.description = [["A","B"],"H 0","CNOT 0 1"]
        self.description = description
        # initialize first system based on setup state
        qubits = self.description[0]
        system = Registers_Manager()
        for qubit in qubits:
            system.add_qubit(qubit, Gates.zero_state)
        self.systems.append(system)
        self.position = 0

    # Steps forward in circuit
    # Adds a new system to our systems
    def step_fwd(self):
        if self.position+1>=len(self.description):
            return # We're out out bounds
        self.position+=1
        # Start interpreting operation type
        operation = self.description[self.position].split(' ')
        op_type : str = operation[0]

        if op_type=="measure":
            # We measure qubit
            qubits_indices = []
            for i in range(1, len(operation)):
                qubits_indices.append(int(operation[i]))
            # Duplicate system
            new_system : Registers_Manager = copy.deepcopy(self.systems[self.position-1])
            # Apply measure
            qubit = new_system.qubits[qubits_indices[0]]
            p = new_system.measure(qubit)
            if self.show_output:
                print(f"Qubit {qubit} collapsed to {p}") # TODO should only print when print is turned on
        else:
            # It is gate
            gate = Gates.string_to_gate(op_type)
            qubits_indices = []
            for i in range(1, len(operation)):
                qubits_indices.append(int(operation[i])) # TODO Should we use names instead? Or perhaps add support for bot
            # Duplicate system
            new_system : Registers_Manager = copy.deepcopy(self.systems[self.position-1])
            # Apply gate
            if len(qubits_indices)==1: # TODO We should probably combine these apply gates into one function
                new_system.apply_gate(gate, new_system.qubits[qubits_indices[0]])
            elif len(gate)==2:
                # this is an if based single qubit gate
                # find vale of "qubit" (a bit in this case). If bit==1 we will apply gate
                for register in new_system.registers:
                    if register.qubits==[new_system.qubits[qubits_indices[1]]]:
                        if np.array_equal(register.vector, np.array([0, 1])):
                            # print("equal to 1")
                            # bit was 1 so we apply gate
                            new_system.apply_gate(gate, new_system.qubits[qubits_indices[0]])
                            break
            # Multi qubit gate
            elif len(qubits_indices)==2:
                new_system.apply_gate_multiple(gate, new_system.qubits[qubits_indices[0]], new_system.qubits[qubits_indices[1]])
        
        # Add to our history
        self.systems.append(new_system)
        # Print output
        if self.show_output:
            print(f"Stepped forward {operation}")
            # self.systems[self.position].print_merged_register()
            self.systems[self.position].print_merged_register_QC()

    # Steps backwards in circuit
    # Removes state at current position
    def step_back(self):
        if self.position<=0:
            return # Early return as we cant go more left
        # Remove state
        del self.systems[self.position]
        self.position-=1 # Go left in system
        if self.show_output:
            # self.systems[self.position].print_merged_register()
            self.systems[self.position].print_merged_register_QC()


    # Runts through the cicuit as fast as possible
    def run(self):
        pass

    # Used for frontend. Converts a circuit to a format that frontend can use
    def as_frontend_gate_list(self):
        description = self.description
        converted_list = []
        for item in description[1:]:
            parts = re.split(r'\s+', item.strip())
            gate = parts[0]
            qubits = [int(qubit) for qubit in re.findall(r'\d+', ' '.join(parts[1:]))]
            converted_list.append((gate, qubits))
        return converted_list
    
    # Used for frontend. Converts and sets list which is frontend gate representation to a format that backend can use.
    def set_circuit_from_frontend_gate_list(self, gate_list):
        description = []
        # Set qubits
        description.append(self.systems[0].qubits)
        for gate_str, qubits in gate_list:
            description.append(gate_str + " " + " ".join(map(str, qubits)))
        self.description = description

# ----------------------------------------------------------------------------------------------------
# METHODS

# Cheks if two qubits are adjacent in a register. Not really used for anything right now.
def check_adjacent(register, qubit_a, qubit_b):
    index_a = register.qubits.index(qubit_a)
    index_b = register.qubits.index(qubit_b)
    return abs(index_a-index_b) == 1


# Returns the instructions for the circuit of the shor subroutine
def shor_subroutine_circuit(guess : int, N : int):
    n = (np.ceil(np.log2(N)))
    qubits = []
    for i in range(n*3):
        qubits.append("q" + str(i))
    temp = []
    temp.append(qubits)
    for k in range(n*2):
        temp.append("H " + str(k))
    temp.append("X " + str(n*2))
    tGate = ("amodN(" + str(guess) +","+str(N)+")")
    for l in range(n*2):
        tString = tGate
        tString = tString + " " + str(l)
        for m in range(n*2, n*3):
           tString = tString + " " + str(m)
        temp.append(tString)  
    tQFT = "QFT(" + str(N) +")"
    for f in range(n*2):
        tQFT = tQFT + " " + str(f)
    temp.append(tQFT)
    for g in range(n*2):
        temp.append("measure " + str(g))
    #print(temp[0:len(temp)])
    return temp

# ----------------------------------------------------------------------------------------------------
"""q = System()
q.add_qubit("A", Gates.zero_state)
q.add_qubit("B", Gates.one_state)
q.add_qubit("C", Gates.zero_state)
q.add_qubit("D", Gates.zero_state)
q.add_qubit("E", Gates.one_state)
q.add_qubit("F", Gates.zero_state)
q.apply_gate_qubit_list(Gates.CNOT, [3,2,5])"""
