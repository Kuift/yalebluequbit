import bluequbit
from qiskit import QuantumCircuit
from collections import Counter  # en haut du fichier

API_KEY = "4kDE91xNSXezFZQyZc0w7w1C4owXRl1f"
QASM_FILENAME = "P4_golden_mountain.qasm"
DEVICE = 'quantum'
SHOTS = 1000


### MEASURE ON X
print(f"Chargement du circuit depuis le fichier : {QASM_FILENAME}")
qc_qiskit = QuantumCircuit.from_qasm_file(QASM_FILENAME)

# Appliquer Hadamard sur tous les qubits avant mesure (pour mesurer en base X)
for qubit in range(qc_qiskit.num_qubits):
    qc_qiskit.h(qubit)

qc_qiskit.measure_all()

print(qc_qiskit.draw(output='text'))

# Initialisation et exécution
bq = bluequbit.init(API_KEY)
print(f"Exécution du circuit sur le backend '{DEVICE}' avec {SHOTS} shots...")
result = bq.run(qc_qiskit, device=DEVICE, shots=SHOTS)

# Résultats
print("\nRésultats (Comptes) :")
counts = result.get_counts()
print(sorted(counts.items(), key=lambda item: item[1], reverse=True))

