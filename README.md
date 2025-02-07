# Lab-1 Análisis estadístico de la señal UMNG
## INTRODUCCIÓN:
Para el desarrollo de este informe de laboratorio, se realizó un análisis estadistico de señanes biomédicas extraidas de la Pagina Physionet
y seleccionamos una señal EMG; esta herramienta es fundamental ya que por medio de ella se extrae informacion relevante con datos para permitir llegar al desarrollo de esta practica.
Para la programación, se utilizo la herramienta python que permite implementar algoritmos para calcular y analizar los datos proporcionados por la señal, graficarlos, contaminar la señal, y otras opciones más que se observarán en éste informe.

## Paso a paso:
- Seleccionar la señal EMG por medio de Physionet [link Physionet](https://physionet.org/)
- Guardar los archivos .hea, .data en una misma carpeta junto con la señal
- Abrir Python, nombrar el archivo y guardarlo en la misma carpeta donde se encuentran los archivos .hea y .data
- Abrir de nuevo python y iniciar con la programación que explicaremos a continuación:
  
## Programación y Datos estadísticos:
Inicialmente agregamos las librerias:
```  import wfdb
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm.
```


- **wfdb** Es una libreria que permite trabajar con bases de datos, en este caso señales fisiologicas de PrysiNet.
Es ta libreria permite leer, escribir y analizar señales fisiologicas
- **Numpy** Esta librería es fundamental para en la programación poder utilizar sintaxis numericas en python, permitiendo arreglos multidimencionalesy operaciones matematicas
- **Matplotlib.pyplot(plt)** Se usa para graficar los datos
- **Scipy.stats.norm** Se usa para trabajar con distribuciones normales y ajustar curvas.

Éstas librerias son fundamentales porque sin ellas tendriamos muchos errores al momento de usar operciones matematicas y correr el codigo.  

#### Cargar la señal EMG desde el archivo
```
record = wfdb.rdrecord('emg_neuropathy')
señal = record.p_signal[:, 0] * 0.5  
fs = record.fs * 0.5  
time = np.arange(len(señal)) / fs  

```

- **record:** Esta funcion especifica la ruta del archivo que contiene la señal EMG de la libreria wfdb lo que permite leer el archivo con los datos llamada 'emg_neuropathy.

- **señal:** Se utiliza esta función matriz donde cada columna representa un canal de la señal registrada. la expresion [:,0] extrae la primera columna, los valores iniciales y se multiplica por 0.5 reduciendo la amplitud a la mitad.

- **fs:** Es un diccionario que contiene metadatos asociados con la señal, como la frecuencia de muestreo ( fs), nombres de los canales, unidades, entre otros.

#### Ajuste intervalo 
```
tiempo_limite = 8  # en segundos
indice_limite = int(tiempo_limite * fs)
señal = señal[:indice_limite]
time = time[:indice_limite]
```
- **tiempo_limite:** esta funcion permite tomar in intervalo de n segundos para establecer la duracion maxima de la señal que se tomará
- **indice_limite:** la funcion fs representa la frecuencia de muestreo en hz (muestras por segundo multiplicando el tiempo limite por fs y obteniendo la cantidad total de muestras.
  
#### Graficar la señal original

```
plt.figure(figsize=(12, 6))
plt.plot(time, señal, label="Señal EMG Neuropathy", color='blue')
plt.title("Señal EMG Neuropathy")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (mV)")
plt.grid()
plt.legend()
plt.show()

```
- **plt.figure( figsize=(12,6))** Se crea una figura grande para visualizar la señal claramente.
- **plt.plot(time, señal)**: Se grafica la señal en función del tiempo.
- **plt.grid()**: Se agrega una cuadrícula para mejorar la visualización.
- **plt.legend()**: Se muestra la etiqueta de la señal.

![image](https://github.com/user-attachments/assets/b59057c3-f08b-4302-abfe-4eb2bea0070d)

#### Cálculo: 
```
suma = 0
for x in señal:
    suma += x
media = suma / len(señal)
```
Aquí se calcula manualmente la media (promedio) de la señal.

#### Cálculo de desviación estándar 
```
suma = 0
for x in señal:
    suma += (x - media) ** 2
desviacion = (suma / len(señal))
```
Se calcula manualmente la desviación estándar

#### Cálculo del coeficiente de variación
```
coef = (desviacion / media) * 100
```
Se calcula el coeficiente de variación , que mide la dispersión en porcentaje.

#### Usando funciones predefinidas
```
media = np.mean(señal)
desviacion = np.std(señal)
coef = (desviacion / media) * 100

```
Aquí se usan las funciones de numpypara hacer lo mismo de forma más eficiente.

#### Mostrar resultados
```
print("\nMDC")
print("Calculos:")
print(f"Media: {media:.4f}")
print(f"Desviación estándar: {desviacion:.4f}")
print(f"Coeficiente de variación: {coef:.2f} %")

print("\nCalculos con funciones:")
print(f"Media: {media:.4f}")
print(f"Desviación estándar: {desviacion:.4f}")
print(f"Coeficiente de variación: {coef:.2f} %")

```
Se imprimen, organiza y presenta cálculos de forma legible, permitiendo verificar que los métodos utilizados para calcular la media, la desviación estándar y el coeficiente de variación sean correctos.

![image](https://github.com/user-attachments/assets/74fc8a78-739d-4d6d-b40d-872377b125fe)

#### Histograma con PDF ajustada
```

plt.figure(figsize=(12, 6))
plt.hist(señal, bins=50, density=True, alpha=0.75, color='blue', label="Histograma")
```

Un histograma muestra la distribución de los valores de la señal. En este caso, se usa para visualizar cómo están distribuidos los valores de la señal EMG y compararlos con una curva de distribución normal.

#### Ajuste de una distribución normal (PDF)
```
mu, sigma = norm.fit(señal)
pdf_x = np.linspace(min(señal), max(señal), 1000)
pdf_y = norm.pdf(pdf_x, mu, sigma)
factor_escala = 8.2 / max(pdf_y)
pdf_y *= factor_escala
plt.plot(pdf_x, pdf_y, 'k-', label=f"Curva G")

plt.title("Histograma de la Señal EMG")
plt.xlabel("Amplitud")
plt.ylabel("Frecuencia Normalizada")
plt.legend()
plt.grid()
plt.show()

```
Se ajusta una distribución normal a los datos de una señal EMG y la grafica sobre un histograma. Primero, estima la media y la desviación estándar de la señal, luego genera y escala una curva normal, y finalmente la grafica junto con las barras del histograma para analizar cómo se distribuyen los valores de la señal.

![image](https://github.com/user-attachments/assets/11efb074-a446-4bcc-b2af-f467562bbe2b)

#### Función de probabilidad acumulativa (CDF)
```
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

```

Este código calcula y grafica la Función de Probabilidad Acumulativa (CDF) de una señal. Primero, ordena los datos con np.sort(señal), luego calcula la CDF dividiendo los índices acumulados por la cantidad total de datos, asegurando valores entre 0 y 1.

Se configura la figura con plt.figure(figsize=(10,6)) y se grafica la CDF con plt.plot(sorted_data, cdf, label="CDF (Empírica)"), donde el eje X representa la amplitud de la señal y el Y la probabilidad acumulada. Finalmente, se agregan título, etiquetas, cuadrícula y leyenda para mejorar la visualización, mostrando cómo se distribuyen los valores de la señal.

![image](https://github.com/user-attachments/assets/0f148b52-933c-40be-af79-2c92538e3457)
### Función para calcular SNR

```
def calcular_snr(señal , ruido):
    potencia_senal = np.mean(señal ** 2)
    potencia_ruido = np.mean(ruido ** 2)
    snr = 10 * np.log10(potencia_senal / potencia_ruido)
    return snr

  ```
La Relación Señal-Ruido (SNR) se define como la razón entre la potencia de la señal y la potencia del ruido, expresada en decibeles (dB).

Calcula la potencia media de la señal (potencia_senal).
Calcula la potencia media del ruido (potencia_ruido).
Calcula el SNR en decibeles (dB) con la fórmula


#### Función para agregar ruido 

```
def agregar_ruido(señal, tipo="gaussiano", intensidad=0.05, frecuencia=50, porcentaje=0.05, time=None):
    if tipo == "gaussiano":
        ruido = np.random.normal(0, intensidad, len(señal))
    elif tipo == "impulso":
        ruido = np.zeros(len(señal))
        num_impulsos = int(porcentaje * len(señal))
        indices = np.random.randint(0, len(señal), num_impulsos)
        ruido[indices] = np.random.choice([-1, 1], size=num_impulsos) * np.max(señal) * 0.5
    elif tipo == "artefacto" and time is not None:
        ruido = intensidad * np.sin(2 * np.pi * frecuencia * time)
    else:
        raise ValueError("Tipo de ruido no válido")
    return señal + ruido, calcular_snr(señal, ruido)

  ```

Esta función agrega ruido a una señal y calcula su relación señal-ruido (SNR). Dependiendo del tipo de ruido seleccionado, puede ser: gaussiano, generado con una distribución normal; impulsivo, donde se insertan valores aleatorios en ciertos puntos; o artefacto, una señal sinusoidal de una frecuencia específica. Si el tipo no es válido, se genera un error. Finalmente, la señal modificada y su SNR se retornan, permitiendo evaluar el impacto del ruido en la señal original.

#### Contaminación de la señal
```
senal_gaussiana, snr_gaussiano = agregar_ruido(señal, tipo="gaussiano")
senal_impulso, snr_impulso = agregar_ruido(señal, tipo="impulso")
senal_artefacto, snr_artefacto = agregar_ruido(señal, tipo="artefacto", time=time)

```
#### Mostrar valores de SNR
```
print("\nRelación Señal-Ruido (SNR)")
for tipo, snr in zip("Gaussiano", "Impulso", "Artefacto"], [snr_gaussiano, snr_impulso, snr_artefacto):
    print(f"SNR con ruido {tipo.lower()}: {snr:.2f} dB")
```
#### Graficar señales con ruido en gráficos separados junto con la señal original
```
ruidos = ("Ruido Gaussiano", senal_gaussiana, snr_gaussiano, "red"),
          ("Ruido Impulso", senal_impulso, snr_impulso, "green"),
          ("Ruido Artefacto", senal_artefacto, snr_artefacto, "yellow")
```

Aquí se introduce tres tipos de ruido en una señal original (gaussiano, impulsivo y artefacto) mediante la función agregar_ruido(), obteniendo tanto la señal contaminada como su relación señal-ruido (SNR) en cada caso.

Luego, imprime los valores de SNR en decibeles (dB), permitiendo comparar cuánto afecta cada tipo de ruido a la señal. Finalmente, organiza las señales modificadas en una lista con su nombre, SNR y color asignado, lo que facilita su posterior graficación para visualizar el impacto de cada ruido en la señal original.

![image](https://github.com/user-attachments/assets/141a0453-bad7-4a31-9629-31f9203d184c)

![image](https://github.com/user-attachments/assets/62237beb-cb76-4680-9044-671831e41df1)


![image](https://github.com/user-attachments/assets/020917bd-979a-45c3-ae90-cfad52509a4c)

## Análisis de resultados.

Se procesó una señal EMG de una neuropatía, obteniendo sus estadísticos descriptivos como la media, desviación estándar y coeficiente de variación, los cuales permitieron describir su comportamiento. El histograma reveló que la señal sigue una distribución normal, mientras que la función de probabilidad mostró cómo se distribuyen los valores de la señal y permitió analizar la probabilidad de encontrar valores en rangos específicos.
Posteriormente, se añadió ruido gaussiano, de impulso y tipo artefacto, evaluando su alteración mediante el cálculo del SNR.

## Conclusión. 
El análisis estadístico permitió caracterizar la señal EMG, evidenciando su variabilidad y comportamiento mediante la media, desviación estándar y coeficiente de variación. La distribución aproximadamente normal.
La introducción de distintos tipos de ruido permitió evaluar su impacto en la calidad de la señal. Esto destaca la importancia del cálculo del SNR como herramienta para medir la degradación de la señal y la necesidad de aplicar filtros adecuados según el tipo de ruido presente

## Referencias:
[Nombre de la referencia](https://ejemplo.com)

