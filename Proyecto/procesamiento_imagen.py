import numpy as np
from scipy.ndimage import shift

def desplazar_imagen(imagen, x_min, x_max, y_min, y_max, distancia, angulo):
    """
    Desplaza un mapa de intensidad en una dirección y una distancia

    Parámetros:
    - imagen: matriz 2D representando el mapa de alturas
    - x_min, x_max: float, límites físicos en la dirección X (metros)
    - y_min, y_max: float, límites físicos en la dirección Y (metros)
    - distancia: float, distancia del desplazamiento en metros
    - angulo: float, ángulo en grados

    Retorna:
    - imagen_desplazada: np.ndarray, el mapa de alturas desplazado.
    """

    filas, columnas = imagen.shape #extraemos el tamano de la imagen en pixeles 

    pixel_x = (x_max - x_min) / columnas #asignamos un tamano fisico a la imagen
    pixel_y = (y_max - y_min) / filas

    desplazamiento_x = distancia * np.cos(np.pi * angulo / 180) / pixel_x #se convierte la distancia de desplazamiento en pixeles
    desplazamiento_y = -distancia * np.sin(np.pi * angulo / 180) / pixel_y #es necesario que sea negativo, porque al tratarse de una matriz, el numero del pixel crece hacia abajo

    imagen_desplazada = shift(imagen, shift=(desplazamiento_y, desplazamiento_x), mode='constant', cval=0, order=0) #desplazamos la imagen y rellenamos los vacios con cero

    return imagen_desplazada #retornamos la imagen desplazada 


def distancia_desplazamiento