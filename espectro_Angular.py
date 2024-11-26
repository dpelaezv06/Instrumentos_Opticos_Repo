''' CODIGO CON LAS FUNCIONES PARA CALCULAR DIFRACCION POR ESPECTRO ANGULAR 
Aca estan todas las funciones relativas a la difraccion por espectro angular  '''

''' LIBRERIAS USADAS EN EL CODIGO '''
import numpy as np #numpy para usar funciones matematicas
import scipy as sc #scipy para obtener constantes cientificas
import matplotlib.pyplot as plt #matplotlib para graficar funciones 

''' 1. Tomar el espectro de fourier de la fuente 
    2. Propago usando helmholtz 
    3. Saco la distribucion de campo optico usando Fourier inversa'''


''' FUNCIONES UTILES PARA SACAR FRECUENCIAS DEPENDIENDO DE LOS PARAMETROS DE MUESTREO ...

########################## CUIDADO!!!!! SOLO FUNCIONA CON VENTANAS CUADRADAS Y MUESTREOS UNIFORMES #######################'''


def frecuencias_Intervalos(intervalo, puntos, longitud_Onda): #funcion que retorna los datos de las frecuencias de muestreo de espacio y frecuencia usando el producto espacio-frecuencia
    deltas_Intervalos = {"delta_Desplazamiento", 0, #en este diccionario se almacenan los datos de delta espacio y frecuencia
                         "delta_Frecuencia", 0,
                         "longitud_Onda", 0}
    
    deltas_Intervalos["delta_Desplazamiento"] = (intervalo[1] - intervalo[0]) / puntos #calculo la frecuencia de muestreo en el espacio como dr = L/N
    deltas_Intervalos["delta_Frecuencia"] = 1 / (puntos * deltas_Intervalos["delta_Desplazamiento"]) #calculo la frecuencia de muestreo en las frecuencias usando el producto espacio-frecuencia dfdr=1/N
    deltas_Intervalos["longitud_Onda"] = longitud_Onda #almaceno la longitud de onda en el diccionario, es bueno ternerla en facil acceso por efectos practicos

    return deltas_Intervalos #devuelvo el diccionario con los deltas de cada muestreo en cada espacio y la longitud de onda para escalar todo

def espectro_Fuente (fuente): #funcion que calcula el espectro de fourier de una fuente 
    transformada = np.fft.fft2(fuente) #calculo el espectro
    espectro = np.fft.fftshift(transformada) #shifteo para que las frecuencias bajas me queden al centro
    return espectro # retorno el espectro

def espectro_Pantalla(espectro_Fuente, distancia, longitud_Onda, delta_F): 
        
    exponente = 1j * distancia * np.sqrt(1 - ((longitud_Onda * delta_F)**2) * )



