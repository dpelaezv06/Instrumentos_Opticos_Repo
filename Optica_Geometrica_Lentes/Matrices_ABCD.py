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
        return radio                #En caso de que lo logre, entonces se ha ingresado un numero, y retornamos dicho numero
    except:                         #En caso contrario, el radio es infinito
        return np.inf               #Si el usuario pone algo como inf, entonces se hace infinito (Sirve para cualquier str)

''' Matriz de Entrada del sistema '''
def matriz_Inicial():
    matriz_Identidad = np.eye(2)        #Se crea una matriz identidad para inciar a trabajar
    return matriz_Identidad             #Retornamos una matriz identidad 2x2 para realizar las matrices de transferencia de rayos

''' Matriz de Refracción '''
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

    ''' Asignacion de valores por default'''
    matriz = matriz_Inicial()                           # Creamos una matriz arbitraria para empezar a meter datos, fíjese que es identidad para facilitar las cosas
    matriz[1,0] = -(n_Transmitido - n_Incidente)/ infinity(radio)  # Creamos la matriz refracción
    '''
    | 1    0 |    
    | -P   1 |    Donde P es el poder de la interfase, P = (n_transmitido - n_incidente)/Radio
    '''
    return matriz #retornamos la matriz construida

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


    ''' valores por default para facilitar las cosas '''
    if n_Medio is None:             #Valor por default para el indice del medio en el cual se produce la reflexion
        n_Medio = 1                 #Si no se pone ningun valor, se asume que el espejo esta en el aire
    if radio is None:               #Si el radio de curvatura esta vacio
        radio = infinity("Inf")     #Se asume entonces que el espejo es plano

    matriz = matriz_Inicial()                   #Se crea matriz identidad para empezar a trabajar
    matriz[1,0] = 2*n_Medio / infinity(radio)   #Se asigna el valor correspondiente al índice de la matriz
    '''
    | 1         0 |    
    | 2*n_i/R   1 |
    '''
    return matriz

'''Matriz de Traslacion entre vértices'''
def propagacion(distancia, n_Medio = 1):
    '''
    Función para calcular la matriz correspondiente a una traslación
    ENTRADAS:
        n_medio   == float 
        distancia == float
    RETORNA:
        Matriz que da cuenta de la propagacion en un medio de indice de refraccion n
    '''
    matriz = matriz_Inicial()               #Se crea matriz identidad para empezar a trabajar
    matriz[0,1] = distancia / n_Medio       #Se asigna el valor del camino optico en la posición correspondiente
    ''' MATRIZ RESULTANTE:
    |1   d/n|
    |0    1 |
    '''
    return matriz 

def foco_LenteDelgada(radio_1, radio_2, n_Incidente, n_Lente, n_Salida,):
    ''' Funcion que calcula la distancia focal de una lente delgada considerando sus caracteristicas fisicas 
    ENTRADAS:
    - radio_1: Radio de curvatura de la primera superficie
    - radio_2: Radio de curvatura de la segunda superficie
    - n_Incidente: indice de refraccion del medio anterior a la lente
    - n_Lente: Indice de refraccion del lente (depende del material)
    - n_Salida: Indice de refraccion del medio posterior a la lente
    
    RETORNA: Distancia focal de la lente con las caracteristicas ingresadas '''


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

    poder_Lente = ((n_Lente - n_Incidente)/infinity(radio_1)) + ((n_Salida - n_Lente)/infinity(radio_2)) #se calcula el poder de covergencia de la lente usando la ecuacion del fabricante de lentes
    distancia_Focal = 1/poder_Lente #calculamos la distancia focal usando el poder de la lente
    return distancia_Focal #retornamos la distancia focal


'''Matriz de una lente delgada'''
def lente_Delgada(distancia_Focal, diametro = np.inf ):
    '''
    Función para calcular la matriz ABCD de un lente delgado
    ENTRADAS:
        distancia_Focal == float
        tamano_Fisico == float
    RETORNA:
        Matriz ABCD correspondiente '''
    
    matriz = matriz_Inicial()               #Se crea matriz identidad para empezar a trabajar
    poder_Lente = 1/distancia_Focal         #Se calcula el poder de la lente usando la distancia focal
    matriz[1,0] = -poder_Lente              #Introducimos el valor correspondiente en la matriz de la lente
    '''
    |1                0  | Poder_lente = 1/f
    |Poder_lente      1  |
    '''
    diccionario = {"matriz":matriz,"diametro":diametro}
    return diccionario #retornamos la matriz

