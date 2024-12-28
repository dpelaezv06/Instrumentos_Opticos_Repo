"Biblioteca para la creación de máscaras"
import numpy as np
import tkinter as tk
from tkinter import filedialog
import cv2

'''Funciones para creación de máscaras'''

def malla_Puntos(resolucion, longitud_Arreglo): #funcion que crea mallas de puntos 
    ''' CREACION DE LAS MALLAS DE PUNTOS 
        
        ENTRARDAS:
        resolucion == numero de puntos que conforman la malla
        longitud_Arreglo == longitud fisica del arreglo, es una correspondencia con longitudes reales en el espacio'''
    
    x = np.linspace(-longitud_Arreglo / 2, longitud_Arreglo / 2, resolucion) #crea las mallas de puntos para el arreglo 
    y = np.linspace(-longitud_Arreglo / 2, longitud_Arreglo / 2, resolucion) 
    xx, yy = np.meshgrid(x, y) #crea una malla de puntos bidimensional 
    return xx, yy #retornamos la malla de puntos

def funcion_punto_3(m, L, xx): # Función que retorna un array con la transmitancia de la función 1/2 + m/2 cos(2*pi*x/L). La del punto 3
    ''' ¡¡¡¡    OJO    !!!!!
    xx debe estar creado a partir de la función malla_puntos para un correcto funcionamiento bidimensional
    '''
    transmitancia = (1 / 2) + (m / 2) * (np.cos(2 * np.pi * xx / L))
    return transmitancia

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