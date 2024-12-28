'''Biblioteca con funciones dft'''

import numpy as np

def Matriz_DFT(resolucion):                                                #Función que retorna una matriz con n, m = resolucion dada que contiene los parámetros necesarios para la DFT
    Frecuencia_base = np.exp(-1j*2*np.pi/resolucion)                       #Frecuencia base para la DFT
    DFT = np.ones((resolucion,resolucion),dtype=np.complex64)              #Matriz llena de unos con tamaño igual a la resolucion x resolucion
    for n in range(0,resolucion,1):                                        #Relleno de filas, n representa las filas
        for m in range(0,resolucion,1):                                    #Relleno de columnas, m representa las columnas
            DFT[n,m] = (Frecuencia_base**n)**m                             #Se asignan las frecuencias correspondientes a cada índice de la matriz
    return DFT

def dft1(Entrada):                                                         #DFT de una entrada 1 dimensional   
    resolucion = len(Entrada)                                              #Calculamos la longitud de la entrada
    DFT_OUT =  Matriz_DFT(resolucion) @ Entrada                            #Realizamos el cálculo de la DFT
    return DFT_OUT

def dft2(Entrada_2D):
    filas, columnas = Entrada_2D.shape                                     #Devuelve las dimensiones de las filas y de las columnas
    
    # Primero, calculamos la DFT para las filas
    DFT_Filas = np.zeros_like(Entrada_2D, dtype=np.complex64)              #Crea un array con la misma forma y tipo de datos del arreglo Entrada_2D
    for i in range(0,filas,1):                                             #Ciclo con longitud igual a las filas
        DFT_Filas[i, :] = dft1(Entrada_2D[i, :])                           #Calcula las DFT de las filas
    
    # Luego, calculamos la DFT para las columnas
    DFT_2D = np.zeros_like(DFT_Filas, dtype=np.complex64)
    for j in range(0,columnas,1):
        DFT_2D[:, j] = dft1(DFT_Filas[:, j])                               #Calcula las DFT sobre las columnas
    
    return DFT_2D

def Matriz_IDFT(resolucion):                                               #Función que retorna una matriz con n, m = resolucion dada que contiene los parámetros necesarios para la DFT
    Frecuencia_base = np.exp(1j*2*np.pi/resolucion)                        #Frecuencia base para la DFT
    DFT = np.ones((resolucion,resolucion),dtype=np.complex64)              #Matriz llena de unos con tamaño igual a la resolucion x resolucion
    for n in range(0,resolucion,1):                                        #Relleno de filas, n representa las filas
        for m in range(0,resolucion,1):                                    #Relleno de columnas, m representa las columnas
            DFT[n,m] = (Frecuencia_base**n)**m                             #Se asignan las frecuencias correspondientes a cada índice de la matriz
    return DFT

def idft1(Entrada):
    resolucion = len(Entrada)                                              #Calculamos la longitud de la entrada
    DFT_OUT =  1/resolucion * Matriz_DFT(resolucion) @ Entrada             #Realizamos el cálculo de la IDFT
    return DFT_OUT

def idft2(Entrada_2D):
    filas, columnas = Entrada_2D.shape                                     #Devuelve las dimensiones de las filas y de las columnas
    
    # Primero, calculamos la DFT para las filas
    DFT_Filas = np.zeros_like(Entrada_2D, dtype=np.complex64)              #Crea un array con la misma forma y tipo de datos del arreglo Entrada_2D
    for i in range(0,filas,1):                                             #Ciclo con longitud igual a las filas
        DFT_Filas[i, :] = idft1(Entrada_2D[i, :])                          #Calcula las DFT de las filas
    
    # Luego, calculamos la DFT para las columnas
    DFT_2D = np.zeros_like(DFT_Filas, dtype=np.complex64)                  #Crea un array con la misma forma y tipo de datos del arreglo Entrada_2D
    for j in range(0,columnas,1):                                          #Ciclo con longitud igual a las filas
        DFT_2D[:, j] = idft1(DFT_Filas[:, j])                              #Calcula las DFT sobre las columnas
    
    return DFT_2D

def dftshift(entrada):
    longitud_entrada = len(entrada)
    mitad = longitud_entrada // 2
    return np.concatenate((entrada[mitad:], entrada[:mitad]))

def dftshift2(entrada):
    filas, columnas = entrada.shape                                        #Creamos dos variables con el número (como float) de filas y columnas
    mitad_filas, mitad_columnas = filas // 2, columnas // 2                #Asignamos la mitad de los valores anteriores a otro para de variables, esto para que el código sea útil con cualquier tamaño
    
    # En esta sección se reordenan los cuadrantes concatenando adecuadamente
    Cuadrante_2 = entrada[:mitad_filas, :mitad_columnas]
    Cuadrante_1 = entrada[:mitad_filas, mitad_columnas:]
    Cuadrante_3 = entrada[mitad_filas:, :mitad_columnas]
    Cuadrante_4 = entrada[mitad_filas:, mitad_columnas:]

    # En esta sección se reorganizan los cuadrantes superiores e inferiores concatenando adecudamente, se termina con el shifteo adecuado 
    Cuadrantes_superiores = np.concatenate((Cuadrante_4, Cuadrante_3), axis=1)
    Cuadrantes_inferiores= np.concatenate((Cuadrante_1, Cuadrante_2), axis=1)
    shifted = np.concatenate((Cuadrantes_superiores, Cuadrantes_inferiores), axis=0)
    return shifted