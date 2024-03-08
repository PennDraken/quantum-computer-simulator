# IMPORTS
import numpy as np
import Gates
import qusim_class
# Create circuit
circuit = qusim_class.Circuit([["A","B"],"H 0","CNOT 0 1","CNOT 1 0","CNOT 0 1","CNOT 1 0","CNOT 0 1"])
circuit.show_output=True
circuit.step_fwd()
circuit.step_fwd()
circuit.step_fwd()
circuit.step_fwd()
circuit.step_fwd()

#q0=Gates.zero_state
#q0=Gates.H.dot(q0)
#q1=Gates.zero_state
##q01=np.kron(q0,q1)
#q01=Gates.CNOT.dot(q01)
#print(q01)
