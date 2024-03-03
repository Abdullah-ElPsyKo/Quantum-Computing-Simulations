from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram


def quantum_teleportation():
    qc = QuantumCircuit(3,3)
    
    qc.x(0)  # Apply X gate to the first qubit that will be teleported
    qc.barrier()
    # Quantum entangle 2 qubits
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()
    # Prepare to be teleported qubit with the entangled qubit
    qc.cx(0,1)
    qc.h(0)
    qc.barrier()
    # Measure the first two qubits
    qc.measure([0,1], [0,1])
    qc.barrier()

    # Apply corrections based on the measurement outcomes
    qc.cx(1, 2)
    qc.cz(0, 2)
    qc.barrier()
    # bobs measurement
    qc.measure(2, 2)

    backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(qc, backend)
    job = backend.run(transpiled_circuit, shots=1024, memory=True)
    results = job.result()
    counts = results.get_counts(transpiled_circuit)
    plot_histogram(counts)
    plt.show()


    qc.draw(output='mpl')
    plt.show()

quantum_teleportation()