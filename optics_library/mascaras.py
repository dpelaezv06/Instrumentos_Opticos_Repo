"Biblioteca para la creación de máscaras"
import numpy as np
import tkinter as tk
from tkinter import filedialog
import cv2
import random
from typing import Tuple

'''Funciones para creación de máscaras'''

def malla_Puntos(puntos_Ancho, ancho_Arreglo, puntos_Alto = None, alto_Arreglo=None):
    ''' Crea mallas de puntos
    ENTRADAS:
        puntos_Ancho -> cantidad de puntos en el ancho
        puntos_Alto -> cantidad de puntos en el alto
        ancho_Arreglo -> longitud física del ancho
        alto_Arreglo -> longitud física del alto (opcional, por defecto igual a ancho_Arreglo)
    RETORNA:
        xx, yy -> malla de puntos bidimensional'''
    

    ''' Definicion de valores por default para ancho y alto, si no se especifican entonces le muestreo es cuadrado y uniforme '''
    if alto_Arreglo is None:
        alto_Arreglo = ancho_Arreglo

    if puntos_Alto is None:
        puntos_Alto = puntos_Ancho
    
    x = np.linspace(-ancho_Arreglo / 2, ancho_Arreglo / 2, puntos_Ancho) #crea las mallas de puntos para el arreglo 
    y = np.linspace(-alto_Arreglo / 2, alto_Arreglo / 2, puntos_Alto) 
    xx, yy = np.meshgrid(x, y) #crea una malla de puntos bidimensional 
    return xx, yy #retornamos la malla de puntos

def muestreo_SegunSensorFresnel(puntos_AnchoSensor, ancho_Sensor, distancia_Propagacion, longitud_Onda, puntos_AltoSensor = None, alto_Sensor=None):

    ''' Crea mallas de puntos
    ENTRADAS:
    puntos_Ancho -> cantidad de puntos en el ancho
    puntos_Alto -> cantidad de puntos en el alto
    ancho_Arreglo -> longitud física del ancho
    alto_Arreglo -> longitud física del alto (opcional, por defecto igual a ancho_Arreglo)

    RETORNA:
    Un diccionario con el muestreo en x y y (horizontal y vertical) que se debe hacer al campo de entrada considerando las caracteristicas fisicas de
    un sensor particular usado

    "delta_XEntrada" -> distancia entre puntos del muestreo horizontal del campo de entrada
    "delta_YEntrada" -> distancia entre puntos del muestreo vertical del campo de entrada

    '''


    ''' Definicion de parametros default, el caso deafult comprende un sensor cuadrado de muestreo uniforme en x y y '''
    if alto_Sensor is None: #definicion del alto por default
        alto_Sensor = ancho_Sensor #en caso default el ancho y el alto son iguales

    if puntos_AltoSensor is None: # definicion del muestreo vertical por defualt
        puntos_AltoSensor = puntos_AnchoSensor #el caso default es un muestreo uniforme
        

    delta_XSensor = ancho_Sensor / puntos_AnchoSensor #calculamos el espaciamiento horizontal entre los puntos del sensor
    delta_YSensor = alto_Sensor / puntos_AltoSensor #calculamos el espaciamiento vertical entre los puntos del sensor

    delta_EntradaX = (longitud_Onda * distancia_Propagacion) / (puntos_AnchoSensor * delta_XSensor) #calculamos el espaciamiento horizontal en la entrada teniendo en cuenta el producto espacio-frecuencia de fresnel
    delta_EntradaY = (longitud_Onda * distancia_Propagacion) / (puntos_AltoSensor * delta_YSensor) #calculamos el espaciamiento horizontal en la entrada teniendo en cuenta el producto espacio-frecuencia de fresnel

    muestreo_Entrada = {"delta_XEntrada" : delta_EntradaX, "delta_YEntrada" : delta_EntradaY} # creamos un diccionario para retornar el muestreo de la fuente en x y y segun el sensor usado 

    return muestreo_Entrada #retornamos el diccionario que contiene los parametros de muestreo en el campo de entrada teniendo en cuenta el muestreo del sensor

def funcion_punto_3(m, L, xx): # Función que retorna un array con la transmitancia de la función 1/2 + m/2 cos(2*pi*x/L). La del punto 3
    '''
    Crea un meshgrid con la función requerida en el punto 3 de la entrega 1
    1/2 + m/2 * cos(2*pi*xx/L)
    ENTRADAS:
        m, L == Parametros de la funcion
        xx == grid en el cuál se quiere representar la funcion, favorablemente que provenga de malla_Puntos
    RETORNA:
        La mascara de transmitancia
    '''
    transmitancia = (1 / 2) + (m / 2) * (np.cos(2 * np.pi * xx / L))
    return transmitancia

