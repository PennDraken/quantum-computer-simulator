# Revised version of qusim class
# Supports smaller vector sizes
# ----------------------------------------------------------------------------------------------------
# IMPORTS
import numpy as np
import copy
import re
if __name__ == "__main__":
    import Gates
else:
    from . import Gates # Import in same directory as qusim_class
# ----------------------------------------------------------------------------------------------------
"""q = System()
q.add_qubit("A", Gates.zero_state)
q.add_qubit("B", Gates.one_state)
q.add_qubit("C", Gates.zero_state)
q.add_qubit("D", Gates.zero_state)
q.add_qubit("E", Gates.one_state)
q.add_qubit("F", Gates.zero_state)
q.apply_gate_qubit_list(Gates.CNOT, [3,2,5])"""
