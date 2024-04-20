# ALGORITHMS
#---------------------------------------------------------------------
import numpy as np
# Returns the instructions for the circuit of the shor subroutine
def shor_subroutine_circuit(guess : int, N : int):
    n = int((np.ceil(np.log2(N))))
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

# Grovers algorithm
# https://i0.wp.com/quantumzeitgeist.com/wp-content/uploads/QZ-Grover-4.png?fit=2427%2C708&ssl=1
def grover_basic():
    return [["q0","q1","q2","q3","ancilla 0","ancilla 1","ancilla 2","ancilla 3","ancilla 4"],"H 0","H 1","H 2","H 3",
            "label Oracle starts here",
            "Toffoli 0 1 4","Toffoli 2 3 5","CNOT 4 5","Toffoli 0 3 6","X 6","Toffoli 5 6 7","CNOT 7 8",
            "Toffoli 5 6 7","X 6","Toffoli 0 3 6","CNOT 4 5","Toffoli 2 3 5","Toffoli 0 1 4",
            "H 0","H 1","H 2","H 3","X 0","X 1","X 2","X 3","I 0","I 1","I 2","H 3",
            "Toffoli 0 1 4","Toffoli 2 3 4","Toffoli 0 1 4","I 0","I 1","I 2","H 3","X 0","X 1","X 2","X 3","H 0","H 1","H 2","H 3",
            "label Rerun Oracle",
            "measure 0","measure 1","measure 2","measure 3"]

# https://www.cs.purdue.edu/homes/white570/media/CS_584_Final_Project.pdf
def grover_2_qubits(key):
    qubits = ["0","1"]
    return [qubits, 
            "H 0", "H 1",
            f"Zor(2,{key}) 0 1",
            f"Ug(2) 0 1",
            "measure 0",
            "measure 1"
            ]

# https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/grovers-algorithm
def grover(n_qubits, states : list[int], iterations=2):
    """
    Implements Grovers algorithm.
    Inputs:
        n_qubits - Number of qubits in algorithm
        states - States to search for. Example input: [0b0110,0b1000]
        iterations - Number of iterations to apply grovers. Note increased iterations leads to amplitude decay of target states.
    """
    # Create qubits
    qubits = []
    for i in range(n_qubits):
        qubits.append(str(i))
    circuit = [qubits]
    # Hadamards on all qubits
    for i in range(n_qubits):
        circuit.append(f"H {i}")
    # Mess up order
    circuit.append("gen_I(2) 3 1")
    circuit.append("gen_I(2) 4 1")
    circuit.append("gen_I(3) 2 1 3")

    # Create Grover operator
    for i in range(iterations):
        # Label
        circuit.append(f"label Iteration_{i}")
        # Grover operator
        circuit.append(f"grover_op({n_qubits},{states}) {qubits_between(0, n_qubits - 1)}")
    circuit.append(f"label Measurement section")
    for i in range(n_qubits):
        circuit.append(f"measure {i}")
    return circuit

def shors(a, N):
     # Create qubits
    qubits = []
    n = int(np.ceil(np.log2(N)))
    for i in range(2*n):
        qubits.append(f"q{i}")
    for i in range(n):
        qubits.append(f"x{i}")
    circuit = [qubits]
    # Hadamards on qubits
    for i in range(2*n):
        circuit.append(f"H {i}")
    for i in range(2*n,3*n):
        circuit.append(f"X {i}")
    circuit.append(f"label Start_operation")
    top_qubits = list(range(2*n))
    bottom_qubits = list(range(2*n,3*n))
    for i in range(0, 2*n):
        control_bit = (2*n-1) - i # Starts at bottom qubit
        qubits = [control_bit] + bottom_qubits
        circuit.append(f"add_control_qubit(gate_Ua({a},{i},{N})) {qubits}")
    circuit.append(f"DFT({2**(2*n)}) {top_qubits}")
    circuit.append(f"label Start_measurement")
    for i in range(2*n):
        circuit.append(f"measure {i}")
    return circuit



def quantum_teleportation():
    return [["A","B","C"],"Ry(np.pi/4) 0","H 1","CNOT 1 2","CNOT 0 1","H 0", "measure 0", "measure 1", "X 1 2", "Z 0 2"]


# ----------------------------------------------------------------------------------------------------------------------
# Helper functions
def qubits_between(start, end):
    """
    Generates a string consisting of all numbers between start and end seperated by spaces
    Used to create algorithms where qubit sizes may vary
    Example: qubits_between(2,5) returns "2 3 4 5"
    """
    if start > end:
        return ""  # Return an empty string if start is greater than end
    else:
        return ' '.join(str(i) for i in range(start, end + 1))