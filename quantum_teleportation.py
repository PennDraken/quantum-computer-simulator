import qusim_class
import Gates
import numpy as np

# This algorithm transports the state of qubit 0 to qubit 2
#----------------------------------------------------------
q = qusim_class.System() # init state
# Add qubits
q.add_qubit("A", Gates.zero_state)
q.add_qubit("B", Gates.zero_state)
q.add_qubit("C", Gates.zero_state)

q.apply_gate(Gates.Ry(np.pi/4), "A") # Set value of qubit to be teleported to |alpha|^2=0.146

# Constructing bell state on qubits 1 and 2
q.apply_gate(Gates.H, "B")
q.apply_gate_multiple(Gates.CNOT, "B", "C")

# Show starting state (after Bell state)
print("---Qubits initialized (q1 and q2 are in a bell state)")
q.print_registers()
# q0=q.getQubit(0)
# print(np.abs(q0[0])**2)

# CNOT -> Hadamard
q.apply_gate_multiple(Gates.CNOT, "A", "B")
q.print_registers()
q.apply_gate(Gates.H, "A")
q.print_registers()

# Measurement
bit0=q.measure("A")
bit1=q.measure("B")

# Error correction
# X
if bit1==1:
    q.apply_gate(Gates.X, "C")
# Z
if bit0==1:
    q.apply_gate(Gates.Z, "C")


# Show final state
print("---Final state of qubits. (Note that qubit 0 should have moved to qubit 2)")
# q2=q.getQubit(2)
q.print_registers()