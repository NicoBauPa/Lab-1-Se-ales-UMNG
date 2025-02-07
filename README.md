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
- **plt.figure( figsize=(50,6))** Se crea una figura grande para visualizar la señal claramente.
- **plt.plot(time, señal)**: Se grafica la señal en función del tiempo.
- **plt.grid()**: Se agrega una cuadrícula para mejorar la visualización.
- **plt.legend()**: Se muestra la etiqueta de la señal.

![image](https://github.com/user-attachments/assets/b59057c3-f08b-4302-abfe-4eb2bea0070d)

#### Cálculo manual de la media 
```
suma = 0
for x in señal:
    suma += x
media = suma / len(señal)
```
Aquí se calcula manualmente la media (promedio) de la señal.

#### Cálculo manual de la desviación estándar 
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
Se imprimen, organiza y presenta cálculos calculados de forma legible, permitiendo verificar que los métodos utilizados para calcular la media, la desviación estándar y el coeficiente de variación sean correctos.

