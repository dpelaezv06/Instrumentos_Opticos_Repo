import numpy as np
import matplotlib.pyplot as plt
import optics_library.mascaras as opt
import time

''' FUNCIONES PROPIAS DEL PROGRAMA'''


def transformada_Fresnel(mascara, ventana, distancia_Propagacion, longitud_Onda):
    ''' Funcion para calcular el campo optico difractado a traves de una mascara usando transformada de fresnel
    ENTRADAS:
    - mascara: Mascara a traves de la cual se va a realizar la difraccion
    - ventana: Ancho de la ventana cuadrada
    - distancia_Propagacion: Distancia entre el plano de la mascara y el plano del detector
    - longitud_Onda: Longitud de onda de la iluminacion
    
    RETORNA: La distribucion de campo optico en el plano de deteccion'''



    ''' Calculo de los terminos que intervienen en el modelo de difraccion por transformada de fresnel '''
    numero_Onda = 2*np.pi / longitud_Onda       #numero de onda
    resolucion = len(mascara) #el numero de puntos que intervienen en el calculo es el mismo del numero de muestras en la mascara
    xx_Entrada, yy_Entrada = opt.malla_Puntos(resolucion, ventana) #Coordenadas del plano de entrada
    fase_ParabolicaEntrada = np.exp(1j * (numero_Onda / (2 * distancia_Propagacion)) * ((xx_Entrada ** 2) + (yy_Entrada **2))) #calculo de a fase parabolica para multiplicar la transmitancia antes de aplicar FFT
    fase_Constante = ((np.exp(1j * numero_Onda * distancia_Propagacion)) / (1j * longitud_Onda * distancia_Propagacion)) #calculo de la fase constante para multiplicar la FFT y obtener el campo de salida
    
    ''' calculo de las coordenadas del plano de salida usando el producto espacio frecuencia modificado para la transformada de fresnel '''
    deltas_Espacio = opt.producto_EspacioFrecuenciaFresnel(longitud_Onda, distancia_Propagacion, ventana, resolucion) #calculamos los deltas del producto espacio frecuencia del 
    longitud_VentanaSalida = resolucion * deltas_Espacio["delta_Llegada"] #la longitud del arreglo de la ventana de salida o el muestreo en el detector calculado usando el producto espacio frecuencia propio de la transformada de fresnel
    xx_Salida, yy_Salida = opt.malla_Puntos(resolucion, longitud_VentanaSalida) #malla de puntos del muestreo del plano de salida (el detector)
    
    ''' termino de la fase parabolica en el plano de salida '''
    fase_ParabolicaSalida = np.exp((1j * (numero_Onda / (2 * distancia_Propagacion)) * ((xx_Salida ** 2) + (yy_Salida ** 2)))) #calculo de la fase parabolica en el plano de salida usando las coordenadas calculados en el plano de salida
    
    ''' operaciones para obtener el campo de salida '''
    campo_EntradaParabolico = mascara * fase_ParabolicaEntrada #preparamos el campo de entrada para meterlo a la fft
    campo_SalidaSinEscalar = np.fft.fft2(campo_EntradaParabolico) #calculamos la fft del campo de entrada multiplicado por la fase parabolica
    campo_Salida = np.fft.fftshift(campo_SalidaSinEscalar) * (deltas_Espacio["delta_Llegada"] ** 2) * fase_Constante * fase_ParabolicaSalida #escalamos el campo de salida con las constantes

    return campo_Salida #retorna la distribucion de campo optico a la salida




'''
#Relativas a la fuente de iluminacion
longitud_Onda = 533E-9          #longitud de onda a utilizar
distancia_Propagacion = (4 * ((1E-5)**2))/longitud_Onda      #distancia entre plano de mascara y plano de observacion
#distancia_Propagacion = 0.01

#Relativas a la malla de puntos y la disposicion de la mascara
ventana = 0.008
resolucion = 8000

#mascara = diff.funcion_Rectangulo(3E-3,3E-3,None,xx_Entrada,yy_Entrada)
#mascara = diff.funcion_Circulo(1E-3, None, xx_Entrada, yy_Entrada)  
mascara = opt.funcion_punto_3(1, 1E-5, xx_Entrada)






intensidad_Salida = (np.abs(campo_Salida)) ** 2 #calculamos el patron de difraccion sacando modulo cuadrado


#graficas
fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Crear dos subgráficos (uno para el plano de abertura y otro para el plano de salida)

# Gráfico del plano de la abertura
im_entrada = axes[0].imshow(mascara, extent=[-ventana/2, ventana/2, -ventana/2, ventana/2], cmap='gray', vmin=0, vmax=np.max(mascara))
axes[0].set_title("Plano de la Abertura")
axes[0].set_xlabel("x (m)")
axes[0].set_ylabel("y (m)")
fig.colorbar(im_entrada, ax=axes[0], label="Intensidad")  # Barra de color para el plano de la abertura

# Gráfico del plano de difracción
im_salida = axes[1].imshow(np.log(1+intensidad_Salida), extent=[-longitud_VentanaSalida/2, longitud_VentanaSalida/2, -longitud_VentanaSalida/2, longitud_VentanaSalida/2], cmap='grey', vmin=0)
axes[1].set_title("Plano de Difracción")
axes[1].set_xlabel("x' (m)")
axes[1].set_ylabel("y' (m)")
fig.colorbar(im_salida, ax=axes[1], label="Intensidad")  # Barra de color para el plano de difracción

# Mostrar ambas gráficas
plt.tight_layout()
plt.show()

'''