def sistema_Optico(interfases, distancia_Objeto, n_Objeto = 1, n_Imagen = 1):
    '''
    Esta función se debe modificar para el sistema óptico que requiera implementar, esto con el fin de evitar la necesidad
    de digitar todo el tiempo lo que se requiera.
    En el archivo encontrará  una sección en donde se deben acomodar las interfases en el órden estándar de un
    sistema óptico; izquierda a derecha.
    ENTRADAS:
        - interfases: Lista con las diferentes matrices de cada una de las etapas del sistema en el orden en el cual ocurren
        - distancia_Objeto == float 
        - n_Objeto         == float, 1 por defecto
        - n_Imagen         == float, 1 por defecto
    RETORNA:
        diccionario con las variables de interes, se accede con:
        "magnificacion_Lateral"         : magnificacion lateral del sistema entero
        "magnificacion_Angular"         : magnificacion angular del sistema entero
        "distancia_Imagen"              : distancia a la cual se forma la imagen del sistema
        "foco_sistema"                  : distancia focal del sistema
        "matriz_Sistema"                : matriz de transferencia de rayos del sistema completo
        "camino_EjeOptico"              : camino optico a lo largo del eje optico (El rayo que pasa derecho)
    '''
    
    matriz_Sistema = matriz_Inicial()   #Matriz identidad para empezar a trabajar
    camino_OpticoEje = 0                #Se crea una variable para guardar el camino optico a lo largo del eje optico del sistema

    #####################################################
    
    for elemento in interfases:                     #Este ciclo sirve para calcular la matriz del sistema
        if type(elemento) == dict:    
            camino_OpticoEje += elemento["matriz"][0,1]          #Sumamos el camino optico a través del eje optico
            matriz_Sistema = matriz_Sistema @ elemento["matriz"] #Multiplicacion matricial para obtener la matriz del sistema
        else:
            camino_OpticoEje += elemento[0,1]           #Sumamos el camino optico a través del eje optico
            matriz_Sistema = matriz_Sistema @ elemento  #Multiplicacion matricial para obtener la matriz del sistema
            
    '''Ahora, recogemos los parámetros necesarios de la matriz del sistema'''
    
    poder_Sistema = - matriz_Sistema[1,0]
    foco_Sistema = 1/poder_Sistema
    distancia_PlanoPrincipalVerticeEntrada = (n_Objeto/matriz_Sistema[1,0]) * (1-matriz_Sistema[0,0])                          # Desde el plano principal H hasta el primer vértice V  ; HV
    distancia_PlanoPrincipalVerticeSalida = (n_Imagen/matriz_Sistema[1,0]) * (1 - matriz_Sistema[1,1])                         # Desde el plano principal H' hasta el último vértice V'; H'V'
    distancia_ObjetoPlanoPrincipalEntrada = distancia_Objeto - distancia_PlanoPrincipalVerticeEntrada                          # Desde el objeto hasta el plano principal H            ; OH
    distancia_PlanoPrincipalSalidaImagen = n_Imagen/(poder_Sistema-(n_Objeto/distancia_ObjetoPlanoPrincipalEntrada))           # Desde el plano H' hasta la imagen                     ; H'I
    magnificacion_Lateral = - distancia_ObjetoPlanoPrincipalEntrada / distancia_PlanoPrincipalSalidaImagen                     # m_x
    magnificacion_Angular = - n_Objeto/n_Imagen * distancia_PlanoPrincipalSalidaImagen/distancia_ObjetoPlanoPrincipalEntrada   # m_alfa
    distancia_VerticeImagen = distancia_PlanoPrincipalVerticeSalida + distancia_PlanoPrincipalSalidaImagen                     # Desde el último vértice hasta la imágen               ; V'I


    
    '''Este diccionario contiene todas las posibles variables de interés'''
        
    propiedades_Sistema = {"magnificacion_Lateral": magnificacion_Lateral,
                           "magnificacion_Angular":magnificacion_Angular,
                           "distancia_Imagen" : distancia_VerticeImagen,
                           "foco_Sistema": foco_Sistema,
                           "matriz_Sistema": matriz_Sistema,
                           "camino_EjeOptico": camino_OpticoEje}
    return propiedades_Sistema
