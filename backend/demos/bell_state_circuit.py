import qusim_class

circuit = qusim_class.Circuit([["A","B"],"H 0","CNOT 0 1"]) 
circuit.step_fwd()
circuit.step_fwd()
