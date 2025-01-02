'''En este archivo se deben poner todas las interfases necesarias para la obtención
de la matriz ABCD final del sistema Óptico de interés, se trata de una única función
en la cuál usted debe poner manualmente lo que necesite paso a paso, luego, obtendrá
los parámetros de interés en un diccionario'''

from Matrices_ABCD import *

#Parametros de al ubicación del objeto:
distancia_Objeto = 200 #mm
n_Objeto = 1
n_Imagen = 1

def formacion_Imagenes(distancia_Objeto , n_Objeto = 1, n_Imagen = 1):
    '''
    Esta función se debe modificar para el sistema óptico que requiera implementar, esto con el fin de evitar la necesidad
    de digitar todo el tiempo lo que se requiera.
    En el archivo encontrará  una sección en donde se deben acomodar las interfases en el órden estándar de un
    sistema óptico; izquierda a derecha.
    ENTRADAS:
        distancia_Objeto == float 
        n_Objeto         == float, 1 por defecto
        n_Imagen         == float, 1 por defecto
    RETORNA:
        diccionario con las variables de interes, se accede con:
        "Magnificacion_lateral"
        "Magnificacion_angular"
        "Distancia_vertice_imagen"
        "foco_sistema"
        "Matriz_Sistema"
    '''
    
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
    
    poder_Sistema = - matriz_Sistema[1,0]
    foco_Sistema = 1/poder_Sistema
    distancia_PlanoPrincipalVerticeEntrada = (n_Objeto/matriz_Sistema[1,0]) * (1-matriz_Sistema[0,0])                          # Desde el plano principal H hasta el primer vértice V  ; HV
    distancia_PlanoPrincipalVerticeSalida = (n_Imagen/matriz_Sistema[1,0]) * (1 - matriz_Sistema[1,1])                         # Desde el plano principal H' hasta el último vértice V'; H'V'
    distancia_ObjetoPlanoPrincipalEntrada = distancia_Objeto - distancia_PlanoPrincipalVerticeEntrada                          # Desde el objeto hasta el plano principal H            ; OH
    distancia_PlanoPrincipalSalidaImagen = n_Imagen/(poder_Sistema-(n_Objeto/distancia_ObjetoPlanoPrincipalEntrada))           # Desde el plano H' hasta la imagen                     ; H'I
    magnificacion_Lateral = - distancia_ObjetoPlanoPrincipalEntrada / distancia_PlanoPrincipalSalidaImagen                     # m_x
    magnificacion_Angular = - n_Objeto/n_Imagen * distancia_PlanoPrincipalSalidaImagen/distancia_ObjetoPlanoPrincipalEntrada   # m_alfa
    distancia_VerticeImagen = distancia_PlanoPrincipalVerticeSalida + distancia_PlanoPrincipalSalidaImagen                    # Desde el último vértice hasta la imágen               ; V'I
    
    '''Este diccionario contiene todas las posibles variables de interés'''
        
    propiedades_Sistema = {"Magnificacion_lateral": magnificacion_Lateral,
                           "Magnificacion_angular":magnificacion_Angular,
                           "Distancia_vertice_imagen" : distancia_VerticeImagen,
                           "foco_sistema": foco_Sistema,
                           "Matriz_Sistema": matriz_Sistema}
    return propiedades_Sistema