import numpy as np
import qusim_class
import Gates
import random


# Boolean functions to verify our quantum simulators properties seem to be correct
# --------------------------------------------------------------------------------
# Checks if our state is normalised
def check_normalized(qubit_state: np.ndarray)->bool:
    return np.isclose(np.sum(np.abs(qubit_state)**2),1,rtol=1e-05)

# Normalizes state so abs square == 1
def normalize(state):
    scaler = np.sqrt(np.sum(np.abs(state)**2))
    return state/scaler

# Checks wether two qubits given by their indices are entangled
def state_entangled(state_vector, qubit_index_a, qubit_index_b)->bool:
    # If two qubits are entangled, collapsing one qubits state will collapse the other qubits state
    # We just need to measure one of the qubits and then check if the other qubit collapsed
    q = qusim_class.Quantum(2) # Create a new quantum simulator
    q.setState(state_vector) # Set its state to state_vector
    # Check if qubit b is collapsed already
    qubitb_before_measure = q.getQubit(qubit_index_b)
    if np.allclose(qubitb_before_measure, np.array([1,0], dtype=complex)) or np.allclose(qubitb_before_measure, np.array([0,1], dtype=complex)):
        return False
    q.measure(qubit_index_a) # Measure the other qubit a
    # Check if qubit b has collapsed now (only reachable if it wasnt collapsed before)
    qubitb_after_measure = q.getQubit(qubit_index_b)
    return np.allclose(qubitb_after_measure, np.array([1,0], dtype=complex)) or np.allclose(qubitb_after_measure, np.array([0,1], dtype=complex))

# Algorithms
# Creates a bell state with qusim. Returns ndarray
def create_bell_state()->np.array:
    q = qusim_class.Quantum(2)
    # qubits
    qubit1_state = np.array([1,0], dtype=complex)
    qubit2_state = np.array([1,0], dtype=complex)
    # creating the bell state
    qubit1_state = Gates.H.dot(qubit1_state)
    two_qubit_state = np.kron(qubit1_state, qubit2_state) # np.kron() is the tensor product
    bell_state = Gates.CNOT.dot(two_qubit_state)
    return bell_state

# Runs measure on a state vector iteration amount of times
# Returns percentage (as fraction) of the outcome 1
def iterate_measure(state_vector, qubit_index, iterations):
    outcome_0 = 0
    outcome_1 = 0
    for i in range(0, iterations):
        q=qusim_class.Quantum(2)
        q.setState(state_vector)
        bit = q.measure(qubit_index)
        if bit==0:
            outcome_0+=1
        elif bit==1:
            outcome_1+=1
    return outcome_1/iterations

# -----------------------------------------------------------------------------------------------------------------------------------------------------

def test_entanglement():
    state_vector = 1/np.sqrt(2)*np.array([1,0,0,1],dtype=complex)
    print(state_entangled(state_vector, 0, 1)) # This should return true
    state_vector = 1/np.sqrt(2)*np.array([1,0,1,0],dtype=complex)
    print(state_entangled(state_vector, 0, 1)) # This should return true
    state_vector = np.array([1,0,0,0],dtype=complex)
    print(state_entangled(state_vector, 0, 1)) # This should return false
    state_vector = 1/2*np.array([1,1,1,1],dtype=complex)
    print(state_entangled(state_vector, 0, 1)) # This should return false

def test_measure():
    bell_state = 1/np.sqrt(2)*np.array([1,0,0,1],dtype=complex)
    bell_state_measurement = iterate_measure(bell_state,0,iterations=1_000)
    assert np.isclose(bell_state_measurement, 0.5, atol=0.1), f"Measurement not successful: {bell_state_measurement}"

    bell_state = 1/np.sqrt(2)*np.array([1,0,0,1],dtype=complex)
    bell_state_measurement = iterate_measure(bell_state,1,iterations=1_000)
    assert np.isclose(bell_state_measurement, 0.5, atol=0.1), f"Measurement not successful: {bell_state_measurement}"

    state = np.array([1,0,0,0],dtype=complex)
    state_measurement = iterate_measure(state,0,iterations=100)
    assert np.isclose(state_measurement, 0, atol=0.01), f"Measurement not successful: {state_measurement}"
    state_measurement = iterate_measure(state,1,iterations=100)
    assert np.isclose(state_measurement, 0, atol=0.01), f"Measurement not successful: {state_measurement}"

    state = np.array([0,0,0,1,0,0,0,0],dtype=complex) # 1*|011>
    state_measurement = iterate_measure(state,0,iterations=100)
    assert np.isclose(state_measurement, 0, atol=0.01), f"Measurement not successful: {state_measurement}"
    state_measurement = iterate_measure(state,1,iterations=100)
    assert np.isclose(state_measurement, 1, atol=0.01), f"Measurement not successful: {state_measurement}"
    state_measurement = iterate_measure(state,2,iterations=100)
    assert np.isclose(state_measurement, 1, atol=0.01), f"Measurement not successful: {state_measurement}"