def funcion_Circulo(radio, centro, xx, yy, opacidad = 1): #definicion de la funcion para hacer un circulo transparente en una malla de puntos
    ''' 
    Crea una máscara con un círculo 
    ENTRADAS:
        radio == radio de circunferencia
        centro == array con las coordenadas espaciales del centro de la circunferencia
        xx, yy == malla de puntos bidimensional en la cual se crea la circunferencia
        opacidad == valor de la transmitancia dentro del círculo
    RETORNA:
        Mascara con un círculo (Claramente)
    '''
    
    if centro is None: # que pasa si el centro no es definido en la funcion
        centro = [0, 0] #ubica el centro de la circunferencia en el origen
    distancia = (xx - centro[0])**2 + (yy - centro[1])**2 #calculamos la distancia desde el centro de la circunferencia a cada punto
    mascara = np.where(distancia <= radio**2, opacidad, 0) #los puntos de la mascara seran los puntos cuya distancia al centro es menor que el radio
    return mascara #devolvemos los puntos que cumplen la condicion para hacer parte de la mascara

def funcion_Rectangulo(base, altura, centro, xx, yy): #funcion para realizar una funcion rectangulo
    '''
    Crea una máscara con un rectángulo
    ENTRADAS:
        base == float (Base obviamente)
        altura == float (Altura obviamente)
        centro == lista [X,Y]
        xx, yy == malla de puntos en la cual se verá el rectángulo
    RETORNO:
        Mascara (Array 2D)    
    '''
    if centro is None: #que es lo que pasa si no se especifica el centro del rectangulo
        centro = [0, 0] #el centro se ubicca por defecto en el origen
    x_Min = centro[0] - base / 2 #calculos de las distancias limite del rectangulo
    x_Max = centro[0] + base / 2
    y_Min = centro[1] - altura / 2
    y_Max = centro[1] + altura / 2

    mascara = (xx <= x_Max) & (xx >= x_Min) & (yy <= y_Max) & (yy >= y_Min) #filtrado de los puntos al interior del rectangulo 

    return mascara #retorno la mascara

def producto_EspacioFrecuencia (intervalo, resolucion): #funcion que saca los intervalos relativos al producto espacio frecuencia y devuelve los deltas de espacio y de frecuencia
    ''' 
    Funcion que retorna los delta espacio y delta frecuencia para un muestreo particular
    ENTRADAS:
        intervalo == longitud fisica del intervalo del arreglo
        resolucion == numero de puntos que tiene la malla del arreglo
    RETORNA:
        Diccionario que contiene los deltas, para acceder:
        deltas["Delta_X"] - para acceder al delta espacial
        deltas["Delta_F"] - para acceder al delta frecuencial
    '''
    
    deltax = intervalo / resolucion #calculo del delta de espacio
    deltaf = 1 / (deltax *resolucion) #calculo del delta de frecuencias usando el producto espacio-frecuencias
    deltas = {"Delta_X": deltax, "Delta_F": deltaf} #agregamos los deltas a una lista
    return deltas #retornamos el diccionario con los deltas

def producto_EspacioFrecuenciaFresnel (longitud_Onda, distancia_Propagacion, intervalo, resolucion): #Calculo del producto espacio frecuencia en transformada de fresnel
    ''' Hay que hacer una modificacion al producto espacio frecuencia cuando se usa transformada de fresnel, debido a que por este metodo hay que adaptar 
        el kernel de fresnel, de modo que se parezca a un kernel de fourier y poder usar DFT's, de hecho, al usar una sola transforrmada de fourier, 
        este producto solo involucra distancias del plano de salida y de llegada, por lo tanto seria un producto espacio-espacio '''
    
    delta_Salida = intervalo / resolucion #calculamos el delta espacio del plano de salida
    delta_Llegada = (longitud_Onda * distancia_Propagacion) / (resolucion * delta_Salida) #calculamos el delta espacio del plano de llegada

    deltas = {"delta_Salida": delta_Salida, "delta_Llegada": delta_Llegada} #ponemos ambos deltas en un diccionario
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
def img_to_array(ruta):
    '''
    Convierte una imagen preferiblemente en escala de grises en un array
    de intensidades normalizadas
    Entradas:
        ruta == ruta de la imagen
    RETORNA:
        array de intensidades
    '''
    array_grises = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)   #lee el array, asignando un valor de intensidad de gris a cada pixel
    array_intensidades = array_grises / 255                 #normaliza el valor de intensidad
    return  array_intensidades

