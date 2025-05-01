from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator
import numpy as np
import random
import matplotlib.pyplot as plt

def oracle(qc, secret_string, qr):
    n = len(secret_string)
    for i, bit in enumerate(secret_string):
        if bit == '0':
            qc.x(qr[i])
    qc.h(qr[n-1])
    qc.mcx(qr[:-1], qr[n-1])
    qc.h(qr[n-1])
    for i, bit in enumerate(secret_string):
        if bit == '0':
            qc.x(qr[i])

def diffuser(qc, n, qr):
    qc.h(qr)
    qc.x(qr)
    qc.h(qr[n-1])
    qc.mcx(qr[:-1], qr[n-1])
    qc.h(qr[n-1])
    qc.x(qr)
    qc.h(qr)

def simulacion_grover(n_simulaciones=500):
    n = 4
    max_iter = 10
    simulator = AerSimulator()
    intentos_grover = []

    for _ in range(n_simulaciones):
        ninja_pos = random.randint(0, 15)
        secret_string = format(ninja_pos, '04b')[::-1]

        qr = QuantumRegister(n)
        cr = ClassicalRegister(n)

        encontrado = False
        for i in range(1, max_iter + 1):
            qc = QuantumCircuit(qr, cr)
            qc.h(qr)

            for _ in range(i):
                oracle(qc, secret_string, qr)
                diffuser(qc, n, qr)

            qc.measure(qr, cr)
            compiled = transpile(qc, simulator)
            result = simulator.run(compiled, shots=8192).result()
            counts = result.get_counts()

            most_common = max(counts, key=counts.get)
            most_common_decimal = int(most_common, 2)

            if most_common_decimal == ninja_pos:
                intentos_grover.append(i)
                encontrado = True
                break

        if not encontrado:
            intentos_grover.append(max_iter + 1)  # caso fallido

    # Estadísticas
    promedio = sum(intentos_grover) / len(intentos_grover)
    print(f"📊 Promedio de iteraciones necesarias: {promedio:.2f}")
    print(f"🎯 Mínimo: {min(intentos_grover)}, Máximo: {max(intentos_grover)}")

    # Histograma
    plt.figure(figsize=(8, 5))
    plt.hist(intentos_grover, bins=range(1, max(intentos_grover)+2), align='left',
             rwidth=0.85, color='lightgreen', edgecolor='black')
    plt.xticks(range(1, max(intentos_grover)+2))
    plt.xlabel("Iteraciones necesarias hasta encontrar al ninja")
    plt.ylabel("Frecuencia")
    plt.title(f"Distribución de iteraciones de Grover ({n_simulaciones} simulaciones)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Ejecutar simulación
simulacion_grover(n_simulaciones=50)