def test_getQubit():
    # 2 qubits
    q0=np.array([1,0], dtype=complex)
    q1=np.array([1,0], dtype=complex)
    state=np.kron(q0,q1)
    q=qusim_class.Quantum(2)
    q.setState(state)
    q0b=q.getQubit(0)
    q1b=q.getQubit(1)
    assert np.allclose(q0,q0b) and np.allclose(q1,q1b), f"getQubit() failed. | Input {q0,q1} Output {q0b,q1b}"

    q0=np.array([0,1], dtype=complex)
    q1=np.array([1,0], dtype=complex)
    state=np.kron(q0,q1)
    q=qusim_class.Quantum(2)
    q.setState(state)
    q0b=q.getQubit(0)
    q1b=q.getQubit(1)
    assert np.allclose(q0,q0b) and np.allclose(q1,q1b), f"getQubit() failed. | Input {q0,q1} Output {q0b,q1b}"
    
    q0=1/np.sqrt(2)*np.array([1,1], dtype=complex)
    q1=np.array([0,1], dtype=complex)
    state=np.kron(q0,q1)
    q=qusim_class.Quantum(2)
    q.setState(state)
    q0b=q.getQubit(0)
    q1b=q.getQubit(1)
    assert np.allclose(q0,q0b) and np.allclose(q1,q1b), f"getQubit() failed.\n Input {q0,q1}\n Output {q0b,q1b}"

    # 3 qubits
    q0=np.array([0,1], dtype=complex)
    q1=np.array([1,0], dtype=complex)
    q2=np.array([1,0], dtype=complex)
    state=np.kron(q0,q1)
    state=np.kron(state,q2)
    q=qusim_class.Quantum(2)
    q.setState(state)
    q0b=q.getQubit(0)
    q1b=q.getQubit(1)
    q2b=q.getQubit(2)
    assert np.allclose(q0,q0b) and np.allclose(q1,q1b) and np.allclose(q2,q2b), f"getQubit() on 3 qubits failed. | Input {q0,q1,q2} Output {q0b,q1b,q2b}"

    q0=np.array([0,-1j], dtype=complex)
    q1=np.array([1,0], dtype=complex)
    q2=np.array([0,1], dtype=complex)
    state=np.kron(q0,q1)
    state=np.kron(state,q2)
    q=qusim_class.Quantum(2)
    q.setState(state)
    q0b=q.getQubit(0)
    q1b=q.getQubit(1)
    q2b=q.getQubit(2)
    assert np.allclose(q0,q0b) and np.allclose(q1,q1b) and np.allclose(q2,q2b), f"getQubit() on 3 qubits failed. | Input {q0,q1,q2} Output {q0b,q1b,q2b}"

    q0=np.array([0,1], dtype=complex)
    q1=np.array([0,1], dtype=complex)
    q2=np.array([0,1], dtype=complex)
    state=np.kron(q0,q1)
    state=np.kron(state,q2)
    q=qusim_class.Quantum(2)
    q.setState(state)
    q0b=q.getQubit(0)
    q1b=q.getQubit(1)
    q2b=q.getQubit(2)
    assert np.allclose(q0,q0b) and np.allclose(q1,q1b) and np.allclose(q2,q2b), f"getQubit() on 3 qubits failed. | Input {q0,q1,q2} Output {q0b,q1b,q2b}"

