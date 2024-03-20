# Revised version of qusim class
# Supports smaller vector sizes
# ----------------------------------------------------------------------------------------------------
# IMPORTS
import numpy as np
import copy
import re
if __name__ == "__main__":
    import Gates
else:
    from . import Gates # Import in same directory as qusim_class
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
        register_reversed = sort_register(copy.deepcopy(self), reversed_qubit_list)
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

# System of all registers of qubits
class System():
    def __init__(self):
        self.qubits=[] # Used to keep track of qubits
        self.registers=[]

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

    # Applies a gate to a qubit list
    def apply_gate_qubit_list(self, gate: np.array, qubit_index_list: []):
        # Get all different register
        unmerged_registers = []
        for qubit_index in qubit_index_list:
            qubit = self.qubits[qubit_index]
            unmerged_registers.append(find_register(self, qubit))
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
        gate = expand_gate(gate, 0, len(merged_register.qubits))
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
        register_reversed = sort_register(register, sorted_register_qubits)
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
        system = System()
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
            new_system : System = copy.deepcopy(self.systems[self.position-1])
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
            new_system : System = copy.deepcopy(self.systems[self.position-1])
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


    # Runs through the cicuit as fast as possible
    def run(self):
        while self.position + 1<len(self.description):
            self.step_fwd()

    # Gets current system as a single register
    def single_register(self):
        system = self.systems[self.position]
        single_register = system.get_as_register()
        return single_register

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
# Find a register where qubit is stored
def find_register(system, qubit):
    for register in system.registers:
        if qubit in register.qubits:
            return register
    return "Qubit not found"

 # Sorts a register based on a qubit list to move qubit states to order given in qubits
# Useful as final state may be shown in wrong order otherwise
def sort_register(register: Register, sorted_qubits)->Register:
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

def merge_registers(register_a, register_b):
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

# Inserts a bit into a binary number at location n
# Example: 0b00 Insert bit at n=1 => 0b010
def insert_bit(binary_num, bit, n):
    # Shift the number to the right by n bits
    mask = 1 << n
    # Create a mask to clear the bit at position n
    cleared_bit = binary_num & ~mask
    # Set the bit at position n to the desired value
    result = cleared_bit | ((bit & 1) << n)
    return result

# Cheks if two qubits are adjacent in a register. Not really used for anything right now.
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
