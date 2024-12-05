'''Esta es la librería que se usará a lo largo de todos los codigos en este repositorio, contendrá funciones útiles para la implementación de la difracción'''
import numpy as np
import tkinter as tk
from tkinter import filedialog
import cv2


def Matriz_DFT(resolucion):                                                #Función que retorna una matriz con n, m = resolucion dada que contiene los parámetros necesarios para la DFT
    Frecuencia_base = np.exp(-1j*2*np.pi/resolucion)                       #Frecuencia base para la DFT
    DFT = np.ones((resolucion,resolucion),dtype=np.complex64)              #Matriz llena de unos con tamaño igual a la resolucion x resolucion
    for n in range(0,resolucion,1):                                        #Relleno de filas, n representa las filas
        for m in range(0,resolucion,1):                                    #Relleno de columnas, m representa las columnas
            DFT[n,m] = (Frecuencia_base**n)**m                             #Se asignan las frecuencias correspondientes a cada índice de la matriz
    return DFT

def dft1(Entrada):                                      #DFT de una entrada 1 dimensional   
    resolucion = len(Entrada)                           #Calculamos la longitud de la entrada
    DFT_OUT =  Matriz_DFT(resolucion) @ Entrada         #Realizamos el cálculo de la DFT
    return DFT_OUT

def dft2(Entrada_2D):
    filas, columnas = Entrada_2D.shape                          #Devuelve las dimensiones de las filas y de las columnas
    
    # Primero, calculamos la DFT para las filas
    DFT_Filas = np.zeros_like(Entrada_2D, dtype=np.complex64)   # Crea un array con la misma forma y tipo de datos del arreglo Entrada_2D
    for i in range(0,filas,1):                                  # Ciclo con longitud igual a las filas
        DFT_Filas[i, :] = dft1(Entrada_2D[i, :])                # Calcula las DFT de las filas
    
    # Luego, calculamos la DFT para las columnas
    DFT_2D = np.zeros_like(DFT_Filas, dtype=np.complex64)
    for j in range(0,columnas,1):
        DFT_2D[:, j] = dft1(DFT_Filas[:, j])                    # Calcula las DFT sobre las columnas
    
    return DFT_2D

def Matriz_IDFT(resolucion):                                                #Función que retorna una matriz con n, m = resolucion dada que contiene los parámetros necesarios para la DFT
    Frecuencia_base = np.exp(1j*2*np.pi/resolucion)                       #Frecuencia base para la DFT
    DFT = np.ones((resolucion,resolucion),dtype=np.complex64)              #Matriz llena de unos con tamaño igual a la resolucion x resolucion
    for n in range(0,resolucion,1):                                        #Relleno de filas, n representa las filas
        for m in range(0,resolucion,1):                                    #Relleno de columnas, m representa las columnas
            DFT[n,m] = (Frecuencia_base**n)**m                             #Se asignan las frecuencias correspondientes a cada índice de la matriz
    return DFT

def idft1(Entrada):
    resolucion = len(Entrada)                           #Calculamos la longitud de la entrada
    DFT_OUT =  1/resolucion * Matriz_DFT(resolucion) @ Entrada         #Realizamos el cálculo de la IDFT
    return DFT_OUT

def idft2(Entrada_2D):
    filas, columnas = Entrada_2D.shape                          #Devuelve las dimensiones de las filas y de las columnas
    
    # Primero, calculamos la DFT para las filas
    DFT_Filas = np.zeros_like(Entrada_2D, dtype=np.complex64)    # Crea un array con la misma forma y tipo de datos del arreglo Entrada_2D
    for i in range(0,filas,1):                                   # Ciclo con longitud igual a las filas
        DFT_Filas[i, :] = idft1(Entrada_2D[i, :])                # Calcula las DFT de las filas
    
    # Luego, calculamos la DFT para las columnas
    DFT_2D = np.zeros_like(DFT_Filas, dtype=np.complex64)        # Crea un array con la misma forma y tipo de datos del arreglo Entrada_2D
    for j in range(0,columnas,1):                                # Ciclo con longitud igual a las filas
        DFT_2D[:, j] = idft1(DFT_Filas[:, j])                    # Calcula las DFT sobre las columnas
    
    return DFT_2D

def dftshift(entrada):
    longitud_entrada = len(entrada)
    mitad = longitud_entrada // 2
    return np.concatenate((entrada[mitad:], entrada[:mitad]))

def dftshif2(entrada):
    filas, columnas = entrada.shape                             #Creamos dos variables con el número (como float) de filas y columnas
    mitad_filas, mitad_columnas = filas // 2, columnas // 2     #Asignamos la mitad de los valores anteriores a otro para de variables, esto para que el código sea útil con cualquier tamaño
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

