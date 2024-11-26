''' CODIGO PARA MOSTRAR LA DIFRACCIÓN POR ESPECTRO ANGULAR'''

''' Comentario temporal para acordarme de los pasos necesarios a realizar para la implementación
de la dufracción por espectro Angular
0 Definir los delta espaciales y frecuenciales que se utilizarán - Estos productos espacio frecuencia se pueden hallar con: from puntos_Mascaras import producto_EspacioFrecuencia [intervalo, resolucion]
1 Generar U[n,m,0] - Este campo se va a generar a través de las funciones contenidas en puntos_Mascaras
2 Calcular A[p,q,0] - Este cálculo será realizado a través de la función espectro_Fuente, la cuál retorna el espectro de U(n,m,0)
3 Calcular A[p,q,z] - esta función se calcula con una multiplicación sencilla entre un término propagante y A[p,q,0]
4
5 '''


''' LIBRERIAS USADAS EN EL CODIGO '''
import numpy as np #numpy para usar funciones matematicas
import scipy as sc #scipy para obtener constantes cientificas
import matplotlib.pyplot as plt #matplotlib para graficar funciones
import puntos_Mascaras as pts

''' FUNCIONES UTILES PARA SACAR FRECUENCIAS DEPENDIENDO DE LOS PARAMETROS DE MUESTREO ...

########################## CUIDADO!!!!! SOLO FUNCIONA CON VENTANAS CUADRADAS Y MUESTREOS UNIFORMES #######################'''

#PARÁMETROS PARA LA DIFRACCIÓN POR ESPECTRO ANGULAR TODILLO EN mm

longitud_onda = 632.8e-6                                #longitud de onda de un Láser de He-Ne
numero_onda = 2*np.pi/longitud_onda
ventana = 20                                            #Ventana de 5cm
resolucion = 3000                                       #1024 puntos
radio = 1                                               #Radio de 1.5mm para el círculo 
Distancia_z = 10                                       #Distancia al plano de observación

'''Funciones para calcular la difracción '''
deltas = pts.producto_EspacioFrecuencia(ventana, resolucion)                                #Regresa los delta espacio, frecuencia en un diccionario
X_in, Y_in = pts.malla_Puntos(resolucion, ventana)                                          #Se prepara una malla de puntos para la máscara
X_espectre, Y_espectre = pts.malla_Puntos(resolucion, resolucion*deltas["Delta_F"])
mascara = pts.funcion_Circulo(radio, None, X_in,Y_in)                                       #Se crea la mascara de un círculo, este va a ser el Campo U[x,y,0] de entrada
espectro_0 = (deltas["Delta_X"]**2) * np.fft.fft2(mascara)                                 #Se calcusla A[x,y,0]
termino_propagante = np.exp(1j*Distancia_z*numero_onda*np.sqrt(1-((longitud_onda**2) * ((X_espectre**2) + (Y_espectre**2)))))
espectro_propagante = espectro_0 * termino_propagante        #Calculamos el espectro A[x,y,z]
Campo_Propagante = (deltas["Delta_F"]**2) * np.fft.ifft2(espectro_propagante) #Calculamos el campo U[x,y,z] y lo shifteamos
intensidad_Salida = np.abs(Campo_Propagante)**2

''' GRAFICAS '''
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

# Mostrar ambas gráficas
plt.tight_layout()
plt.show()