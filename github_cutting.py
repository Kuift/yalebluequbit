########## Quantum Circuit Solver - Circuit_2_42q.qasm - by Jamie Kraus 10/25/2024 ##########

# Importing necessary libraries
import bluequbit
from qiskit import QuantumCircuit
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
bq = bluequbit.init()

load_dotenv() 

token = os.getenv("TOKEN")

def run_sub_circuit(qasm_content, start_qubit, num_qubits):
    print(f"\nRunning sub-circuit from qubit {start_qubit} with {num_qubits} qubits.")
    sub_circuit = QuantumCircuit(num_qubits, num_qubits)
    
    original_circuit = QuantumCircuit.from_qasm_str(qasm_content)
    print(f"Original circuit loaded with {original_circuit.num_qubits} qubits.")

    for instr in original_circuit.data:
        operation, qargs, cargs = instr.operation, instr.qubits, instr.clbits
        max_qubit = start_qubit + num_qubits - 1
        q_indices = [original_circuit.qubits.index(q) for q in qargs if start_qubit <= original_circuit.qubits.index(q) <= max_qubit]
        if len(q_indices) == len(qargs):
            q_indices = [i - start_qubit for i in q_indices]
            print(f"Appending operation {operation.name} with qubits {q_indices}.")
            if cargs: 
                c_indices = [original_circuit.clbits.index(c) for c in cargs if original_circuit.clbits.index(c) < num_qubits]
                if len(c_indices) != len(cargs):
                    print(f"Skipping operation {operation.name} due to mismatched classical bits.")
                    continue
                print(f"Appending operation {operation.name} with classical bits {c_indices}.")
                sub_circuit.append(operation, q_indices, c_indices)
            else:
                sub_circuit.append(operation, q_indices)
    print(f"Sub-circuit created with {sub_circuit.num_qubits} qubits and {sub_circuit.num_clbits} classical bits.")
    
    try:
        result = bq.run(sub_circuit, device='mps.cpu', shots=1000)  #
        counts = result.get_counts()
        print(f"Sub-circuit run completed successfully.")
        return counts

    except Exception as e:
        print(f"Failed to run the sub-circuit. Error: {e}")
        return {}

# Loading the circuit from the .qasm file
qasm_file_path = "P3__sharp_peak.qasm"  # For example "C:/Users/Jamie/QuantumCircuitSolver/circuit_2_42q.qasm"
with open(qasm_file_path, 'r') as f:
    qasm_content = f.read()

sub_circuits_results = []
qubits_per_sub_circuit = 44
total_qubits = 44

# Run sub-circuits
for start_qubit in range(0, total_qubits, qubits_per_sub_circuit):
    result = run_sub_circuit(qasm_content, start_qubit, min(qubits_per_sub_circuit, total_qubits - start_qubit))
    sub_circuits_results.append(result)

# Recombine the results
combined_counts = {}
for idx, result in enumerate(sub_circuits_results):
    start_qubit = idx * qubits_per_sub_circuit
    for bitstring, probability in result.items():
        full_bitstring = ['0'] * total_qubits
        for i, bit in enumerate(bitstring):
            full_bitstring[start_qubit + i] = bit
        full_bitstring = ''.join(full_bitstring)
        if full_bitstring in combined_counts:
            combined_counts[full_bitstring] += probability
        else:
            combined_counts[full_bitstring] = probability

df = pd.DataFrame(list(combined_counts.items()), columns=['Bitstring', 'Probability'])

df = df.sort_values(by='Probability', ascending=False)

hidden_bitstring = max(combined_counts, key=combined_counts.get)

N = 20  
top_df = df.head(N)

plt.figure(figsize=(10, 6))
bars = plt.bar(top_df['Bitstring'], top_df['Probability'], color='skyblue')
plt.xticks(rotation=90)  
plt.xlabel('Bitstring')
plt.ylabel('Probability')
plt.title('Top Bitstring Probabilities')

for bar, bitstring in zip(bars, top_df['Bitstring']):
    if bitstring == hidden_bitstring:
        bar.set_color('red')

plt.tight_layout()
plt.show()

print(f"\nThe hidden bitstring is: {hidden_bitstring}")