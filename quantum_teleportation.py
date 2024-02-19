import qusim_class
import Gates
import numpy as np

# This algorithm transports the state of qubit 0 to qubit 2
#----------------------------------------------------------
q = qusim_class.Quantum(3)
q.applyGate(Gates.Ry(np.pi/4), 0) # Set value of qubit to be teleported to |alpha|^2=0.146

# Constructing bell state on qubits 1 and 2
q.applyGate(Gates.H, 1)
q.applyGateQubits(Gates.CNOT, [1,2])

# Show starting state (after Bell state)
print("---Qubits initialized (q1 and q2 are in a bell state)")
q.printQubits()
# q0=q.getQubit(0)
# print(np.abs(q0[0])**2)

# CNOT -> Hadamard
q.applyGateQubits(Gates.CNOT, [0,1])
q.applyGate(Gates.H, 0)

# Measurement
bit0=q.measure(0)
bit1=q.measure(1)

# Error correction
# X
if bit1==1:
    q.applyGate(Gates.X, 2)
# Z
if bit0==1:
    q.applyGate(Gates.Z, 2)

# Show final state
print("---Final state of qubits. (Note that qubit 0 should have moved to qubit 2)")
# q2=q.getQubit(2)
q.printQubits()