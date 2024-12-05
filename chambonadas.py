'''CODIGO PARA LA DIFRACCIÓN INVERSA POR ESPECTRO ANGULAR'''

'''  
Estos son los paso que se van a desarrollar para  conseguir la difracción por espectro angular
0. Definir los delta espaciales y frecuenciales que se utilizarán - Estos productos espacio frecuencia se pueden hallar con: from puntos_Mascaras import producto_EspacioFrecuencia [intervalo, resolucion]
1. Aquirir   U(n,m,z) - Esta función es el campo Óptico que se va a cargar para hacer su difracción't
2. Calcular  A[p,q,z] - El esepctro que se propaga en el espacio y con el que vamos a antipropagar
3. Calcular  A[p,q,0] - El espectro del punto en el que se difractó la luz, cabe aclara que vamos a calcularlo con un z arbitrario hasta encontrar una imagen enfocada
4. Calcular  U[n,m,0] - La máscara que causó la difracción
5. Realizar los shifteos necesarios para todo
'''

''' LIBRERIAS USADAS EN EL CODIGO '''
import numpy as np #numpy para usar funciones matematicas
import scipy as sc #scipy para obtener constantes cientificas
import matplotlib.pyplot as plt #matplotlib para graficar funciones
import diffraction_library as diff

########################## CUIDADO!!!!! SOLO FUNCIONA CON VENTANAS CUADRADAS Y MUESTREOS UNIFORMES #######################
############################## TENER EN CUENTA, TODILLO EL CODIGO EN MILÍMETROS ##########################################
#PARÁMETROS PARA LA DIFRACCIÓN POR ESPECTRO ANGULAR TODILLO EN mm

longitud_onda = 632.8E-6                                #longitud de onda de un Láser de He-Ne
numero_onda = 2*np.pi/longitud_onda
Tamaño_pixel = 3.45E-3                                  #3.45 um. Dato del enunciado           
ventana = 2048 * Tamaño_pixel                            #Ventana en mm
resolucion = 2048                                       #Número de puntos
Distancia_z = 150 #Distancia al plano de observación en mm


'''Funciones para calcular la difracción '''

deltas = diff.producto_EspacioFrecuencia(ventana, resolucion)                                #Regresa los delta espacio, frecuencia en un diccionario
X_in, Y_in = diff.malla_Puntos(resolucion, ventana)                                          #Se prepara una malla de puntos para la máscara
X_espectre, Y_espectre = diff.malla_Puntos(resolucion, resolucion*deltas["Delta_F"])         #Se crea una malla de puntos para el espectro
Intensidad_Medida = diff.abrir_imagen(ruta="Intensity.png")                                  #Asignamos un array de valores de intensidad al array en función de la imagen Intensity.png, este el campo U[n,m,z]
Espectro_propagante = np.fft.fftshift(np.fft.fft2(Intensidad_Medida)) / (deltas["Delta_F"]**2)                       #Campo A[p,q,z], este es el campo que se propaga, tener en cuenta que ya está multiplicado por una exponencial compleja de la cual desconocemos su valor de z
Termino_antipropagante = np.exp(-1j*Distancia_z*numero_onda*np.sqrt(1-((longitud_onda**2) * ((X_espectre**2) + (Y_espectre**2))))) #La exponencial que antipropaga el espectro, por eso está con un negativo
Espectro_0 = Espectro_propagante * Termino_antipropagante                                    #Espectro del campo en la entrada, llamese A[p,q,0]
Mascara_Difractora = np.fft.fftshift(np.fft.ifft2(Espectro_0))  / (deltas["Delta_X"]**2)                             #Mascara que produjo la difracción, U[n,m,0]
Geometria_Mascara = np.abs(Mascara_Difractora)**2


''' GRAFICAS '''
fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Crear dos subgráficos (uno para el plano de abertura y otro para el plano de salida)

# Gráfico de la máscara que produjo la difracción
im_entrada = axes[0].imshow(Intensidad_Medida, extent=[X_in[0, 0], X_in[0, -1], Y_in[0, 0], Y_in[-1, 0]], cmap='gray')
axes[0].set_title("Geometría de la abertura")
axes[0].set_xlabel("x (mm)")
axes[0].set_ylabel("y (mm)")
fig.colorbar(im_entrada, ax=axes[0], label="Intensidad")  # Barra de color para el plano de la abertura

# Gráfico del plano de difracción
im_salida = axes[1].imshow(Geometria_Mascara, extent=[X_in[0, 0], X_in[0, -1], Y_in[0, 0], Y_in[-1, 0]], cmap='gray', vmin=0, vmax=np.max(Geometria_Mascara))
axes[1].set_title("Plano de Difracción")
axes[1].set_xlabel("x' (mm)")
axes[1].set_ylabel("y' (mm)")
fig.colorbar(im_salida, ax=axes[1], label="Intensidad")  # Barra de color para el plano de difracción
plt.tight_layout()
plt.show()