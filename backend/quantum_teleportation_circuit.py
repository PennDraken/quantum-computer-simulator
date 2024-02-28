import qusim_class

# TODO implement measure and bits correction
circuit = qusim_class.Circuit([["A","B","C"],"Ry(np.pi/4) 0","H 1","CNOT 1 2","CNOT 0 1","H 0", "measure 0", "measure 1"])
circuit.step_fwd()
circuit.step_fwd()
circuit.step_fwd()
circuit.step_fwd()
circuit.step_fwd()
circuit.step_fwd()
circuit.step_fwd()