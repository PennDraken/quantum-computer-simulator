import qusim_class
import Gates
import numpy as np

# Constructing bell state on qubits 1 and 2
q = qusim_class.Quantum(3)
q.setQubit(0, [0,1]) # Sets qubit to be teleported
q.applyGate(Gates.H, 1)
q.applyGateQubits(Gates.CNOT, [1,2])
print(f"Bell state:\n {q.state_matrix}")
# q.measure(1)
# print(f"Qubit 1:{q.getQubit(1)}")
# print(f"Qubit 2:{q.getQubit(2)}")
print(f"Probability total:\n {q.totalProbability()}")
# Apply rx
q.applyGate(Gates.Rx(np.pi/4), 0)
q.applyGateQubits(Gates.CNOT, [0,1])
q.applyGate(Gates.H, 0)

# Measurement
q.measure(0)
q.measure(1)
bit0=q.getQubit(0)
bit1=q.getQubit(1)
print(f"Probability total:\n {q.totalProbability()}")
# X
if bit1==1:
    q.applyGate(Gates.X, 2)

# Z
if bit0==1:
    q.applyGate(Gates.Z, 2)

print(f"Probability total:\n {q.totalProbability()}")
print(f"Final state matrix:\n {q.state_matrix}")
print(f"Qubit 2:\n {q.getQubit(2)}")
print(f"Probability total:\n {q.totalProbability()}")