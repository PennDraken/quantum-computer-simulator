import numpy as np
import qusim_class
def state_normalized(qubit_state: np.ndarray)->bool:
    return np.isclose(np.sum(np.abs(qubit_state)**2),1,rtol=1e-05)

def state_entangeld(qubit_state :np.ndarray)->bool:
    list_one = []
    list_zero= []
    for i in range(0,10001):
        value = qusim_class.q.measure(0)
        if value == 1:
            list_one.append(value)
        else:
            list_zero.append(value)
    return np.isclose(len(list_one),len(list_zero),rtol=1)

def state_entangeld2(qubit_state :np.ndarray)->bool:
    state = qusim_class.q.state_matrix
    length = int((qusim_class.q.qubit_count)**2)
    for i in range(0,length+1):
        qusim_class.q.applyGate(qusim_class.Gates.H, i/length)
    print(state, qusim_class.q.state_matrix)
    return np.allclose(qusim_class.q.state_matrix,state)

state_vector = 1/np.sqrt(2)*np.array([1,0,0,1],dtype=complex)
    print(state_entangled(state_vector, 0, 1)) # This should return true
    state_vector = 1/np.sqrt(2)*np.array([1,0,1,0],dtype=complex)
    print(state_entangled(state_vector, 0, 1)) # This should return true
    state_vector = np.array([1,0,0,0],dtype=complex)
    print(state_entangled(state_vector, 0, 1)) # This should return false
    state_vector = 1/2*np.array([1,1,1,1],dtype=complex)
    print(state_entangled(state_vector, 0, 1)) # This should return false


print(state_normalized(np.array([0+0.j, 0+0.j, 0+0.j, 1+0.j])))
print(state_entangeld2(qusim_class.q.state_matrix))