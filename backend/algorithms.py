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
def grover(n_qubits, oracle_target, iterations=2):
    # Create qubits
    qubits = []
    for i in range(n_qubits):
        qubits.append(str(i))
    circuit = [qubits]
    # Hadamrds on all qubits
    for i in range(n_qubits):
        circuit.append(f"H {i}")
    for i in range(iterations):
        # Label
        circuit.append(f"label Iteration_{i}")
        # Zor
        circuit.append(f"Zor({n_qubits},{oracle_target}) {qubits}")
        # Ug
        circuit.append(f"Ug({n_qubits}) {qubits}")
    circuit.append(f"label Measurement section")
    for i in range(n_qubits):
        circuit.append(f"measure {i}")
    return circuit

    

def quantum_teleportation():
    return [["A","B","C"],"Ry(np.pi/4) 0","H 1","CNOT 1 2","CNOT 0 1","H 0", "measure 0", "measure 1", "X 1 2", "Z 0 2"]