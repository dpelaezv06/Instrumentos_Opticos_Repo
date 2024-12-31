'''En este archivo se deben poner todas las interfases necesarias para la obtención
de la matriz ABCD final del sistema Óptico de interés, se trata de una única función
en la cuál usted debe poner manualmente lo que necesite paso a paso, luego, obtendrá
los parámetros de interés en un diccionario'''

from Matrices_ABCD import *

#Parametros de al ubicación del objeto:
distancia_Objeto = 200 #mm
n_Objeto = 1
n_Imagen = 1

def formacion_Imagenes(distancia_Objeto , n_Objeto, n_Imagen):
    matriz_Sistema = matriz_Inicial()   #Matriz identidad para empezar a trabajar
    
    '''En esta sección irán sus interfases, ingreselas en la lista:'''  
    #####################################################
    interfases = [
        refraccion(1.628, 1, 1.6116),
        traslacion_EntreVertices(0.357,1.6116),
        refraccion(-27.57 , 1.6116 , 1),
        traslacion_EntreVertices(0.189 , 1),
        refraccion(-3.457 , 1 , 1.6053),
        traslacion_EntreVertices(0.081 , 1.6053),
        refraccion(1.582 , 1.6053 , 1),
        traslacion_EntreVertices(0.325 , 1),
        refraccion("inf", 1 , 1.5123),
        traslacion_EntreVertices(0.217 , 1.5123),
        refraccion(1.920 , 1.5123 , 1.6116),
        traslacion_EntreVertices(0.396 , 1.6116),
        refraccion(-2.394 , 1.6116 , 1)
    ]
    #####################################################
    
    for elemento in interfases:                    #Este ciclo sirve para calcular la matriz del sistema
        matriz_Sistema = elemento @ matriz_Sistema #Pura multiplicación matricial   
        
    '''Ahora, recogemos los parámetros necesarios de la matriz del sistema'''
    poder_Sistema = - matriz_Sistema[0,1]
    distancia_H_V = (n_Objeto/matriz_Sistema[0,1]) * (1-matriz_Sistema[0,0])                    # Desde el plano principal H hasta el primer vértice V  ; HV
    distancia_H_prima_V_prima = (n_Imagen/matriz_Sistema[0,1]) * (1 - matriz_Sistema[1,1])      # Desde el plano principal H' hasta el último vértice V'; H'V'
    distancia_Objeto_H = distancia_Objeto - distancia_H_V                                       # Desde el objeto hasta el plano principal H            ; OH
    distancia_H_prima_Imagen = n_Imagen/(poder_Sistema-(n_Objeto/distancia_Objeto_H))           # Desde el plano H' hasta la imagen                     ; H'I
    magnificacion_Lateral = - distancia_Objeto_H / distancia_H_prima_Imagen                     # m_x
    magnificacion_Angular = - n_Objeto/n_Imagen * distancia_H_prima_Imagen/distancia_Objeto_H   # m_alfa
    distancia_Vertice_Imagen = distancia_H_prima_V_prima + distancia_H_prima_Imagen             # Desde el último vértice hasta la imágen               ; V'I
    
    '''Aclaración, la teoría de planos principales toma en cuenta un par de planos que simulan una lente delgada, por lo tanto,
    toda teoría en la que se usen lentes delgadas es válida sobre los planos principales, mucho ojo porque los planos están
    separados, no unidos'''
    
    propiedades_Sistema = {"Distancia_H_V":distancia_H_V,"Distancia_H_prima_V_prima":distancia_H_prima_V_prima,
                           "Distancia_objeto_H":distancia_Objeto_H, "Distancia_H_prima_imagen":distancia_H_prima_Imagen,
                           "Magnificacion_lateral": magnificacion_Lateral,"Magnificacion_angular ":magnificacion_Angular,
                           "Distancia_vertice_imagen" : distancia_Vertice_Imagen}
    
    '''Este diccionario contiene todas las posibles variables de interés'''
    return propiedades_Sistema

Propiedades = formacion_Imagenes(distancia_Objeto, n_Objeto, n_Imagen)
print(Propiedades)