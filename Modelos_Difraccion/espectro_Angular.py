''' CODIGO PARA MOSTRAR LA DIFRACCIÓN POR ESPECTRO ANGULAR'''

'''  
Estos son los paso que se van a desarrollar para  conseguir la difracción por espectro angular
0 Definir los delta espaciales y frecuenciales que se utilizarán - Estos productos espacio frecuencia se pueden hallar con: from puntos_Mascaras import producto_EspacioFrecuencia [intervalo, resolucion]
1 Generar U[n,m,0]  - Este campo se va a generar a través de las funciones contenidas en puntos_Mascaras
2 Calcular A[p,q,0] - Este cálculo será realizado a través de la función espectro_Fuente, la cuál retorna el espectro de U(n,m,0)
3 Calcular A[p,q,z] - Esta función se calcula con una multiplicación sencilla entre un término propagante y A[p,q,0]
4 Calcular U[n,m,z] - Esta función es el campo Óptico observado en la panatalla de observación a alguna distancia z
5 Se shiftea el resultado
'''


''' LIBRERIAS USADAS EN EL CODIGO '''
import numpy as np #numpy para usar funciones matematicas
import matplotlib.pyplot as plt #matplotlib para graficar funciones
import optics_library.mascaras as opt
import optics_library.graficas as graf

########################## CUIDADO!!!!! SOLO FUNCIONA CON VENTANAS CUADRADAS Y MUESTREOS UNIFORMES #######################'''

#PARÁMETROS SUGERIDOS PARA UNA ABERTURA CIRCULAR

'''
longitud_onda = 632.8E-9                                #longitud de onda de un Láser de He-Ne
ventana = 7E-3                                             #Ventana en mm
resolucion = 2048                                       #Número de puntos
radio = 1E-3                                               #Radio de 1.5mm para el círculo 
Distancia_z = 15E-3                                     #Distancia al plano de observación en mm
'''

def espectro_angular(mascara, ventana, distancia_Propagacion, longitud_Onda):
    '''
    Esta función calcula la difracción a través del método de espectro angular.
    ENTRADAS:
        mascara == grid 2D el cuál simboliza la apertura por la cual la luz se propaga
        ventana == tamaño de la ventana de observación
        Distancia_z == Distancia que se propaga el espectro desde que choca con la mascara
    RETORNA:
        Ventana emergente con el gráfico que representa la difracción
    '''
    
    '''Funciones para calcular la difracción '''
    resolucion = len(mascara)
    numero_onda = 2*np.pi/longitud_Onda
    deltas = opt.producto_EspacioFrecuencia(ventana, resolucion)                                #Regresa los delta espacio, frecuencia en un diccionario
    X_in, Y_in = opt.malla_Puntos(resolucion, ventana)                                          #Se prepara una malla de puntos para la máscara                              
    X_espectre, Y_espectre = opt.malla_Puntos(resolucion, resolucion*deltas["Delta_F"])         #Se crea una malla de puntos para el espectro
    espectro_0 = (deltas["Delta_X"]**2) * np.fft.fftshift(np.fft.fft2(mascara))                 #Se calcula   la A[x,y,0]
    termino_propagante = np.exp(1j*distancia_Propagacion*numero_onda*np.sqrt(1-((longitud_Onda**2) * ((X_espectre**2) + (Y_espectre**2)))))
    espectro_propagante = espectro_0 * termino_propagante                                       #Calculamos el espectro A[x,y,z]
    Campo_Propagante = (deltas["Delta_F"]**2) * np.fft.ifft2(espectro_propagante)               #Calculamos el campo U[x,y,z] y lo shifteamos
    #intensidad_Salida = np.abs(Campo_Propagante)**2

    ''' GRAFICAS 
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
    plt.show() '''
    return Campo_Propagante

'''
# Gráfico de la función de transferencia
im_salida = axes[1].imshow(np.angle(espectro_propagante), extent=[X_in[0, 0], X_in[0, -1], Y_in[0, 0], Y_in[-1, 0]], cmap='gray' )
axes[1].set_title("Plano de Difracción")
axes[1].set_xlabel("x' (mm)")
axes[1].set_ylabel("y' (mm)")
fig.colorbar(im_salida, ax=axes[1], label="Intensidad")  # Barra de color para el plano de difracción
'''

malla_X, malla_Y = opt.malla_Puntos(1024, 5E-3)
mascara = opt.funcion_Circulo(0.25E-3, None, malla_X, malla_Y)
campo = espectro_angular(mascara, 5E-3, 0.1, 533E-9)
graf.fase(campo, 5E-3)