# Generates a random qubit list
def random_qubit_list(qubit_count):
    qubit_list=[]
    for i in range(0,qubit_count):
        real_part = random.uniform(0,1)
        imag_part = random.uniform(0,1)
        alpha = real_part + 1j * imag_part
        real_part = random.uniform(0,1)
        imag_part = random.uniform(0,1)
        beta = real_part + 1j * imag_part
        state=np.array([alpha,beta])
        qubit_list.append(normalize(state))
    assert len(qubit_list)==qubit_count, f"Random qubit list failed. Expected {qubit_count} Got {len(qubit_list)}"
    return qubit_list

def random_state_vector(qubit_count):
    real_part = np.random.normal(size=qubit_count**2)
    imag_part = np.random.normal(size=qubit_count**2)
    complex_array = real_part + 1j * imag_part
    # Normalize to make the sum of absolute values squared equal to 1
    norm = np.sqrt(np.sum(np.abs(complex_array) ** 2))
    normalized_array = complex_array / norm
    print(normalized_array)
    assert check_normalized(normalized_array), f"Not normalized."
    return normalized_array

# Tests taking a state vector, taking out the individual qubits and then reconstructing the state with the qubits
def test_decomposition():
    # Simple test 1
    q=qusim_class.Quantum(2)
    q0=np.array([1,0],dtype=complex)
    q1=1/np.sqrt(2)*np.array([1,1],dtype=complex)
    state1 = np.kron(q0,q1)
    q.setState(state1)
    qubit_list = q.getQubitList()
    assert np.allclose(q0, qubit_list[0]), f"Qubits extraction failed"
    assert np.allclose(q1, qubit_list[1]), f"Qubits extraction failed"
    state2 = q.setQubitList(qubit_list)
    assert np.allclose(state1, state2), f"De/recomposition failed. State 1:\n {state1}\n State 2:\n {state2}"

    # Simple test 2
    q=qusim_class.Quantum(2)
    q0=np.array([0,1j],dtype=complex)
    q1=1/np.sqrt(2)*np.array([1,1],dtype=complex)
    qubit_list1=[q0,q1]
    state1 = np.kron(q0,q1)
    state2 = q.setQubitList(qubit_list1)
    assert np.allclose(state1, state2)
    qubit_list = q.getQubitList()
    assert np.allclose(q0, qubit_list[0]), f"Qubits extraction failed"
    assert np.allclose(q1, qubit_list[1]), f"Qubits extraction failed"
    state2 = q.setQubitList(qubit_list)
    assert np.allclose(state1, state2), f"De/recomposition failed. State 1:\n {state1}\n State 2:\n {state2}"

    # Simple test 2b
    q=qusim_class.Quantum(2)
    q0=np.array([0,1],dtype=complex)
    q1=1/np.sqrt(2)*np.array([1,1],dtype=complex)
    q2=np.array([0,1j],dtype=complex)
    qubit_list1=[q0,q1,q2]
    state1 = np.kron(np.kron(q0,q1),q2)
    state2 = q.setQubitList(qubit_list1)
    assert np.allclose(state1, state2)
    qubit_list2 = q.getQubitList()
    assert np.allclose(q0, qubit_list2[0]), f"Qubits extraction failed"
    assert np.allclose(q1, qubit_list2[1]), f"Qubits extraction failed"
    assert np.allclose(q2, qubit_list2[1]), f"Qubits extraction failed"
    state2 = q.setQubitList(qubit_list2)
    assert np.allclose(state1, state2), f"De/recomposition failed. State 1:\n {state1}\n State 2:\n {state2}"

    # Simple test 3
    q=qusim_class.Quantum(2)
    qubit_list1=random_qubit_list(2)
    assert qubit_list1[0].shape==(2,), f"Wrong shape from random_qubit_list {qubit_list1[0].shape}"
    assert qubit_list1[1].shape==(2,), f"Wrong shape from random_qubit_list {qubit_list1[1].shape}"
    q.setQubitList(qubit_list1) # This fails
    qubit_list2 = q.getQubitList()
    assert np.allclose(qubit_list1, qubit_list2), f"Qubit extraction failed.\n{qubit_list1}\nList 2\n{qubit_list2}"

    q=qusim_class.Quantum(3)
    qubit_list1=random_qubit_list(3)
    q.setQubitList(qubit_list1)
    qubit_list2 = q.getQubitList()
    assert np.allclose(qubit_list1, qubit_list2), f"Qubit extraction failed."

    # Random tests
    for i in range(2,10):
        q=qusim_class.Quantum(i)
        state1 = random_state_vector(i)
        q.setState(state1)
        qubit_list = q.getQubitList()
        state2 = q.setQubitList(qubit_list)
        assert check_normalized(state1), f"Not normalised"
        assert check_normalized(state2), f"Not normalised"
        assert np.allclose(state1, state2), f"De/recomposition failed. State 1:\n {state1}\n State 2:\n {state2}\nQubit size: {i}"

