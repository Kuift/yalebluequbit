import bluequbit
from qiskit import QuantumCircuit

API_KEY = "4kDE91xNSXezFZQyZc0w7w1C4owXRl1f"
QASM_FILENAME = "P2_swift_rise.qasm"
DEVICE = 'mps.cpu'
SHOTS = 10000

print(f"Chargement du circuit depuis le fichier : {QASM_FILENAME}")
qc_qiskit = QuantumCircuit.from_qasm_file(QASM_FILENAME)
qc_qiskit.measure_all()

print(qc_qiskit.draw(output='text'))

bq = bluequbit.init(API_KEY)

print(f"Exécution du circuit sur le backend '{DEVICE}' avec {SHOTS} shots...")
result = bq.run(qc_qiskit, device=DEVICE, shots=SHOTS)

print("\nRésultats (Comptes) :")
counts = result.get_counts()
print(sorted(counts.items(), key=lambda item: item[1], reverse=True))