import random
import matplotlib.pyplot as plt

def intento_búsqueda_clásica(ninja_pos):
    for intento in range(16):
        if intento == ninja_pos:
            return intento + 1  # cuenta desde 1

def simulacion_clasica(repeticiones):
    resultados = []

    for _ in range(repeticiones):
        ninja_pos = random.randint(0, 15)
        intentos = intento_búsqueda_clásica(ninja_pos)
        resultados.append(intentos)

    # === Estadísticas básicas ===
    promedio = sum(resultados) / repeticiones
    print(f"📊 Promedio de intentos: {promedio:.2f}")
    print(f"🎯 Mínimo: {min(resultados)}, Máximo: {max(resultados)}")

    # === Graficar histograma ===
    plt.figure(figsize=(8, 5))
    plt.hist(resultados, bins=range(1, 18), align='left', rwidth=0.85, color='skyblue', edgecolor='black')
    plt.xticks(range(1, 17))
    plt.xlabel("Número de intentos hasta encontrar al ninja")
    plt.ylabel("Frecuencia")
    plt.title(f"Distribución de intentos (búsqueda clásica, {repeticiones} juegos)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Ejecutar simulación y graficar
simulacion_clasica(repeticiones=1500)