def test_gateApply():
    state1 = np.array([1,0,0,0], dtype=complex)
    state1 = Gates.CNOT.dot(state1)
    q=qusim_class.Quantum(2)
    q.applyGateQubits(Gates.CNOT, [0,1])
    state2 = q.state_vector
    assert np.allclose(state1, state2), f"Gate application not succesfull. State 1:\n {state1}\n State 2:\n {state2}"

    # CNOT on qubits 1 and 2 in three qubit system
    # https://quantumcomputing.stackexchange.com/questions/34167/how-to-apply-cnot-on-a-three-qubit-system-with-two-qubits-already-entangled
    state_start = 1/np.sqrt(2)*np.array([1,0,0,0,0,0,1,0], dtype=complex)
    CNOT_expanded = np.kron(Gates.I, Gates.CNOT)
    state1 = CNOT_expanded.dot(state_start)
    q=qusim_class.Quantum(2)
    q.setState(state_start)
    q.applyGateQubits(Gates.CNOT, [1,2])
    state2 = q.state_vector
    assert np.allclose(state1, state2), f"Gate application not succesfull. \nState 1:\n {state1}\nState 2:\n {state2}"

    # Reverse check
    # state1 = np.array([1,0,0,0], dtype=complex)
    # state1 = Gates.CNOT.dot(state1)
    # q=qusim_class.Quantum(2)
    # q.applyGateQubits(Gates.CNOT, [1,0])
    # state2 = q.state_vector
    # assert np.allclose(state1, state2), f"Gate application not succesfull. State 1:\n {state1}\n State 2:\n {state2}"


    state1 = np.array([1,0,0,0,0,0,0,0], dtype=complex)
    gate = np.kron(Gates.CNOT, Gates.I)
    state1 = gate.dot(state1)
    q=qusim_class.Quantum(3)
    q.applyGateQubits(Gates.CNOT, [0,1])
    state2 = q.state_vector
    assert np.allclose(state1, state2), f"Gate application not succesfull. State 1:\n {state1}\n State 2:\n {state2}"

    state1 = np.array([1,0,0,0,0,0,0,0], dtype=complex)
    gate = np.kron(Gates.I, Gates.CNOT)
    state1 = gate.dot(state1)
    q=qusim_class.Quantum(3)
    q.applyGateQubits(Gates.CNOT, [1,2])
    state2 = q.state_vector
    assert np.allclose(state1, state2), f"Gate application not succesfull. State 1:\n {state1} State 2:\n {state2}"


    # Check if 4x4 matrix can be applied on two qubits not next to eachother
    state1 = np.array([1,0,0,0,0,0,0,0], dtype=complex)
    gate = np.kron(Gates.I, Gates.CNOT)
    state1 = gate.dot(state1)
    q=qusim_class.Quantum(3)
    q.applyGateQubits(Gates.CNOT, {1,2})
    state2 = q.state_vector
    assert np.allclose(state1, state2), f"Gate application not succesfull. State 1:\n {state1} State 2:\n {state2}"


def test_circuits():
    bell_state = 1/np.sqrt(2)*np.array([1,0,0,1],dtype=complex)
    assert np.allclose(create_bell_state(), bell_state), "Bell state not successful"


# -----------------------------------------------------------------------------------------------------------------------------------------------------

print("Starting tests...")

# test_entanglement()
test_measure()
test_circuits()
test_getQubit()
test_decomposition()
test_gateApply()

print("All tests completed!")

# print(apply_gate_to_qubits([1,0,0,0], Gates.CNOT, 0, 1))
