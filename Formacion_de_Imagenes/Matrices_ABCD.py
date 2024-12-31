'''En este código se almacena todo lo relacionado con las matrices ABCD para sistemas ópticos complejos
Se utiliza la teoría de planos principales para simplificar los procesos.
Tomar en cuenta que se usa la siguiente notación:
| n * theta |
|     x     |
Para simbolizar los rayos
'''

import numpy as np

'''Funcion para el caso de radios infinitos'''
def infinity(Radio):
    try:
        Radio = float(Radio)        #Intenta transformar el radio a un float
        return Radio
    except:
        return np.inf       #Si el usuario pone algo como inf, entonces se hace infinito (Sirve para cualquier str)

'''Matriz de Entrada del sistema'''
def Matriz_inicial():
    return np.eye(2)        #Se crea una matriz identidad para inciar a trabajar

'''Matriz de Refracción'''
def Refraccion(Radio, n_incidente, n_transmitido):
    '''
    Función para calcular la matriz correspondiente a una interfase que se refracta
    ENTRADAS:
        Radio         == float (si es finito), str (si se quiere un infinito)
        n_incidente   == float
        n_transmitido == float
        Todas estas son propiedades físicas de la interfase
    RETORNA:
        Matriz correspondiente a la transformación que genera la interfase
    '''
    Matriz = Matriz_inicial()                           # Creamos una matriz arbitraria para empezar a meter datos, fíjese que es identidad para facilitar las cosas
    Matriz[0,1] = -(n_transmitido - n_incidente)/ infinity(Radio)  # Creamos la matriz refracción como debe ser
    '''
    | 1 -P |    
    | 0  1 |
    '''
    #Donde P es el poder de la interfas, P = (n_transmitido - n_incidente)/Radio
    return Matriz

'''Matriz de Reflexión'''
def Reflexion(Radio, n_medio):
    '''
    Función para calcular la matriz correspondiente a un interfase que refleja
    ENTRADAS:
        Radio   == float (si es finito), str (si se quiere un infinito), tome en cuenta que debe estar con el signo adecuado dependiendo de la concavidad
        n_medio == float 
        Todas estas son propiedades físicas de la interfase
    RETORNA:
        Matriz correspondiente a la transformación que genera la interfase
    '''
    Matriz = Matriz_inicial()         #Se crea matriz identidad para empezar a trabajar
    Matriz[0,1] = 2*n_medio / infinity(Radio) #Se asigna el valor correspondiente al índice de la matriz
    '''
    | 1 2*n_i/R |    
    | 0     1   |
    '''  
    return Matriz

'''Matriz de Traslacion entre vértices'''
def Traslacion_entre_vertices(Distancia, n_medio):
    '''
    Función para calcular la matriz correspondiente a una traslación
    ENTRADAS:
        n_medio   == float 
        Distancia == float
    RETORNA
        Matriz que da cuenta de la traslación entre vértices
    '''
    Matriz = Matriz_inicial()           #Se crea matriz identidad para empezar a trabajar
    Matriz[1,0] = Distancia/ n_medio    #Se asigna el valor adecuado en la posición correspondiente
    '''
    |1   0|
    |D/n 1|
    '''
    return Matriz

'''Matriz de traslación objeto - vértice'''
def Traslacion_objeto_vertice(Distancia, n_medio):
    '''
    Funcion para calcular la transferencia entre el objeto y el primer vértice
    ENTRADAS:
        Distancia == float
        n_medio   == float
    RETORNA:
        Matriz que da cuenta de la transferencia
    '''
    Matriz = Matriz_inicial()             #Se crea matriz identidad para empezar a trabajar
    Matriz[1,0] = Distancia / n_medio     #Se asigna el valor adecuado en la posición correspondiente
    return Matriz

'''Matriz de una lente delgada'''
def Lente_delgada(Radio_1, Radio_2 , n_incidente, n_lente, n_salida, tamaño_fisico = None):
    '''
    Función para calcular la matriz ABCD de un lente delgado
    ENTRADAS:
        Radio_1     == float si finito, str si infinito
        Radio_2     == float si finito, str si infinito
        n_incidente == float
        n_lente     == float
        n_salida    == float
    RETORNA:
        Matriz ABCD correspondiente
    '''
    Matriz = Matriz_inicial()              #Se crea matriz identidad para empezar a trabajar
    Poder_Lente = ((n_lente-n_incidente)/infinity(Radio_1)) + ((n_salida-n_lente)/infinity(Radio_2))
    Matriz[0,1] = -Poder_Lente
    '''
    |1  Poder_lente | Poder_lente = 1/f
    |0       1      |
    '''
    return Matriz