def malla_Puntos(resolucion, longitud_Arreglo): #funcion que crea mallas de puntos 
    ''' CREACION DE LAS MALLAS DE PUNTOS 
        
        ENTRARDAS:
        resolucion == numero de puntos que conforman la malla
        longitud_Arreglo == longitud fisica del arreglo, es una correspondencia con longitudes reales en el espacio'''
    
    x = np.linspace(-longitud_Arreglo / 2, longitud_Arreglo / 2, resolucion) #crea las mallas de puntos para el arreglo 
    y = np.linspace(-longitud_Arreglo / 2, longitud_Arreglo / 2, resolucion) 
    xx, yy = np.meshgrid(x, y) #crea una malla de puntos bidimensional 
    return xx, yy #retornamos la malla de puntos


def funcion_Circulo(radio, centro, xx, yy): #definicion de la funcion para hacer un circulo transparente en una malla ded puntos
    ''' CREACCION DEL CONJUNTO DE PUNTOS DE LA MASCARA DE DFRACCION 

        ENTRADAS:
        radio == radio de circunferencia
        centro == array con las coordenadas espaciales del centro de la circunferencia
        xx, yy == malla de puntos bidimensional en la cual se crea la circunferencia'''
    
    if centro is None: # que pasa si el centro no es definido en la funcion
        centro = [0, 0] #ubica el centro de la circunferencia en el origen
    distancia = (xx - centro[0])**2 + (yy - centro[1])**2 #calculamos la distancia desde el centro de la circunferencia a cada punto
    mascara = distancia <= radio**2 #los puntos de la mascara seran los puntos cuya distancia al centro es menor que el radio
    return mascara #devolvemos los puntos que cumplen la condicion para hacer parte de la mascara

def funcion_Rectangulo(base, altura, centro, xx, yy): #funcion para realizar una funcion rectangulo
    ''' CREACION DE UN CONJUNTO DE PUNTOS QUE HACEN UNA ABERTURA RECTANGULAR
     
      ENTRADAS:
        base == longitud de la base del rectangulo
        altura == longitud de la altura del rectangulo
        centro == array con las coordenadas espaciales del centro del rectangulo
        xx, yy == malla de puntos bidimensional en la cual se crea el rectangulo '''

    if centro is None: #que es lo que pasa si no se especifica el centro del rectangulo
        centro = [0, 0] #el centro se ubicca por defecto en el origen
    x_Min = centro[0] - base / 2 #calculos de las distancias limite del rectangulo
    x_Max = centro[0] + base / 2
    y_Min = centro[1] - altura / 2
    y_Max = centro[1] + altura / 2

    mascara = (xx <= x_Max) & (xx >= x_Min) & (yy <= y_Max) & (yy >= y_Min) #filtrado de los puntos al interior del rectangulo 

    return mascara #retorno la mascara

def producto_EspacioFrecuencia (intervalo, resolucion): #funcion que saca los intervalos relativos al producto espacio frecuencia y devuelve los deltas de espacio y de frecuencia
    ''' FUNCION QUE RETORNA LOS DELTA ESPACIO Y DELTA FRECUENCIA PARA UN MUESTREO EN PARTICULAR.

    ATENCION!!!!!!!!!!  ESTA FUNCION ASUME QUE SE ESTAN USANDO MUESTREOS UNIFORMES TANTO EN X COMO EN Y, DE LA MISMA LONGITUD DE INTERVALO Y NUMERO DE PUNTOS EN 
    AMBAS DIRECCIONES
     
        ENTRADAS:
        intervalo == longitud fisica del intervalo del arreglo
        resolucion == numero de puntos que tiene la malla del arreglo '''
    
    deltax = intervalo / resolucion #calculo del delta de espacio
    deltaf = 1 / (deltax *resolucion) #calculo del delta de frecuencias usando el producto espacio-frecuencias
    deltas = {"Delta_X": deltax, "Delta_F": deltaf} #agregamos los deltas a una lista
    return deltas #retornamos el diccionario con los deltas

#Función para seleccionar una imagen desde el PC y convertirla en un array normalizado de escala de grises
def seleccionar_imagen(): 
    root = tk.Tk()                  # Crea una ventana oculta para el diálogo de archivo
    root.withdraw()                 # Oculta la ventana que acabamos de crear, para no mostrar nada
    ruta_imagen = filedialog.askopenfilename(
    title="Selecciona una imagen",
    filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif")])
    array_grises = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)      #Leer la escala de grises
    array_intensidades = array_grises/255                             #Normalizar el Array
    return array_intensidades

#Función para darle una ruta y que devuelva el array correspondiente - solo cuestión de no andar poniendo comandos al ejecutar
def abrir_imagen(ruta):
    array_grises = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
    array_intensidades = array_grises / 255
    return  array_intensidades
