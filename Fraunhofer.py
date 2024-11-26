import numpy as np
import matplotlib.pyplot as plt
import puntos_Mascaras as pts

resolucion = 5000  # Número de puntos en la malla
longitud_Arreglo = 0.45  # Tamaño físico del área (10 mm)
radio = 2E-3  # Radio del círculo en metros
centro = [0,0] # El centro será el origen 
long_Onda = 533E-9 #longitud de onda de la iluminacion
distancia = 5000 #distancia de propagacion

# Crear la malla de puntos
xx, yy = pts.malla_Puntos(resolucion, longitud_Arreglo)

# Crear la máscara circular
mascara = pts.funcion_Rectangulo(4E-3, 4E-3, centro, xx, yy)

#calculamos la fft de la iluminacion inicial
fft_Mascara = np.fft.fftshift(np.fft.fft2(mascara))

''' propagacion '''
numero_Onda = 2*np.pi/long_Onda #calculamos el numero de onda para propagar 
fase_Constante = (np.exp(1j* numero_Onda*distancia)) / (1j * long_Onda * distancia) #calculamos el elemento de fase constante para propagar las ondas en fraunhoffer
patron_Difraccion = fft_Mascara * fase_Constante #calculamos el campo optico en el detector
amplitud_Detector = (np.abs(patron_Difraccion)) ** 2 #calculamos la irradiancia sacando el modulo cuadrado 


'''visualizacion de graficas cortes transversales '''

# Visualización de la mascara
plt.figure(figsize=(6, 6))
plt.imshow(np.abs(mascara), extent=[-longitud_Arreglo/2, longitud_Arreglo/2, -longitud_Arreglo/2, longitud_Arreglo/2], cmap='gray')
plt.title("Máscara Circular")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.colorbar(label="Transmitancia")
plt.show()

# Visualización del espectro de la mascara
plt.imshow(np.abs(fft_Mascara), extent=[-longitud_Arreglo/2, longitud_Arreglo/2, -longitud_Arreglo/2, longitud_Arreglo/2], cmap='inferno', vmax= 0.65*(np.max(np.abs(fft_Mascara))))
plt.title("Espectro de la mascara")
plt.xlabel("u (1/m)")
plt.ylabel("v (1/m)")
plt.colorbar(label="Amplitud del espectro")
plt.show()

# Visualizacion del patron de difraccion
plt.imshow(amplitud_Detector, extent=[-longitud_Arreglo/2, longitud_Arreglo/2, -longitud_Arreglo/2, longitud_Arreglo/2], cmap='gray', vmax=0.05*np.max(amplitud_Detector))
plt.title("Patron de difracción")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.colorbar(label="Intensidad")
plt.show()

