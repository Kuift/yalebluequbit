from qiskit import QuantumCircuit

QASM_FILENAME = "P3__sharp_peak.qasm"

qc_qiskit = QuantumCircuit.from_qasm_file(QASM_FILENAME)
qc_qiskit.measure_all()

# Sauvegarde du circuit en image
qc_qiskit.draw(output='mpl').savefig("mon_circuit.png")


print(f"Chargement du circuit depuis le fichier : {QASM_FILENAME}")
qc_qiskit = QuantumCircuit.from_qasm_file(QASM_FILENAME)
qc_qiskit.measure_all()
circuit_info = {'n_qubits': qc_qiskit.num_qubits, 'depth': qc_qiskit.depth(), 'gates': dict(Counter(instr.name for instr, _, _ in qc_qiskit.data))}
print("Infos du circuit :", circuit_info)
