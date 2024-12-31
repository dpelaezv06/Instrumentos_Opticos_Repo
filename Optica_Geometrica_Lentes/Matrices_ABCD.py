'''En este código se almacena todo lo relacionado con las matrices ABCD para sistemas ópticos complejos
Se utiliza la teoría de planos principales para simplificar los procesos.
Tomar en cuenta que se usa la siguiente notación:
| n * theta |
|     x     |
Para simbolizar los rayos
'''

import numpy as np

'''Funcion para el caso de radios infinitos'''
def infinity(radio):
    try:
        radio = float(radio)        #Intenta transformar el radio a un float
        return radio
    except:
        return np.inf       #Si el usuario pone algo como inf, entonces se hace infinito (Sirve para cualquier str)

'''Matriz de Entrada del sistema'''
def matriz_Inicial():
    return np.eye(2)        #Se crea una matriz identidad para inciar a trabajar

'''Matriz de Refracción'''
def refraccion(radio, n_Incidente, n_Transmitido):
    '''
    Función para calcular la matriz correspondiente a una interfase que se refracta
    ENTRADAS:
        radio         == float (si es finito), str (si se quiere un infinito)
        n_Incidente   == float
        n_Transmitido == float
        Todas estas son propiedades físicas de la interfase
    RETORNA:
        Matriz correspondiente a la transformación que genera la interfase
    '''
    matriz = matriz_Inicial()                           # Creamos una matriz arbitraria para empezar a meter datos, fíjese que es identidad para facilitar las cosas
    matriz[0,1] = -(n_Transmitido - n_Incidente)/ infinity(radio)  # Creamos la matriz refracción como debe ser
    '''
    | 1 -P |    
    | 0  1 |
    '''
    #Donde P es el poder de la interfas, P = (n_transmitido - n_incidente)/Radio
    return matriz

'''Matriz de Reflexión'''
def reflexion(radio, n_Medio):
    '''
    Función para calcular la matriz correspondiente a un interfase que refleja
    ENTRADAS:
        radio   == float (si es finito), str (si se quiere un infinito), tome en cuenta que debe estar con el signo adecuado dependiendo de la concavidad
        n_Medio == float 
        Todas estas son propiedades físicas de la interfase
    RETORNA:
        Matriz correspondiente a la transformación que genera la interfase
    '''
    matriz = matriz_Inicial()         #Se crea matriz identidad para empezar a trabajar
    matriz[0,1] = 2*n_Medio / infinity(radio) #Se asigna el valor correspondiente al índice de la matriz
    '''
    | 1 2*n_i/R |    
    | 0     1   |
    '''  
    return matriz

'''Matriz de Traslacion entre vértices'''
def Traslacion_EntreVertices(distancia, n_Medio):
    '''
    Función para calcular la matriz correspondiente a una traslación
    ENTRADAS:
        n_medio   == float 
        distancia == float
    RETORNA:
        Matriz que da cuenta de la traslación entre vértices
    '''
    matriz = matriz_Inicial()           #Se crea matriz identidad para empezar a trabajar
    matriz[1,0] = distancia/ n_Medio    #Se asigna el valor adecuado en la posición correspondiente
    '''
    |1   0|
    |D/n 1|
    '''
    return matriz

'''Matriz de traslación objeto - vértice'''
def Traslacion_objetoVertice(distancia, n_Medio):
    '''
    Funcion para calcular la transferencia entre el objeto y el primer vértice
    ENTRADAS:
        distancia == float
        n_medio   == float
    RETORNA:
        Matriz que da cuenta de la transferencia
    '''
    matriz = matriz_Inicial()             #Se crea matriz identidad para empezar a trabajar
    matriz[1,0] = distancia / n_Medio     #Se asigna el valor adecuado en la posición correspondiente
    return matriz

'''Matriz de una lente delgada'''
def lente_Delgada(radio_1, radio_2 , n_Incidente, n_Lente, n_Salida, tamaño_Fisico = None):
    '''
    Función para calcular la matriz ABCD de un lente delgado
    ENTRADAS:
        radio_1     == float si finito, str si infinito
        radio_2     == float si finito, str si infinito
        n_Incidente == float
        n_Lente     == float
        n_Salida    == float
    RETORNA:
        Matriz ABCD correspondiente
    '''
    matriz = matriz_Inicial()              #Se crea matriz identidad para empezar a trabajar
    poder_Lente = ((n_Lente - n_Incidente)/infinity(radio_1)) + ((n_Salida - n_Lente)/infinity(radio_2))
    matriz[0,1] = -poder_Lente
    '''
    |1  Poder_lente | Poder_lente = 1/f
    |0       1      |
    '''
    return matriz