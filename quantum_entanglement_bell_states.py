from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram


def bell_states():
    circuits = []
    bell_state_names = []
    for i in range(4):
        qc = QuantumCircuit(2,2)

        qc.h(0)  # apply Hadamard gate to the first qubit
        qc.cx(0,1)  # apply CNOT gate with the first qubit as control and second qubit as target

        if i == 0:
           name = '|Φ+⟩' 
        elif i == 1:
            name = '|Φ-⟩'
            qc.z(1)
        elif i == 2:
            name = '|Ψ+⟩'
            qc.x(1)
        elif i == 3:
            name = '|Ψ-⟩'
            qc.x(1)
            qc.z(1)
    
        circuits.append(qc)
        bell_state_names.append(name)

        print(f"Circuit for {name}:")
        print(qc)

    return circuits, bell_state_names


def measure_qubits(circuits, names):
    backend = Aer.get_backend('qasm_simulator')

    for i, qc in enumerate(circuits):
        qc.measure([0, 1], [0, 1])

        transpiled_circuit = transpile(qc, backend)
        job = backend.run(transpiled_circuit, shots=1024, memory=True)
        results = job.result()

        counts = results.get_counts(transpiled_circuit)
        plot_histogram(counts)
        plt.title(f"Measurement Results for {names[i]}")
        plt.show()

        
circuits, names = bell_states()
measure_qubits(circuits, names)