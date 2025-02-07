import wfdb
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Función para calcular SNR
def calcular_snr(señal, ruido):
    potencia_senal = np.mean(señal ** 2)
    potencia_ruido = np.mean(ruido ** 2)
    snr = 10 * np.log10(potencia_senal / potencia_ruido)
    return snr

# Cargar la señal EMG desde el archivo
record = wfdb.rdrecord('emg_neuropathy')
señal = record.p_signal[:, 0] * 0.5  # Reducir la amplitud de la señal original
fs = record.fs * 0.5  # Reducir la frecuencia de muestreo para alargar la señal
time = np.arange(len(señal)) / fs  # Crear el eje de tiempo

# Limitar a 10 segundos de datos (ajuste de intervalo)
tiempo_limite = 8  # en segundos
indice_limite = int(tiempo_limite * fs)
señal = señal[:indice_limite]
time = time[:indice_limite]

# Graficar la señal original
plt.figure(figsize=(12, 6))
plt.plot(time, señal, label="Señal EMG Neuropathy", color='blue')
plt.title("Señal EMG Neuropathy")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (mV)")
plt.grid()
plt.legend()
plt.show()

# Cálculo manual de la media 
suma = 0
for x in señal:
    suma += x
media = suma / len(señal)

# Cálculo manual de la desviación estándar 
suma = 0
for x in señal:
    suma += (x - media) ** 2
desviacion = (suma / len(señal))

# Cálculo del coeficiente de variación
coef = (desviacion / media) * 100

# Usando funciones predefinidas
media = np.mean(señal)
desviacion = np.std(señal)
coef = (desviacion / media) * 100

# Mostrar resultados
print("\nMDC")
print("Calculos:")
print(f"Media: {media:.4f}")
print(f"Desviación estándar: {desviacion:.4f}")
print(f"Coeficiente de variación: {coef:.2f} %")

print("\nCalculos con funciones:")
print(f"Media: {media:.4f}")
print(f"Desviación estándar: {desviacion:.4f}")
print(f"Coeficiente de variación: {coef:.2f} %")


# Histograma con PDF ajustada
plt.figure(figsize=(12, 6))
plt.hist(señal, bins=50, density=True, alpha=0.75, color='blue', label="Histograma")

# Ajuste de una distribución normal (PDF)
mu, sigma = norm.fit(señal)
pdf_x = np.linspace(min(señal), max(señal), 1000)
pdf_y = norm.pdf(pdf_x, mu, sigma)
factor_escala = 8.2 / max(pdf_y)
pdf_y *= factor_escala
plt.plot(pdf_x, pdf_y, 'k-', label=f"Curva G")

plt.title("Histograma de la Señal EMG")
plt.xlabel("Amplitud")
plt.ylabel("Frecuencia ")
plt.legend()
plt.grid()
plt.show()

# Función de probabilidad acumulativa (CDF)
sorted_data = np.sort(señal)
cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

plt.figure(figsize=(10, 6))
plt.plot(sorted_data, cdf, label="CDF (Empírica)")
plt.title("Función de Probabilidad Acumulativa (CDF)")
plt.xlabel("Amplitud")
plt.ylabel("Probabilidad acumulada")
plt.grid()
plt.legend()
plt.show()

# Función para agregar ruido y calcular SNR
def agregar_ruido(señal, tipo="gaussiano", intensidad=0.05, frecuencia=50, porcentaje=0.02, time=None):
    if tipo == "gaussiano":
        ruido = np.random.normal(0, intensidad, len(señal))
    elif tipo == "impulso":
        ruido = np.zeros(len(señal))
        num_impulsos = int(porcentaje * len(señal))  # Reducimos la cantidad de impulsos
        indices = np.random.randint(0, len(señal), num_impulsos)
        amplitud_ruido = np.max(señal) * 0.2  # Reducimos la amplitud del ruido
        ruido[indices] = amplitud_ruido  # Solo valores positivos
    elif tipo == "artefacto" and time is not None:
        ruido = intensidad * np.sin(2 * np.pi * frecuencia * time)
    else:
        raise ValueError("Tipo de ruido no válido")
    snr = calcular_snr(señal, ruido)
    snr = max(snr, 0)
    return señal + ruido, snr


# Contaminación de la señal
senal_gaussiana, snr_gaussiano = agregar_ruido(señal, tipo="gaussiano")
senal_impulso, snr_impulso = agregar_ruido(señal, tipo="impulso")
senal_artefacto, snr_artefacto = agregar_ruido(señal, tipo="artefacto", time=time)

# Mostrar valores de SNR
print("\nRelación Señal-Ruido (SNR)")
for tipo, snr in zip(["Gaussiano", "Impulso", "Artefacto"], [snr_gaussiano, snr_impulso, snr_artefacto]):
    print(f"SNR con ruido {tipo.lower()}: {snr:.2f} dB")

# Graficar señales con ruido en gráficos separados junto con la señal original
ruidos = [("Ruido Gaussiano", senal_gaussiana, snr_gaussiano, "red"),
          ("Ruido Impulso", senal_impulso, snr_impulso, "green"),
          ("Ruido Artefacto", senal_artefacto, snr_artefacto, "yellow")]

for nombre, senal_ruido, snr, color in ruidos:
    # Graficar la señal original junto con la señal con ruido
    plt.figure(figsize=(12, 6))
    plt.plot(time, señal, label="Señal Original", color="black", alpha=1.0, linewidth=1.5)
    plt.plot(time, senal_ruido, label=f"Señal con {nombre} (SNR={snr:.2f} dB)", color=color, alpha=0.7)
    plt.title(f"Señal EMG con {nombre}")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Voltaje (mV)")
    plt.grid()
    plt.legend()
    plt.show()
