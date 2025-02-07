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
### Cargar la señal EMG desde el archivo
```
record = wfdb.rdrecord('emg_neuropathy')
señal = record.p_signal[:, 0] * 0.5  
fs = record.fs * 0.5  
time = np.arange(len(señal)) / fs  

```

- **record:** Esta funcion especifica la ruta del archivo que contiene la señal EMG de la libreria wfdb lo que permite leer el archivo con los datos llamada 'emg_neuropathy.

- **señal:** Se utiliza esta función matriz donde cada columna representa un canal de la señal registrada. la expresion [:,0] extrae la primera columna, los valores iniciales y se multiplica por 0.5 reduciendo la amplitud a la mitad.

- **fs:** Es un diccionario que contiene metadatos asociados con la señal, como la frecuencia de muestreo ( fs), nombres de los canales, unidades, entre otros.

### Ajuste intervalo 
```
tiempo_limite = 8  # en segundos
indice_limite = int(tiempo_limite * fs)
señal = señal[:indice_limite]
time = time[:indice_limite]
```

### Función para calcular la relación señal-ruido (SNR):

```
def calcular_snr(señal, ruido):
    potencia_senal = np.mean(señal ** 2)  
    potencia_ruido = np.mean(ruido ** 2)  
    snr = 10 * np.log10(potencia_senal / potencia_ruido) 
    return snr
   
```
