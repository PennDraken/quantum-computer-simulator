# Change path (in order to import backend module)
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from backend.circuit import Circuit
import backend.algorithms as algorithms
import time

start_time = time.time()
for i in range(0,100):
    circuit : Circuit = Circuit(algorithms.grover(10, [0b11010], iterations=8))
    circuit.run()
end_time = time.time()
print(f"Time for execution {end_time - start_time}")