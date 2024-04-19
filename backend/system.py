import numpy as np
import copy


if __name__ == "__main__":
    import Gates
    from Gates import expand_gate
    from register import Register, apply_gate_register, merge_registers, swap
    from bit_operations import swap_bits, insert_bit
else:
    from . import Gates
    from .Gates import expand_gate # Import in same directory as qusim_class
    from .register import Register, apply_gate_register, merge_registers, swap
    from .bit_operations import swap_bits, insert_bit

# System of all registers of qubits
class System():
    def __init__(self):
        self.qubits=[] # Used to keep track of qubits
        self.registers=[]

    def add_qubit(self, qubit, vector: np.array):
        self.registers.append(Register([qubit], vector))
        self.qubits.append(qubit)

    # Apply a gate to a single qubit
    def apply_gate(self, gate, qubit):
        register = find_register(self, qubit)
        register_index = self.registers.index(register)
        register = apply_gate_register(register, qubit, gate)
        self.registers[register_index] = register


    # Applies a 2 input gate to 2 qubits in a system
    def apply_gate_multiple(self, gate: np.array, qubit_a, qubit_b):
        # Find registers
        register_a = find_register(self, qubit_a)
        register_b = find_register(self, qubit_b)
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
            register = swap(register, qubit_at_target, qubit_b)
            # apply expanded gate
            gate = expand_gate(gate, index_qubit_a, len(register.qubits))
            register.vector = gate.dot(register.vector)
            # swap back
            register = swap(register, qubit_at_target, qubit_b)
            # update our state
            # set register_a to register to update state
            self.registers[self.registers.index(register_a)] = register
        else:
            # First swap qubit a and b, so qubit a is to the left of qubit b
            register = swap(register, qubit_b, qubit_a)
            target_index = index_qubit_b+1
            qubit_at_target = register.qubits[target_index]
            register = swap(register, qubit_at_target, qubit_b)
            # apply expanded gate
            gate = expand_gate(gate, index_qubit_b, len(register.qubits))
            register.vector = gate.dot(register.vector)
            # swap back
            register = swap(register, qubit_at_target, qubit_b)
            register = swap(register, qubit_b, qubit_a)
            # update our state
            # set register_a to register to update state
            self.registers[self.registers.index(register_a)] = register


    # Applies a gate to a qubit list (of integers)
    def apply_gate_qubit_list(self, gate: np.array, qubit_index_list: []):
        # Get all different register
        unmerged_registers = []
        sorted_qubit_index_list = []
        for qubit_index in qubit_index_list:
            qubit_in_system = self.qubits[qubit_index]
            sorted_qubit_index_list.append(qubit_in_system)
            unmerged_registers.append(find_register(self, qubit_in_system))
        # Remove duplicates (by casting to dict and back to list)
        unmerged_registers = list(dict.fromkeys(unmerged_registers))    
        # Merge registers
        merged_register = unmerged_registers.pop(0) # Remove first element
        register_index = self.registers.index(merged_register)
        self.registers.remove(merged_register)
        for register in unmerged_registers:
            merged_register = merge_registers(merged_register, register)
            self.registers.remove(register) # Remove from register self list

        # Find order of swaps
        original_qubits = merged_register.qubits
        original_qubit_index_list = []
        for qubit in merged_register.qubits:
            original_qubit_index_list.append(self.qubits.index(qubit))
        
        sorted_qubit_index_list = sort_list_by_key(original_qubit_index_list, qubit_index_list)

        sorted_qubits = []
        for qubit_index in sorted_qubit_index_list:
            qubit = self.qubits[qubit_index]
            sorted_qubits.append(qubit)

        # Sort register
        merged_register = merged_register.sort_register(sorted_qubits)
        
        # Apply gate
        gate_apply_index = merged_register.qubits.index(self.qubits[qubit_index_list[0]])
        gate = expand_gate(gate, gate_apply_index, len(merged_register.qubits))
        merged_register.vector = gate.dot(merged_register.vector)

        # Resort register
        merged_register = merged_register.sort_register(original_qubits)

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
        # assert p0+p1==1, f"Error regarding probabilities p(0)={p0} + p(1)={p1} = {p0 + p1}"
        assert abs(1-p1)+p1==1, f"Error regarding probabilities p(0)={p0}, p(1)={p1},  |1-p1|+p1 ={abs(1-p1)+p1}, p0 + p1 ={p0 + p1}"
        p = np.random.choice([0,1], p=[1-p1,p1])
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
        new_vector = self.normalize(new_vector)
        # Add the two new registers to system self
        measured_register = Register([qubit], np.array([1 if p == 0 else 0, p])) # Create vector [1,0] or [0,1] based on p (result of measurement)
        register.qubits.remove(qubit) # Our other register should no longer contain measured qubit
        remaining_register = Register(register.qubits, new_vector)
        remaining_register.verify(f"Measure failed {qubit}")
        self.registers[register_index] = remaining_register # We update self to contain this register
        self.registers.append(measured_register)
        return p # Returns probability of q_n=1 for qubit n
    
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
        register_reversed = register.sort_register(sorted_register_qubits)
        for i in range(0, len(register.vector)):
            state_val = register_reversed.vector[i]
            binary_str = bin(i)[2:].zfill(len(register.qubits))
            print(f"|{binary_str}> = {state_val}")
        print("-----------------------------------------------------------------")        


    def get_probability(self, register, qubit)->float:
        qubit_index = register.qubits.index(qubit)
        m1 = Gates.collapsed_vector([0,1], qubit_index, len(register.qubits))
        p1 = np.sum(np.abs(m1*register.vector)**2)
        return float(p1)
    
# Find a register where qubit is stored
def find_register(system, qubit):
    for register in system.registers:
        if qubit in register.qubits:
            return register
    return "Qubit not found"

# Useful for setting qubit state in a specific order
def sort_list_by_key(input_list, key):
    # Create a dictionary to store the indices of numbers in the key list
    key_indices = {num: i for i, num in enumerate(key)}
    # Sort the input list based on the indices of numbers in the key list
    sorted_list = sorted(input_list, key=lambda x: key_indices.get(x, float('inf')))
    return sorted_list
