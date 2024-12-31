import numpy as np
import matplotlib.pyplot as plt
import optics_library.mascaras as opt

def fraunhofer(mascara, ventana, distancia_Propagacion, longitud_Onda):
    ''' Funcion que realiza el calculo del campo optico usando la aproximacion de Fraunhofer 
    ENTRADAS:
    - mascara: Puntos presentes en la mascara a travez de la cual se va a difractar
    - ventana: Longitud fisica del ancho de la ventana, la funcion asume por default ventanas cuadradas
    - distancia_propagacion: es la distancia entre el plano de la mascara y el plano del detector
    - longitud_Onda: longitud de onda de la iluminacion
    
    RETORNA: Distribucion de campo optico en el plano de salida'''

    resolucion = len(mascara) #la resolucion es el numero de puntos que hay presentes en el arreglo mascara
    fft_Mascara = np.fft.fftshift(np.fft.fft2(mascara)) #calculamos la fft de la iluminacion inicial

    ''' propagacion '''
    numero_Onda = 2*np.pi/longitud_Onda #calculamos el numero de onda para propagar 
    mascara_X, mascara_Y = opt.malla_Puntos(resolucion, ventana) #creamos una malla de puntos para las coordenadas del plano de entrada
    fase_Constante = (np.exp(1j* numero_Onda*distancia_Propagacion)) / (1j * longitud_Onda * distancia_Propagacion) #calculamos el elemento de fase constante para propagar las ondas en fraunhoffer
    fase_Parabolica = np.exp(1j * (numero_Onda / (2* distancia_Propagacion))*(mascara_X**2 + mascara_Y**2)) #calculamos el campo difrractado
    patron_Difraccion = fft_Mascara * fase_Constante * fase_Parabolica #calculamos el campo optico en el detector

    return patron_Difraccion #retornamos el campo optico difractado    


'''
resolucion = 2040  # Número de puntos en la malla
longitud_Arreglo = 0.1  # Tamaño físico del área (10 mm)
radio = 2E-3  # Radio del círculo en metros
centro = [0,0] # El centro será el origen 
long_Onda = 632.8E-9 #longitud de onda de la iluminacion
distancia = 5000 #distancia de propagacion
# Crear la malla de puntos
xx, yy = opt.malla_Puntos(resolucion, longitud_Arreglo)

# Crear la máscara circular
mascara = opt.funcion_Rectangulo(1E-3, 1E-3, centro, xx, yy)

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

'''