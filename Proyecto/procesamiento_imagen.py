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

def frecuencia_muestra(objetivo = 50E-3, lente_fourier = 150E-3, lente_posteriorIluminador = 40E-3, lente_anteriorIluminador = 100E-3, espejos = 7, tamano_espejo = 5.4E-6):
    periodo_espacial = 2 * (objetivo / lente_fourier) * (lente_posteriorIluminador / lente_anteriorIluminador) * espejos * tamano_espejo
    frecuencia_espacial = 1 / periodo_espacial
    return frecuencia_espacial

def desplazamiento_frecuencia(frecuencia, angulo, distancia_focal = 50E-3, longitud_onda = 632.8E-9):
    desplazamiento = frecuencia * longitud_onda * distancia_focal
    return desplazamiento
