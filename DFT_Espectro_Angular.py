'''CODIGO PARA HACER EL ESPECTRO ANGULAR A TRAVÉS DE UNA DFT
############  ¡¡¡ OJO !!! SIN ALGORITMOS FFT   ############# 
### ¡¡¡SOLO FUNCIONA CON ARREGLOS UNIFORMES Y CUADRADOS ####
# '''          
'''  
Estos son los paso que se van a desarrollar para 
0 Definir los delta espaciales y frecuenciales que se utilizarán - Estos productos espacio frecuencia se pueden hallar con: from puntos_Mascaras import producto_EspacioFrecuencia [intervalo, resolucion]
1 Generar U[n,m,0]  - Este campo se va a generar a través de las funciones contenidas en puntos_Mascaras
2 Calcular A[p,q,0] - Este cálculo será realizado a través de la función espectro_Fuente, la cuál retorna el espectro de U(n,m,0)
3 Calcular A[p,q,z] - Esta función se calcula con una multiplicación sencilla entre un término propagante y A[p,q,0]
4 Calcular U(n,m,z) - Esta función es el campo Óptico observado en la panatalla de observación a alguna distancia z
5 Se shiftea el resultado
'''

''' LIBRERIAS USADAS EN EL CODIGO '''
import numpy as np #numpy para usar funciones matematicas
import scipy as sc #scipy para obtener constantes cientificas
import matplotlib.pyplot as plt #matplotlib para graficar funciones
import puntos_Mascaras as pts
import Funciones_DFT as dft
import time

''' Parámetros que se utilizarán para sacar la Difracción por espectro angular todas las medidas en mm '''

longitud_onda = 632.8e-6                                #longitud de onda de un Láser de He-Ne
numero_onda = 2*np.pi/longitud_onda                     #Pues sí, el número de onda
ventana = 7                                             #Ventana en mm
resolucion = 512                                        #Número de puntos 
radio = 1                                               #Radio de 1.5mm para el círculo 
Distancia_z = 15                                        #Distancia al plano de observación en mm

#Función para calcular el tiempo que tarda el código
Reloj_1 = time.time()

'''Funciones para calcular la difracción '''
deltas = pts.producto_EspacioFrecuencia(ventana, resolucion)                                #Regresa los delta espacio, frecuencia en un diccionario
X_in, Y_in = pts.malla_Puntos(resolucion, ventana)                                          #Se prepara una malla de puntos para la máscara
X_espectre, Y_espectre = pts.malla_Puntos(resolucion, resolucion*deltas["Delta_F"])         #Se crea una malla de puntos para el espectro
mascara = pts.funcion_Circulo(radio, None, X_in,Y_in)                                       #Se crea la mascara de un círculo, este va a ser el Campo U[x,y,0] de entrada
espectro_0 =   (deltas["Delta_X"]**2) * np.fft.fftshift(dft.dft2(mascara))
termino_propagante = np.exp(1j*Distancia_z*numero_onda*np.sqrt(1-((longitud_onda**2) * ((X_espectre**2) + (Y_espectre**2)))))
espectro_propagante = espectro_0 * termino_propagante        #Calculamos el espectro A[x,y,z]
Campo_Propagante = (deltas["Delta_F"]**2) * np.fft.fftshift(dft.idft2(espectro_propagante)) #Calculamos el campo U[x,y,z] y lo shifteamos
intensidad_Salida = np.fft.fftshift(np.abs(Campo_Propagante)**2)

#Funciones para calcular el tiempo que tarda el codigo
Reloj_2 = time.time()
Final = Reloj_2 -Reloj_1
print("El código tardó ejecutándose: ", Final)

'''GRÁFICAS'''
fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Crear dos subgráficos (uno para el plano de abertura y otro para el plano de salida)

# Gráfico del plano de la abertura
im_entrada = axes[0].imshow(mascara, extent=[X_in[0, 0], X_in[0, -1], Y_in[0, 0], Y_in[-1, 0]], cmap='gray', vmin=0, vmax=np.max(mascara))
axes[0].set_title("Plano de la Abertura")
axes[0].set_xlabel("x (mm)")
axes[0].set_ylabel("y (mm)")
fig.colorbar(im_entrada, ax=axes[0], label="Intensidad")  # Barra de color para el plano de la abertura

# Gráfico del plano de difracción
im_salida = axes[1].imshow(intensidad_Salida, extent=[X_in[0, 0], X_in[0, -1], Y_in[0, 0], Y_in[-1, 0]], cmap='gray', vmin=0, vmax=np.max(intensidad_Salida))
axes[1].set_title("Plano de Difracción")
axes[1].set_xlabel("x' (mm)")
axes[1].set_ylabel("y' (mm)")
fig.colorbar(im_salida, ax=axes[1], label="Intensidad")  # Barra de color para el plano de difracción

plt.tight_layout()
plt.show()