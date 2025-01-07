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
import optics_library.mascaras as diff

########################## CUIDADO!!!!! SOLO FUNCIONA CON VENTANAS CUADRADAS Y MUESTREOS UNIFORMES #######################

def Intensidad_Antipropagante(Ruta_Campo_Intensidades, Distancia_z, Tamaño_pixel, longitud_onda = 632.8E-9):
    '''
    A partir de una imagen en escala de grises que representan la intensidad medida se obtiene la
    antipropagación a través del método de espectro angular
    ENTRADAS:
        Ruta_Campo_Intensidades == string , ruta donde se encuentra almacenada esta parte del campo
        Distancia_z == float , Distancia que se desea antipropagar el campo complejo
        Tamaño_pixel == float , Tamaño físico del píxel de la imagen del campo proporcionado
    RETORNA:
        Campo Óptico antipropagado
    '''
    numero_onda = 2*np.pi/longitud_onda
    Intensidad_Medida = diff.img_to_array(Ruta_Campo_Intensidades)                               #Asignamos un array de valores de intensidad al array en función de la imagen Intensity.png, este el campo U[n,m,z]
    resolucion = len(Intensidad_Medida)                                                          #Se adquiere la resolución de la imagen de entrada
    ventana = resolucion * Tamaño_pixel                                                          #Se calcula el tamaño de la ventana
    deltas = diff.producto_EspacioFrecuencia(ventana, resolucion)                                #Regresa los delta espacio, frecuencia en un diccionario
    X_espectre, Y_espectre = diff.malla_Puntos(resolucion, resolucion*deltas["Delta_F"])         #Se crea una malla de puntos para el espectro
    Campo_Amplitud = np.sqrt(Intensidad_Medida)                                                  #Obtenemos el campo de amplitudes a partir del campo de intensidades
    Espectro_propagante = np.fft.fftshift(np.fft.fft2(Campo_Amplitud)) / (deltas["Delta_F"]**2)  #Campo A[p,q,z], este es el campo que se propaga, tener en cuenta que ya está multiplicado por una exponencial compleja de la cual desconocemos su valor de z
    Termino_antipropagante = np.exp(-1j*Distancia_z*numero_onda*np.sqrt(1-((longitud_onda**2) * ((X_espectre**2) + (Y_espectre**2))))) #La exponencial que antipropaga el espectro, por eso está con un negativo
    Espectro_0 = Espectro_propagante * Termino_antipropagante                                    #Espectro del campo en la entrada, llamese A[p,q,0]
    Mascara_Difractora = (np.fft.ifft2(Espectro_0))  / (deltas["Delta_X"]**2)                    #Mascara que produjo la difracción, U[n,m,0]
    return Mascara_Difractora

'''Función para calcular la anti difracción adquiriendo el campo complejo'''

def Compleja_Antipropagante(Ruta_Campo_Real,Ruta_Campo_Complejo, Distancia_z, Tamaño_pixel, longitud_onda = 632.8E-9):
    '''
    A partir de dos imágenes que componen los valores en escala de grises de un campo óptico complejo,
    se obtiene la antipropagación a través del método de espectro angular.
    ENTRADAS:
        Ruta_Campo_Real == string , ruta donde se encuentra almacenada esta parte del campo
        Ruta_Campo_Complejo == string , ruta donde se encuentra almacenada esta parte del campo
        Distancia_z == float , Distancia que se desea antipropagar el campo complejo
        Tamaño_pixel == float , Tamaño físico del píxel de la imagen del campo proporcionado
    RETORNA:
        Campo Óptico antipropagado
    '''
    numero_onda = 2*np.pi/longitud_onda
    Parte_Real = diff.img_to_array(Ruta_Campo_Real)                                      #Asignamos un array de valores de intensidad al array en función de la imagen real.png, este es la parte real del campo Complej U[n,m,z]
    Parte_Imaginaria = diff.img_to_array(Ruta_Campo_Complejo)                              #Parte imaginaria del Campo Complejo U[n,m,z]
    resolucion = len(Parte_Real)                                                                 #Se adquiere la resolución de la imagen de entrada
    ventana = resolucion * Tamaño_pixel                                                          #Se calcula el tamaño de la ventana
    deltas = diff.producto_EspacioFrecuencia(ventana, resolucion)                                #Regresa los delta espacio, frecuencia en un diccionario
    X_espectre, Y_espectre = diff.malla_Puntos(resolucion, resolucion*deltas["Delta_F"])         #Se crea una malla de puntos para el espectro
    Campo_Complejo = Parte_Real + 1j*Parte_Imaginaria                                            #Campo Complejo completo U[n,m,z]
    Espectro_propagante = np.fft.fftshift(np.fft.fft2(Campo_Complejo)) / (deltas["Delta_F"]**2)  #Campo A[p,q,z], este es el campo que se propaga, tener en cuenta que ya está multiplicado por una exponencial compleja de la cual desconocemos su valor de z
    Termino_antipropagante = np.exp(-1j*Distancia_z*numero_onda*np.sqrt(1-((longitud_onda**2) * ((X_espectre**2) + (Y_espectre**2))))) #La exponencial que antipropaga el espectro, por eso está con un negativo
    Espectro_0 = Espectro_propagante * Termino_antipropagante                                    #Espectro del campo en la entrada, llamese A[p,q,0]
    Mascara_Difractora = (np.fft.ifft2(Espectro_0))  / (deltas["Delta_X"]**2)                    #Mascara que produjo la difracción, U[n,m,0]
    return Mascara_Difractora