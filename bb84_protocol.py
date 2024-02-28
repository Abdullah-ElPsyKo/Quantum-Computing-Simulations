from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np
import matplotlib.pyplot as plt

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def prepare_qubits(n):
    bits = np.random.randint(2, size=n)
    bases = np.random.choice(['+', 'z'], size=n) #  + for diagonal and z for rectilinear
    circuits = []
    for i in range(n):
        qc = QuantumCircuit(1,1)
        if bases[i] == 'z':
            if bits[i] == 1:
                qc.x(0)
        else:
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        circuits.append(qc)
    return circuits, bases, bits


def measure_qubits(circuits):
    backend = Aer.get_backend('qasm_simulator')  # Aer simulator
    measurement_results = []
    bob_bases = []
    for qc in circuits:
        bob_basis =  np.random.choice(['+', 'z'])
        bob_bases.append(bob_basis)
        
        if bob_basis == '+':
            qc.h(0)

        qc.measure(0, 0)

        # Transpile and run the circuit on the simulator backend
        new_circuit = transpile(qc, backend)
        job = backend.run(new_circuit, shots=1, memory=True)
        result = job.result()
        measured_bit = int(result.get_memory()[0])
        measurement_results.append(measured_bit) 

    return measurement_results, bob_bases


def sift_keys(numberQubits, alice_bases, alice_bits, bob_measurement_results, bob_bases):
    # Sift the key based on matching bases
    alice_sifted_key = []
    bob_sifted_key = []
    for i in range(numberQubits):
        if alice_bases[i] == bob_bases[i]:
            alice_sifted_key.append(alice_bits[i])
            bob_sifted_key.append(bob_measurement_results[i])
    return alice_sifted_key, bob_sifted_key


def eavesdrop(circuits):
    print(bcolors.FAIL + "\nEve is eavesdropping and attempting to measure the qubits..." + bcolors.ENDC)
    measure_qubits(circuits)
    

def simulate_bb84(n, eve):
    circuits, alice_bases, alice_bits = prepare_qubits(n)
    if eve:
        eavesdrop(circuits)
    print(bcolors.WARNING + "\nBob is now measuring the qubits in randomly chosen bases...\n" + bcolors.ENDC)
    bob_measurement_results, bob_bases = measure_qubits(circuits)  # Pass Alice's bases for comparison
    print(bcolors.OKCYAN + "\nSifting keys based on matching bases...\n" + bcolors.ENDC)
    alice_key, bob_key = sift_keys(n, alice_bases, alice_bits, bob_measurement_results, bob_bases)

    print(f"\nAlice's key: {alice_key}")
    print(f"Bob's key:   {bob_key}\n")
    error_rate = calculate_error_rate(alice_key, bob_key)
    print(f"Keys are identical: {alice_key == bob_key}\nError rate: {error_rate}%")


def calculate_error_rate(alice_key, bob_key):
    key_size = len(alice_key)
    subset = np.random.randint(key_size, size=15)
    mismatch = 0
    for bit in range(0, key_size):
        if alice_key[bit] != bob_key[bit]:
            mismatch += 1

    error_rate = mismatch / len(subset)
    return error_rate


def main():
    print(bcolors.HEADER + "BB84 Quantum Key Distribution Simulation" + bcolors.ENDC)
    amount_qubits = 50
    while True:
        print("1. Without eavesdropping")
        print("2. With eavesdropping")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            simulate_bb84(amount_qubits, False)
        elif choice == '2':
            simulate_bb84(amount_qubits, True)
        elif choice == '3':
            break
        else:
            print("Invalid input, please try again.")
             
        print("\n" + "Simulation complete. Would you like to run another simulation?" + "\n")
# Execute the main function
if __name__ == '__main__':
    main()