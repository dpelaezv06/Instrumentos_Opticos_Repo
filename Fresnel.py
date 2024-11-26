import numpy as np
import matplotlib.pyplot as plt
import puntos_Mascaras as pts

def producto_EspacioFrecuencia (intervalo, resolucion):
    deltax = intervalo / resolucion #calculo del delta x
    deltaf = 1 / (deltax *resolucion) #calculo del delta de frecuencias usaando el producto espacio-frecuencias
    deltas = {("Delta_X", deltax), ("Delta_F", deltaf)} #agregamos los deltas a una lista
    return deltas #retornamos el diccionario con los deltas

