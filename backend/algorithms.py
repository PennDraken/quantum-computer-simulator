# ALGORITHMS
#---------------------------------------------------------------------
import numpy as np
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