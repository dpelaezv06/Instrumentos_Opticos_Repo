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
import time

########################## CUIDADO!!!!! SOLO FUNCIONA CON VENTANAS CUADRADAS Y MUESTREOS UNIFORMES #######################'''

#PARÁMETROS PARA LA DIFRACCIÓN POR ESPECTRO ANGULAR TODILLO EN mm

longitud_onda = 632.8e-6                                #longitud de onda de un Láser de He-Ne
numero_onda = 2*np.pi/longitud_onda
ventana = 7                                             #Ventana en mm
resolucion = 2048                                       #Número de puntos
radio = 1                                               #Radio de 1.5mm para el círculo 
Distancia_z = 15                                        #Distancia al plano de observación en mm
'''Funciones para calcular la difracción '''
deltas = diff.producto_EspacioFrecuencia(ventana, resolucion)                                #Regresa los delta espacio, frecuencia en un diccionario
