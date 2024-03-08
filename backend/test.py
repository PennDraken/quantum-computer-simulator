# Revised version of qusim class
# Supports smaller vector sizes
# ----------------------------------------------------------------------------------------------------
# IMPORTS
import numpy as np
import Gates
import qusim_class
# ----------------------------------------------------------------------------------------------------
# TESTS
def test_gateApply():
    target = np.array([1, 0, 0, 0])
    target = Gates.CNOT.dot(target)
    q = qusim_class.System()
    q.add_qubit("A", [1, 0])
    q.add_qubit("B", [1, 0])
    q.apply_gate_multiple(Gates.CNOT, "A", "B")
    result = q.get_as_register().vector
    test(target, result, "Testing gate application")

    target = np.array([0, 0, 1, 0])
    target = Gates.CNOT.dot(target)
    q = qusim_class.System()
    q.add_qubit("A", [0, 1])
    q.add_qubit("B", [1, 0])
    q.apply_gate_multiple(Gates.CNOT, "A", "B")
    result = q.get_as_register().vector
    test(target, result, "Testing gate application")


    q = qusim_class.System()
    q.add_qubit("A", np.array([1, 0]))
    q.add_qubit("B", np.array([1, 0]))
    q.apply_gate(Gates.H, "A")
    q.apply_gate_multiple(Gates.CNOT, "A", "B")
    result=q.get_as_register().vector
    target =1/np.sqrt(2) * np.array([1, 0, 0, 1])
    test(target, result, "Testing gate application")


    # define qubits
    q0 = 1/np.sqrt(2)*np.array([1, 1])
    q1 = np.array([0, 1])
    q2 = np.array([0, 1])

    # New case
    target = kron_list([q0, q1, q2])
    target = target.dot(np.kron(Gates.CNOT, Gates.I))
    q = qusim_class.System()
    q.add_qubit("A", q0)
    q.add_qubit("B", q1)
    q.add_qubit("C", q2)

    q.apply_gate_multiple(Gates.CNOT, "A", "B")
    result = q.get_as_register().vector
    test(target, result, "Testing gate application")

    # New case
    target = kron_list([q0, q1, q2])
    target = target.dot(np.kron(Gates.I, Gates.CNOT))
    q = qusim_class.System()
    q.add_qubit("A", q0)
    q.add_qubit("B", q1)
    q.add_qubit("C", q2)

    q.apply_gate_multiple(Gates.CNOT, "B", "C")
    result = q.get_as_register().vector
    test(target, result, "Testing gate application")

    # Non adjacent qubits
    target = kron_list([q0, q1, q2])
    target = target.dot(np.kron(Gates.I, Gates.SWAP))  # Swap q2 q1
    target = target.dot(np.kron(Gates.CNOT, Gates.I))  # Apply CNOT
    target = target.dot(np.kron(Gates.I, Gates.SWAP))  # Swap back

    q = qusim_class.System()
    q.add_qubit("A", q0)
    q.add_qubit("B", q1)
    q.add_qubit("C", q2)
    q.register_combined()
    q.apply_gate_multiple(Gates.CNOT, "A", "C")
    result = q.get_as_register().vector
    test(target, result, "Testing gate application")

def test_swap():
    register = qusim_class.Register(["A","B"], np.array([0,1,2,3]))
    register2 = qusim_class.swap(register, "A", "B")
    vector=register2.vector
    target = np.array([0,2,1,3])
    test(target, vector, "Testing swap")

    register = qusim_class.Register(["A","B","C"], np.array([0,1,2,3,4,5,6,7]))
    register2 = qusim_class.swap(register, "A", "C")
    target = np.array([0,4,2,6,1,5,3,7])
    vector=register2.vector
    test(target, vector, "Testing swap")

def test_sort():
    # define qubits
    q0 = 1/np.sqrt(2)*np.array([1, 1])
    q1 = np.array([0, 1])
    q2 = np.array([0, 1])
    q3 = 1/np.sqrt(2)*np.array([1, 1])

    # sorted same as unsorted test
    q = qusim_class.System()
    q.add_qubit("A", q0)
    q.add_qubit("B", q1)
    q.add_qubit("C", q2)
    q.add_qubit("D", q3)
    q.register_combined()
    q.apply_gate_multiple(Gates.CNOT, "A", "C")
    result = q.register_combined().vector
    result2 = q.sort_register(q.registers[0], q.qubits).vector
    test(result, result2, "Tested sorting already sorted state")

    # sort unsorted test
    q = qusim_class.System()
    q.add_qubit("A", q0)
    q.add_qubit("B", q1)
    q.add_qubit("C", q2)
    q.add_qubit("D", q3)
    q.apply_gate_multiple(Gates.CNOT, "A", "D")
    q.apply_gate_multiple(Gates.CNOT, "B", "D")
    q.register_combined()
    qubit_result = q.sort_register(q.registers[0], q.qubits).qubits
    test(["A","B","C","D"], qubit_result, "Tested sorting already sorted state")

    # bell state test
    # q = qusim_class.System()
    # q.add_qubit("A", q0)
    # q.add_qubit("B", q1)
    # q.add_qubit("C", q2)

# ----------------------------------------------------------------------------------------------------
# UTIL
# Used for feedback in terminal
def test(target, result, test_text : str):
    assert np.allclose(result, target),test_text+f"\nTest failed! Exptected:\n{target}\nReceived:\n{result}\n"

# Apply kron to a whole list
def kron_list(list):
    vector = list[0]
    for i in range(1, len(list)):
        vector = np.kron(vector, list[i])
    return vector

# ----------------------------------------------------------------------------------------------------
# TESTS TO RUN
print("Starting tests!")
test_swap()
test_gateApply()
test_sort()
print("All tests passed!")
