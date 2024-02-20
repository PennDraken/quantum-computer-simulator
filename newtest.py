import numpy as np
import qusim_class
import Gates
import random

def test_gateApply():
    vector1 = np.array([1,0,0,0])
    vector1 = Gates.CNOT.dot(vector1)
    q=qusim_class.System()
    q.add_qubit("A", [1,0])
    q.add_qubit("B", [1,0])
    q.apply_gate_multiple(Gates.CNOT, "A", "B")
    vector2 = q.as_register().vector
    assert np.allclose(vector1, vector2), f"Gate application not succesfull."

    vector1 = np.array([0,0,1,0])
    vector1 = Gates.CNOT.dot(vector1)
    q=qusim_class.System()
    q.add_qubit("A", [0,1])
    q.add_qubit("B", [1,0])
    q.apply_gate_multiple(Gates.CNOT, "A", "B")
    vector2 = q.as_register().vector
    assert np.allclose(vector1, vector2), f"Gate application not succesfull."

    q = qusim_class.System()
    q.add_qubit("A", np.array([1,0]))
    q.add_qubit("B", np.array([1,0]))
    q.apply_gate(Gates.H, "A")
    q.apply_gate_multiple(Gates.CNOT, "A", "B")
    assert np.allclose(q.as_register().vector, 1/np.sqrt(2)*np.array([1,0,0,1])), f"Gate application not succesfull."

    q0 = 1/np.sqrt(2)*np.array([1,1])
    q1 = np.array([0,1])
    q2 = np.array([0,1])

    # New case
    vector1 = kron_list([q0,q1,q2])
    vector1 = vector1.dot(np.kron(Gates.CNOT, Gates.I))
    q=qusim_class.System()
    q.add_qubit("A", q0)
    q.add_qubit("B", q1)
    q.add_qubit("C", q2)

    q.apply_gate_multiple(Gates.CNOT, "A", "B")
    vector2 = q.as_register().vector
    assert np.allclose(vector1, vector2), f"Gate application not succesfull."

    # New case
    vector1 = kron_list([q0,q1,q2])
    vector1 = vector1.dot(np.kron(Gates.I, Gates.CNOT))
    q=qusim_class.System()
    q.add_qubit("A", q0)
    q.add_qubit("B", q1)
    q.add_qubit("C", q2)

    q.apply_gate_multiple(Gates.CNOT, "B", "C")
    vector2 = q.as_register().vector
    assert np.allclose(vector1, vector2), f"Gate application not succesfull."

    # Non adjacent qubits
    vector1 = kron_list([q0,q1,q2])
    vector1 = vector1.dot(np.kron(Gates.I, Gates.SWAP)) # Swap q2 q1
    vector1 = vector1.dot(np.kron(Gates.CNOT, Gates.I)) # Apply CNOT
    vector1 = vector1.dot(np.kron(Gates.I, Gates.SWAP)) # Swap back

    q=qusim_class.System()
    q.add_qubit("A", q0)
    q.add_qubit("B", q1)
    q.add_qubit("C", q2)
    q.register_combined()
    q.apply_gate_multiple(Gates.CNOT, "A", "C")
    vector2 = q.as_register().vector
    assert np.allclose(vector1, vector2), f"Gate application not succesfull."

# Apply kron to a whole list
def kron_list(list):
    vector = list[0]
    for i in range(1,len(list)):
        vector = np.kron(vector, list[i])
    return vector

test_gateApply()
print("All tests passed!")