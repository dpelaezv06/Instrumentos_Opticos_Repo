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
    matriz[1,0] = -(n_Transmitido - n_Incidente)/ infinity(radio)  # Creamos la matriz refracción como debe ser
    '''
    | 1  0 |    
    | -P 1 |
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
    matriz[1,0] = 2*n_Medio / infinity(radio) #Se asigna el valor correspondiente al índice de la matriz
    '''
    | 1         0 |    
    | 2*n_i/R   1 |
    '''  
    return matriz

'''Matriz de Traslacion entre vértices'''
def traslacion_EntreVertices(distancia, n_Medio):
    '''
    Función para calcular la matriz correspondiente a una traslación
    ENTRADAS:
        n_medio   == float 
        distancia == float
    RETORNA:
        Matriz que da cuenta de la traslación entre vértices
    '''
    matriz = matriz_Inicial()           #Se crea matriz identidad para empezar a trabajar
    matriz[0,1] = distancia/ n_Medio    #Se asigna el valor adecuado en la posición correspondiente
    ''' MATRIZ RESULTANTE:
    |1   D/n|
    |0    1 |
    '''
    return matriz

'''Matriz de traslación objeto - vértice'''
def traslacion_ObjetoVertice(distancia, n_Medio):
    '''
    Funcion para calcular la transferencia entre el objeto y el primer vértice
    ENTRADAS:
        distancia == float
        n_medio   == float
    RETORNA:
        Matriz que da cuenta de la transferencia
    '''
    matriz = matriz_Inicial()             #Se crea matriz identidad para empezar a trabajar
    matriz[0,1] = distancia / n_Medio     #Se asigna el valor adecuado en la posición correspondiente
    return matriz

'''Matriz de una lente delgada'''
def lente_Delgada(radio_1, radio_2, n_Incidente, n_Lente, n_Salida, tamaño_Fisico = None):
    '''
    Función para calcular la matriz ABCD de un lente delgado
    ENTRADAS:
        radio_1     == float si finito, str si infinito
        radio_2     == float si finito, str si infinito
        n_Incidente == float, por default es 1 (aire)
        n_Lente     == float, por default es 1.5 (vidrio)
        n_Salida    == float, por default es 1 (aire)
    RETORNA:
        Matriz ABCD correspondiente
    '''

    ''' Definicion de valores por default para los indices de refraccion, se asume por default que la lente esta hecha de vidrio y que esta 
    inmersa en el aire
    Por tanto:
    n_Incidente = 1 por default
    n_Lente = 1.5 por default
    n_Salida = 1 por default'''
    if n_Incidente is None: #establecemos un valor por default para los indices de refraccion
        n_Incidente = 1 #si no se define, entonces el indice de refraccion es el del aire
    if n_Salida is None: #Establecemos un valor por default para el indice de refraccion de salida
        n_Salida = 1 #Si no se define, entonces el indice de refraccion de salida es el del aire
    if n_Lente is None: #establecemos un valor por default para el indice de refraccion de los lentes en caso de que se deje vacio
        n_Lente = 1.5 #Asumimos por default que las lentes estan hechas de vidrio
    
    matriz = matriz_Inicial()              #Se crea matriz identidad para empezar a trabajar
    poder_Lente = ((n_Lente - n_Incidente)/infinity(radio_1)) + ((n_Salida - n_Lente)/infinity(radio_2)) #se calcula el poder de covergencia de la lente usando la ecuacion del fabricante de lentes
    matriz[1,0] = -poder_Lente
    '''
    |1                0  | Poder_lente = 1/f
    |Poder_lente      1  |
    '''
    return matriz
