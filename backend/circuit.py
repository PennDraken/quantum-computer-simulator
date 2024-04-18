# ----------------------------------------------------------------------------------------------------
# IMPORTS
import numpy as np
import copy
import re
if __name__ == "__main__":
    import Gates
    from system import System
else:
    from . import Gates # Import in same directory as qusim_class
    from .system import System

# ----------------------------------------------------------------------------------------------------
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
        elif op_type=="label":
            new_system : System = copy.deepcopy(self.systems[self.position-1])
        else:
            # It is gate
            gate = Gates.string_to_gate(op_type)
            qubits_indices = []
            # Convert to useable data type
            for i in range(1, len(operation)):
                qubits_indices.append(int(operation[i])) # TODO Should we use names instead? Or perhaps add support for bot
            # Duplicate system
            new_system : System = copy.deepcopy(self.systems[self.position-1])
            # Apply gate
            if len(qubits_indices)==1: # TODO We should probably combine these apply gates into one function
                new_system.apply_gate(gate, new_system.qubits[qubits_indices[0]])
            # Bit controlled gate
            elif len(gate)==2:
                # this is an if controlled single qubit gate (controlled by a bit (measured register))
                # find value of "qubit" (a bit in this case). If bit==1 we will apply gate
                for register in new_system.registers:
                    if register.qubits==[new_system.qubits[qubits_indices[0]]]:
                        if np.array_equal(register.vector, np.array([0, 1])):
                            # print("equal to 1")
                            # bit was 1 so we apply gate
                            new_system.apply_gate(gate, new_system.qubits[qubits_indices[1]])
                            break
            # Multi qubit gate
            elif len(qubits_indices)==2:
                # new_system.apply_gate_multiple(gate, new_system.qubits[qubits_indices[0]], new_system.qubits[qubits_indices[1]])
                new_system.apply_gate_multiple(gate, new_system.qubits[qubits_indices[0]], new_system.qubits[qubits_indices[1]])
            # Multi qubit gate that is more than 2
            elif len(qubits_indices)>2:
                new_system.apply_gate_qubit_list(gate, qubits_indices)

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


    # Runs through the cicuit to the end position
    def run(self):
        while self.position + 1<len(self.description):
            self.step_fwd()

    # Resets the circuit to initial starting position
    def reset(self):
        self.position = 0
        self.systems = [self.systems[0]]
        

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
            if gate!="label":
                qubits = [int(qubit) for qubit in re.findall(r'\d+', ' '.join(parts[1:]))]
                converted_list.append((gate, qubits))
            else:
                label_text = parts[1] # Load the text
                converted_list.append((gate, label_text))
        return converted_list
    
    # Used for frontend. Converts and sets list which is frontend gate representation to a format that backend can use.
    def set_circuit_from_frontend_gate_list(self, gate_list):
        description = []
        # Set qubits
        description.append(self.systems[0].qubits)
        for gate_str, qubits in gate_list:
            description.append(gate_str + " " + " ".join(map(str, qubits)))
        self.description = description
