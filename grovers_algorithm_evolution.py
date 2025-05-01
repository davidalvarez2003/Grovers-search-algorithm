from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
import numpy as np
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# === FUNCIÓN ADICIONAL: graficar solo amplitudes reales ===
def plot_real_amplitudes(statevector, title="Amplitudes reales"):
    n = int(np.log2(len(statevector.data)))
    basis_states = [format(i, f'0{n}b') for i in range(2**n)]
    amplitudes_real = statevector.data.real

    plt.figure(figsize=(10, 4))
    plt.bar(basis_states, amplitudes_real, color='royalblue')
    plt.title(title)
    plt.ylabel("Amplitud real")
    plt.xlabel("Estados base")
    plt.grid(True)
    plt.ylim(-1, 1)
    plt.show()

# === 1. Oráculo generalizado ===
def oracle(qc, secret_string, qr):
    n = len(secret_string)
    qc.barrier(qr)
    for i, bit in enumerate(secret_string):
        if bit == '0':
            qc.x(qr[i])
    qc.h(qr[n - 1])
    qc.mcx(qr[:n - 1], qr[n - 1])
    qc.h(qr[n - 1])
    for i, bit in enumerate(secret_string):
        if bit == '0':
            qc.x(qr[i])
    qc.barrier(qr)

# === 2. Difusor ===
def diffuser(qc, n, qr):
    qc.barrier(qr)
    qc.h(qr)
    qc.x(qr)
    qc.h(qr[n - 1])
    qc.mcx(qr[:-1], qr[n - 1])
    qc.h(qr[n - 1])
    qc.x(qr)
    qc.h(qr)
    qc.barrier(qr)

# === 3. Configuración general ===
user_string = '1000'  # Define aquí el estado objetivo de 4 bits
secret_string = user_string[::-1]  # Inversión por convención Qiskit

n = len(secret_string)
qr = QuantumRegister(n, name='q')
cr = ClassicalRegister(n, name='c')
qc = QuantumCircuit(qr, cr, name='grover')

# Inicialización
qc.h(qr)

# Iteraciones óptimas de Grover
iterations = int(np.floor(np.pi / 4 * np.sqrt(2**n)))
print(f"Número de iteraciones: {iterations}")

# === 4. Evolución del estado ===
state_history = [Statevector(qc)]

for i in range(iterations):
    oracle(qc, secret_string, qr)
    state_history.append(Statevector(qc))
    diffuser(qc, n, qr)
    state_history.append(Statevector(qc))

# === 5. Medición final ===
qc_measure = qc.copy()
qc_measure.measure(qr, cr)

final_result = AerSimulator().run(transpile(qc_measure, AerSimulator()), shots=8192).result()
final_counts = final_result.get_counts(qc_measure)

# Mostrar histograma final
print("\nResultados del conteo final:", final_counts)
plot_histogram(final_counts, title=f"Resultados Finales de Grover (objetivo '{user_string}')")
plt.show()

# === 6. Visualizar evolución: solo amplitudes reales ===
for i, statevector in enumerate(state_history):
    print(f"\nAmplitudes después del paso {i}:")
    plot_real_amplitudes(statevector, title=f"Amplitudes reales después del paso {i}")

# === 7. Probabilidad de éxito en cada paso ===
probability_success_history = []
target_state_index = int(secret_string, 2)

for statevector in state_history:
    prob_amplitude = statevector[target_state_index]
    prob_success = np.abs(prob_amplitude)**2
    probability_success_history.append(prob_success)
    print(f"Probabilidad de éxito (estado |{user_string}>) después del paso {len(probability_success_history)-1}: {prob_success:.4f}")
