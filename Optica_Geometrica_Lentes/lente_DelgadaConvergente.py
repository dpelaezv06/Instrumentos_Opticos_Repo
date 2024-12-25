from Modelos_Difraccion import diffraction_library as diff
import numpy as np
import matplotlib.pyplot as plt

''' En este archivo se pondrán las funciones propias de la lente convergente se usaran los eleemetos propios de la lente (radios de cada cara y 
    material) para caracterizar la funcion de transmitancia propia de la lente '''

def Lente_NoParaxial(campo_Entrada, longitud_Onda, delta_X, radio_Anterior, radio_Posterior, grosor_Central, material, opacidad):
    ''' esta funcion devuelve el campo optico a la salida de una lente delgada convergente sin la aproximacion paraxial, se considera que la lente es
        de extension infinita, por tanto hay que definir el diafragma de la lente antes de usar esta funcion 
        
        Parametros:
        - campo_Entrada: Campo optico en la entrada de la lente, es decir, amplitud y fase punto a punto sobre el plano de la lente
        - radio_Anterior: Radio de curvatura de la cara anterior a la lente
        - longitud_Onda: longitud de onda de la iluminacion incidente
        - radio_Posterior: Radio de curvatura de la cara posterior de la lente
        - delta_X: El paso los puntos en el producto espacio frecuencia correspondiente al campo optico de entrada
        - Grosor_Central: Grosor de la lente en el eje optico (si no se ingresa se pone un cero por defecto)
        - material: Indice de refraccion del material de la lente (si no se ingresa un valor por defecto pone 1.5, asumiendo vidrio)
        - opacidad: Factor de transmision de la lente, (0 completamente opaca, 1 completamente translucida), si no se ingresa valor por defecto pone
          1, asumiendo una leente completamente transparente
          
        Retorna: Campo optico en la salida de la lente'''
    
    ''' definicion de los parametros por defecto en caso de que no se especifiquen '''
    if grosor_Central is None: #si no se pone un valor en el grosor central
        grosor_Central = 0 #se asume que es completamente nulo
    
    if material is None: #si no se especifica el material de la lente
        material = 1.5 #se asume el indice de refraccion del vidrio
    
    if opacidad is None: #si no se define un factor de atenuacion de amplitud
        opacidad = 1 #se asume que la lente es completamente translucida

    ''' Definicion de las coordenadas y las mallas de puntos que usaremos para realizar los calculos de transferencia '''
    resolucion_X, resolucion_Y = campo_Entrada.shape #resolucion del campo de entrada (tamano de la matriz 2d del campo de entrada)
    extension_X = resolucion_X * delta_X #calculo de los pasos de cada punto en la lente considerando las dimensiones del campo optico en la entrada
    extension_Y = resolucion_Y * delta_X #calculo de los pasos de cada punto en la lente considerando las dimensiones del campo optico en la entrada
    malla_X = np.linspace(-extension_X /2, extension_X /2) #creacion de la malla de puntos 1d para el eje x de las coordenadas de la lente
    malla_Y = np.linspace(-extension_Y /2, extension_Y /2) #creacion de la malla de puntos 1d para el eje y de las coordenadas de la lente
    malla_XX, malla_YY =  np.meshgrid(malla_X, malla_Y) #creacion de la malla de puntos 2d para las coordenadas de la lente

    ''' calculo de las funciones de grosor '''
    grosor_Anterior = radio_Anterior * (1 - np.sqrt(1 - (malla_XX **2 + malla_YY **2) / (radio_Anterior **2))) #calculo del grosor anterior de la lente
    grosor_Posterior = radio_Posterior * (1 - np.sqrt(1 - (malla_XX **2 + malla_YY **2) / (radio_Posterior **2))) #calculo del grosor posterior de la lente
    grosor_Lente = grosor_Central - grosor_Anterior + grosor_Posterior #calculo del grosor total de la lente punto a punto

    numero_Onda = 2 * np.pi / longitud_Onda #numero de onda de la iluminacion incidente sobre la lente
    transmitancia_Lente = opacidad * np.exp(1j * numero_Onda * grosor_Central) * np.exp(1j * numero_Onda * (material-1) * grosor_Lente) #calculamos la transmitancia de la lente
    campo_Salida = campo_Entrada * transmitancia_Lente #calculamos el campo de salida
    
    return campo_Salida #retornamos el campo de salida

def lente_Convergente(campo_Entrada, longitud_Onda, delta_X, foco, opacidad):
        ''' esta funcion devuelve el campo optico a la salida de una lente delgada convergente en aproximacion paraxial, se considera que la lente es
        de extension infinita, por tanto hay que definir el diafragma de la lente antes de usar esta funcion 
        
        Parametros:
        - campo_Entrada: Campo optico en la entrada de la lente, es decir, amplitud y fase punto a punto sobre el plano de la lente
        - longitud_Onda: longitud de onda de la iluminacion incidente
        - delta_X: El paso los puntos en el producto espacio frecuencia correspondiente al campo optico de entrada
        - foco: distancia focal de la lente
        - opacidad: Factor de transmision de la lente, (0 completamente opaca, 1 completamente translucida), si no se ingresa valor por defecto pone
          1, asumiendo una leente completamente transparente
          
        Retorna: Campo optico en la salida de la lente'''



