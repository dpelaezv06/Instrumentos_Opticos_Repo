import numpy as np
from scipy.ndimage import shift

def desplazar_imagen(imagen, x_min, x_max, y_min, y_max, distancia, angulo):
    """
    Desplaza un mapa de alturas en una dirección y magnitud especificadas.

    Parámetros:
    - mapa: np.ndarray, matriz 2D representando el mapa de alturas.
    - x_min, x_max: float, límites físicos en la dirección X (metros).
    - y_min, y_max: float, límites físicos en la dirección Y (metros).
    - distancia: float, distancia del desplazamiento en metros.
    - angulo: float, ángulo en grados (0° es hacia la derecha, 90° hacia arriba).

    Retorna:
    - mapa_desplazado: np.ndarray, el mapa de alturas desplazado.
    """
    # Tamaño de la imagen en píxeles
    filas, columnas = mapa.shape

    # Tamaño del pixel en metros
    pixel_x = (x_max - x_min) / columnas
    pixel_y = (y_max - y_min) / filas

    # Convertir distancia en píxeles
    desplazamiento_x = distancia * np.cos(np.radians(angulo)) / pixel_x
    desplazamiento_y = -distancia * np.sin(np.radians(angulo)) / pixel_y  # Negativo porque en NumPy el eje Y crece hacia abajo

    # Aplicar desplazamiento con interpolación de orden 0 (mantiene valores y rellena con ceros)
    mapa_desplazado = shift(mapa, shift=(desplazamiento_y, desplazamiento_x), mode='constant', cval=0, order=0)

    return mapa_desplazado