def random_Pinholes(no_Pinholes, radio , xx, yy , random_Phase = False):
    '''
    Funcion que crea una malla de pinholes distribuidos aleatoriamente
    ENTRADA:
        No_Pinholes == int      Cantidad de pinholes deseados
        tamaño      == float    Tamaño de los pinholes
        xx, yy      == meshgrid
        random_Phase== Boolean  True si se desea incluir fase aleatoria
    RETONRA
        Mascara
    '''
    mascara = np.zeros_like(xx, dtype = np.complex128)  # Inicializamos la máscara con ceros
    mascara_aux = np.zeros_like(xx, dtype = np.complex128)  # Máscara auxiliar para detectar superposiciones
    longitud_fisica = xx[0][-1]- xx[0][0]
    if random_Phase == False:
        for pinhole in range(no_Pinholes):
            while True:
                # Generar centro aleatorio
                centro_x = random.uniform(-longitud_fisica/2, longitud_fisica/2)
                centro_y = random.uniform(-longitud_fisica/2, longitud_fisica/2)
                centro_Pinholes = [centro_x, centro_y]

                # Crear el pinhole temporalmente
                pinhole_temp = funcion_Circulo(radio, centro_Pinholes, xx, yy)

                # Verificar si hay superposición con agujeros anteriores
                if np.sum(pinhole_temp * mascara_aux) == 0:
                    # Si no hay superposición, agregar el pinhole a la máscara
                    mascara += pinhole_temp
                    mascara_aux += pinhole_temp
                    break  # Salir del bucle while
    else:
        for pinhole in range(no_Pinholes):
            while True:
                # Generar centro aleatorio
                centro_x = random.uniform(-longitud_fisica/2, longitud_fisica/2)
                centro_y = random.uniform(-longitud_fisica/2, longitud_fisica/2)
                fase = np.exp(1j * random.uniform(0, 2*np.pi))
                
                centro_Pinholes = [centro_x, centro_y]

                # Crear el pinhole temporalmente
                pinhole_temp = funcion_Circulo(radio, centro_Pinholes, xx, yy, fase)

                # Verificar si hay superposición con agujeros anteriores
                if np.sum(pinhole_temp * mascara_aux) == 0:
                    # Si no hay superposición, agregar el pinhole a la máscara
                    mascara += pinhole_temp
                    mascara_aux += pinhole_temp
                    break  # Salir del bucle while
    return mascara

def rejilla_AperturasCuadradas(no_rectangulos_por_mm, ventana, xx, yy):
    '''
    Crea una máscara con una rejilla de aperturas cuadradas utilizando la función funcion_Rectangulo.

    ENTRADAS:
        no_rectangulos_por_mm == Número de rectángulos por milímetro.
        ventana == Tamaño total de la ventana en milímetros.
        xx, yy  == Malla de puntos.

    RETORNA:
        Máscara numérica con la rejilla de aperturas
    '''

    # Calcular el tamaño de cada rectángulo en unidades de la malla
    longitud_lado = 0.5 * 1 / (no_rectangulos_por_mm*1000) 
    # Crear una máscara vacía
    mascara = np.zeros_like(xx, dtype=float)

    # Calcular el número de rectángulos por fila y columna
    num_rectangulos = int(ventana * no_rectangulos_por_mm * 1000)

    # Crear los centros de los rectángulos
    centros_x = np.linspace(-ventana/2+2*longitud_lado, ventana/2-2*longitud_lado, num_rectangulos)
    centros_y = np.linspace(-ventana/2+2*longitud_lado, ventana/2-2*longitud_lado , num_rectangulos)

    # Crear la máscara iterando sobre los centros y utilizando funcion_Rectangulo
    for x in centros_x:
        for y in centros_y:
            # Obtener la máscara del rectángulo
            rectangulo_mascara = funcion_Rectangulo(longitud_lado, longitud_lado, [x, y], xx, yy)
            # Sumar la máscara del rectángulo a la máscara total
            mascara += rectangulo_mascara
    return mascara

def resize_with_pad(image: np.array, 
                    new_shape: Tuple[int, int], 
                    padding_color: Tuple[int] = (255, 255, 255)) -> np.array:
    """Maintains aspect ratio and resizes with padding.
    Params:
        image: Image to be resized.
        new_shape: Expected (width, height) of new image.
        padding_color: Tuple in BGR of padding color
    Returns:
        image: Resized image with padding
    """
    original_shape = (image.shape[1], image.shape[0])
    ratio = float(max(new_shape))/max(original_shape)
    new_size = tuple([int(x*ratio) for x in original_shape])
    image = cv2.resize(image, new_size)
    delta_w = new_shape[0] - new_size[0]
    delta_h = new_shape[1] - new_size[1]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)
    image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=padding_color)
    return image