from register import Register
import numpy as np
import Gates
import copy
from bit_functions import *

# System of all registers of qubits
class Registers_Manager():
    def __init__(self):
        self.qubits=[] # Used to keep track of qubits
        self.registers=[]

    def add_qubit(self, qubit, vector):
        self.registers.append(Register([qubit], vector))
        self.qubits.append(qubit)

    # Apply a gate to a single qubit
    def apply_gate(self, gate, qubit):
        register = self.find_register(self, qubit)
        register_index = self.registers.index(register)
        # register = apply_gate_register(register, qubit, gate)
        register = register.apply_gate(qubit, gate)
        self.registers[register_index] = register

    # Applies a 2 input gate to 2 qubits
    def apply_gate_multiple(self, gate: np.array, qubit_a, qubit_b):
        # Find registers
        register_a = self.find_register(self, qubit_a)
        register_b = self.find_register(self, qubit_b)
        register = register_a
        # merge registers into a single register if theyre not already merged
        if register_a != register_b:
            # if self.qubits.index(qubit_a)<self.qubits.index(qubit_b):
            register = merge_registers(register_a, register_b)
            self.registers.remove(register_b)

        # swap so that registers are next to each other
        # qubit_b should be placed at index_qubit_a+1
        index_qubit_a = register.qubits.index(qubit_a)
        index_qubit_b = register.qubits.index(qubit_b)
        if index_qubit_a < index_qubit_b:
            # Move qubit b so that they're adjacent
            target_index = index_qubit_a+1
            qubit_at_target = register.qubits[target_index]
            register = register.swap(qubit_at_target, qubit_b)
            # apply expanded gate
            gate = Gates.expand_gate(gate, index_qubit_a, len(register.qubits))
            register.vector = gate.dot(register.vector)
            # swap back
            register = register.swap(qubit_at_target, qubit_b)
            # update our state
            # set register_a to register to update state
            self.registers[self.registers.index(register_a)] = register
        else:
            # First swap qubit a and b, so qubit a is to the left of qubit b
            register = register.swap(qubit_b, qubit_a)
            target_index = index_qubit_b+1
            qubit_at_target = register.qubits[target_index]
            register = register.swap(qubit_at_target, qubit_b)
            # apply expanded gate
            gate = Gates.expand_gate(gate, index_qubit_b, len(register.qubits))
            register.vector = gate.dot(register.vector)
            # swap back
            register = register.swap(qubit_at_target, qubit_b)
            register = register.swap(register, qubit_b, qubit_a)
            # update our state
            # set register_a to register to update state
            self.registers[self.registers.index(register_a)] = register

    # Applies a gate to a qubit list
    def apply_gate_qubit_list(self, gate: np.array, qubit_index_list: []):
        # Get all different register
        unmerged_registers = []
        for qubit_index in qubit_index_list:
            qubit = self.qubits[qubit_index]
            unmerged_registers.append(self.find_register(self, qubit))
        # Remove duplicates (by casting to dict and back to list)
        unmerged_registers = list(dict.fromkeys(unmerged_registers))    
        # Merge registers
        merged_register = unmerged_registers.pop() # Remove first element
        register_index = self.registers.index(merged_register)
        self.registers.remove(merged_register)
        for register in unmerged_registers:
            merged_register = merge_registers(merged_register, register)
            self.registers.remove(register) # Remove from register self list

        # Store indices of how qubits are stored in register
        unswapped_qubits_index_list = []
        for qubit in merged_register.qubits:
            state_index = self.qubits.index(qubit)
            unswapped_qubits_index_list.append(state_index)
        # Perform swap operation
        ordered_vector = copy.deepcopy(merged_register.vector)
        for state_index in range(0,len(merged_register.vector)):
            new_index = state_index
            for index in range(0, len(qubit_index_list)):
                # Find the bits to swap in state_index to calculate where the state should be placed
                index_original = unswapped_qubits_index_list[index]
                index_target   = qubit_index_list[index]
                new_index = swap_bits(new_index, index_original, index_target, 2**len(merged_register.qubits))
            ordered_vector[new_index] = merged_register.vector[state_index]
        # Apply gate
        gate = Gates.expand_gate(gate, 0, len(merged_register.qubits))
        ordered_vector = gate.dot(ordered_vector)
        # Swap back
        for state_index in range(0,len(merged_register.vector)):
            new_index = state_index
            for index in range(0, len(qubit_index_list)):
                # Find the bits to swap in state_index to calculate where the state should be placed
                index_original = unswapped_qubits_index_list[index]
                index_target   = qubit_index_list[index]
                new_index = swap_bits(new_index, index_original, index_target, 2**len(merged_register.qubits))
            merged_register.vector[new_index] = ordered_vector[state_index]
        # Sort register into qubit order TODO
        # Update our register state
        self.registers.append(merged_register)

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

    # Measures a qubit
    # returns state of qubit after measurement as 0 or 1
    # Also seperates the measured qubit into a seperate register
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
        norm_vector = self.normalize(measured_state)
        # Seperate out the measured qubit and remaining qubits into different registers
        new_vector = np.zeros(2**(len(register.qubits) - 1), dtype=complex)
        for index in range(0, len(new_vector)):
            # calculate the indices of the elements that should be put at index in new_vector
            index_a = insert_bit(index, 0, len(register.qubits) - qubit_index - 1)
            index_b = insert_bit(index, 1, len(register.qubits) - qubit_index - 1)
            # add the two elements that should be put into new indices
            new_vector[index] = norm_vector[index_a] + norm_vector[index_b]
        # Add the two new registers to system self
        measured_register = Register([qubit], np.array([1 if p == 0 else 0, p])) # Create vector [1,0] or [0,1] based on p (result of measurement)
        register.qubits.remove(qubit) # Our other register should no longer contain measured qubit
        self.registers[register_index] = Register(register.qubits, new_vector) # We update self to contain this register
        self.registers.append(measured_register)
        return p # Returns probability of q_n=1 for qubit n
    
    # Find and returns the register where a qubit is contained
    def find_register(self, qubit):
        for register in self.registers:
            if qubit in register.qubits:
                return register
        return "Qubit not found"
    
    # Normalises probabilities of vector and returns it
    def normalize(self, vector : np.array)->Register:
        scaler = np.sqrt(np.sum(np.abs(vector)**2))
        new_vector = vector/scaler
        return new_vector

    # Prints all registers
    def print_registers(self):
        print("-------State of registers:---------------------------------------")
        for register in self.registers:
            print(f"Qubits:")
            for qubit in register.qubits:
                print(f"{qubit}: {self.get_probability(register, qubit)*100:.4}%")
            print(f"State:\n {register.vector}\n")
        print("-----------------------------------------------------------------")        

    def print_merged_register(self):
        print("-------State of registers:---------------------------------------")
        register = self.get_as_register()
        print(f"Qubits:")
        for qubit in register.qubits:
            print(f"{qubit}: {self.get_probability(register, qubit)*100:.4}%")
        # Print the vector matrix
        print("\nState:")
        print(f"|{''.join(register.qubits)}>")
        for i in range(0, len(register.vector)):
            state_val = register.vector[i]
            binary_str = bin(i)[2:].zfill(len(register.qubits))
            print(f"|{binary_str}> = {state_val}")
        print("-----------------------------------------------------------------")        

    # Prints the register in the style of QC
    def print_merged_register_QC(self):
        print("-------State of registers:---------------------------------------")
        register = self.get_as_register()
        print(f"Qubits:")
        for qubit in register.qubits:
            print(f"{qubit}: {self.get_probability(register, qubit)*100:.4}%")
        # Print the vector matrix
        print("\nState:")

        # Sort the qubits based on the list in self.systems.qubits
        reversed_qubit_key = self.qubits[::-1]
        sorted_register_qubits = sorted(register.qubits, key=lambda x: reversed_qubit_key.index(x))
        print(f"|{''.join(sorted_register_qubits)}>")
        # Resort state vector based on new qubit list
        register_copy = copy.deepcopy(register)
        register_reversed = register_copy.sort(sorted_register_qubits)
        for i in range(0, len(register.vector)):
            state_val = register_reversed.vector[i]
            binary_str = bin(i)[2:].zfill(len(register.qubits)) # Converts index to binary representation
            print(f"|{binary_str}> = {state_val}")
        print("-----------------------------------------------------------------")        


    def get_probability(self, register, qubit)->float:
        qubit_index = register.qubits.index(qubit)
        m1 = Gates.collapsed_vector([0,1], qubit_index, len(register.qubits))
        p1 = np.sum(np.abs(m1*register.vector)**2)
        return float(p1)
    
# Merges two registers into one # TODO Sort based on qubit list
def merge_registers(register_a, register_b):
    vector = np.kron(register_a.vector, register_b.vector)
    qubits = register_a.qubits + register_b.qubits
    return Register(qubits, vector)