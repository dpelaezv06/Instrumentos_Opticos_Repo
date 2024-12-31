'''En este archivo se deben poner todas las interfases necesarias para la obtención
de la matriz ABCD final del sistema Óptico de interés, se trata de una única función
en la cuál usted debe poner manualmente lo que necesite paso a paso, luego, obtendrá
los parámetros de interés en un diccionario'''

from Matrices_ABCD import *

#Parametros de al ubicación del objeto:
Distancia_Objeto = 200 #mm
n_objeto = 1
n_imagen = 1

def Formacion_imagenes(Distancia_Objeto , n_objeto, n_imagen):
    Matriz_Sistema = Matriz_inicial()   #Matriz identidad para empezar a trabajar
    
    '''En esta sección irán sus interfases, ingreselas en la lista:'''  
    #####################################################
    Interfases=[
        Refraccion(1.628, 1, 1.6116),
        Traslacion_entre_vertices(0.357,1.6116),
        Refraccion(-27.57 , 1.6116 , 1),
        Traslacion_entre_vertices(0.189 , 1),
        Refraccion(-3.457 , 1 , 1.6053),
        Traslacion_entre_vertices(0.081 , 1.6053),
        Refraccion(1.582 , 1.6053 , 1),
        Traslacion_entre_vertices(0.325 , 1),
        Refraccion("inf", 1 , 1.5123),
        Traslacion_entre_vertices(0.217 , 1.5123),
        Refraccion(1.920 , 1.5123 , 1.6116),
        Traslacion_entre_vertices(0.396 , 1.6116),
        Refraccion(-2.394 , 1.6116 , 1)
    ]
    #####################################################
    
    for i in Interfases:                    #Este ciclo sirve para calcular la matriz del sistema
        Matriz_Sistema = i @ Matriz_Sistema #Pura multiplicación matricial   
        
    '''Ahora, recogemos los parámetros necesarios de la matriz del sistema'''
    Poder_Sistema = - Matriz_Sistema[0,1]
    Distancia_H_V = (n_objeto/Matriz_Sistema[0,1]) * (1-Matriz_Sistema[0,0])                    # Desde el plano principal H hasta el primer vértice V  ; HV
    Distancia_H_prima_V_prima = (n_imagen/Matriz_Sistema[0,1]) * (1 - Matriz_Sistema[1,1])      # Desde el plano principal H' hasta el último vértice V'; H'V'
    Distancia_Objeto_H = Distancia_Objeto - Distancia_H_V                                       # Desde el objeto hasta el plano principal H            ; OH
    Distancia_H_prima_Imagen = n_imagen/(Poder_Sistema-(n_objeto/Distancia_Objeto_H))           # Desde el plano H' hasta la imagen                     ; H'I
    Magnificacion_Lateral = - Distancia_Objeto_H / Distancia_H_prima_Imagen                     # m_x
    Magnificacion_Angular = - n_objeto/n_imagen * Distancia_H_prima_Imagen/Distancia_Objeto_H   # m_alfa
    Distancia_Vertice_Imagen = Distancia_H_prima_V_prima + Distancia_H_prima_Imagen             # Desde el último vértice hasta la imágen               ; V'I
    
    '''Aclaración, la teoría de planos principales toma en cuenta un par de planos que simulan una lente delgada, por lo tanto,
    toda teoría en la que se usen lentes delgadas es válida sobre los planos principales, mucho ojo porque los planos están
    separados, no unidos'''
    
    Propiedades_Sistema = {"Distancia_H_V":Distancia_H_V,"Distancia_H_prima_V_prima":Distancia_H_prima_V_prima,
                           "Distancia_objeto_H":Distancia_Objeto_H, "Distancia_H_prima_imagen":Distancia_H_prima_Imagen,
                           "Magnificacion_lateral": Magnificacion_Lateral,"Magnificacion_angular ":Magnificacion_Angular,
                           "Distancia_vertice_imagen" : Distancia_Vertice_Imagen}
    
    '''Este diccionario contiene todas las posibles variables de interés'''
    return Propiedades_Sistema

Propiedades = Formacion_imagenes(Distancia_Objeto,n_objeto,n_imagen)
print(Propiedades)