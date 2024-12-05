import numpy as np
import matplotlib.pyplot as plt
import diffraction_library as diff

resolucion = 5000  # Número de puntos en la malla
longitud_Arreglo = 0.1  # Tamaño físico del área (10 mm)
radio = 2E-3  # Radio del círculo en metros
centro = [0,0] # El centro será el origen 
long_Onda = 533E-9 #longitud de onda de la iluminacion
distancia = 5000 #distancia de propagacion

# Crear la malla de puntos
xx, yy = diff.malla_Puntos(resolucion, longitud_Arreglo)

# Crear la máscara circular
mascara = diff.funcion_Rectangulo(1E-3, 1E-3, centro, xx, yy)

#calculamos la fft de la iluminacion inicial
fft_Mascara = np.fft.fftshift(np.fft.fft2(mascara))

''' propagacion '''
numero_Onda = 2*np.pi/long_Onda #calculamos el numero de onda para propagar 
fase_Constante = (np.exp(1j* numero_Onda*distancia)) / (1j * long_Onda * distancia) #calculamos el elemento de fase constante para propagar las ondas en fraunhoffer
patron_Difraccion = fft_Mascara * fase_Constante #calculamos el campo optico en el detector
amplitud_Detector = (np.abs(patron_Difraccion)) ** 2 #calculamos la irradiancia sacando el modulo cuadrado 

'''Visualización de gráficas cortes transversales'''

# Crear una figura con dos subgráficos
fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Crear dos subgráficos lado a lado

# Subgráfico de la máscara de difracción
im_mascara = axes[0].imshow(np.abs(mascara), extent=[-longitud_Arreglo/2, longitud_Arreglo/2, -longitud_Arreglo/2, longitud_Arreglo/2], cmap='gray')
axes[0].set_title("Máscara")
axes[0].set_xlabel("x (m)")
axes[0].set_ylabel("y (m)")
fig.colorbar(im_mascara, ax=axes[0], label="Transmitancia")  # Barra de color para la máscara

# Subgráfico del patrón de difracción
im_difraccion = axes[1].imshow(amplitud_Detector, extent=[-longitud_Arreglo/2, longitud_Arreglo/2, -longitud_Arreglo/2, longitud_Arreglo/2], cmap='gray', vmax=0.05*np.max(amplitud_Detector))
axes[1].set_title("Patrón de Difracción")
axes[1].set_xlabel("x (m)")
axes[1].set_ylabel("y (m)")
fig.colorbar(im_difraccion, ax=axes[1], label="Intensidad")  # Barra de color para el patrón de difracción

# Ajustar diseño para evitar superposición de elementos
plt.tight_layout()

# Mostrar las gráficas
plt.show()

