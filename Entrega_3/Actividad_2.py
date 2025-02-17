import Optica_Geometrica_Lentes.Matrices_ABCD as mat
import optics_library.mascaras as opt
import Optica_Geometrica_Lentes.formacion_ImagenLenteDelgada as tlen
import optics_library.graficas as graph
import Modelos_Difraccion.Transformada_Fresnel as diff
import numpy as np


''' definicion de parametros del montaje experimental'''
#caracteristicas del montaje y la ilimunacion
longitud_Onda = 632.8E-9
foco_LenteAnterior = 20E-3
foco_LentePosterior = 20E-3
distancia_Adicional = foco_LentePosterior
diametro_Diafragma = 3


#calculo de las caracteristicas de cada sistema
sistema_Anterior = [mat.propagacion(foco_LenteAnterior), mat.lente_Delgada(foco_LenteAnterior), mat.propagacion(foco_LenteAnterior)]
sistema_Posterior = [mat.propagacion(foco_LentePosterior), mat.lente_Delgada(foco_LentePosterior), mat.propagacion(distancia_Adicional)]

propiedad_SistemaAnterior = mat.sistema_Optico(sistema_Anterior, foco_LenteAnterior)
propiedad_SistemaPosterior = mat.sistema_Optico(sistema_Posterior, distancia_Adicional)

#caracteristicas del sensor y parametros de muestreo... Pueden depender del sensor
pixeles_X = 2448
pixeles_Y = 2048
tamano_Pixel = 3.45E-6
longitud_SensorX = pixeles_X * tamano_Pixel
longitud_SensorY = pixeles_Y * tamano_Pixel
coseno_directorX = -0.0627
coseno_directorY = 0.0398


#calculo de ventana en el espacio de muestreo del diafragma
muestreo_Diafragma = opt.muestreo_SegunSensorFresnel(pixeles_X, longitud_SensorX, propiedad_SistemaPosterior["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, longitud_SensorY)
ancho_XVentanaDiafragma = muestreo_Diafragma["delta_XEntrada"] * pixeles_X
ancho_YVentanaDiafragma = muestreo_Diafragma["delta_YEntrada"] * pixeles_Y
malla_XDiafragma, malla_YDiafragma = opt.malla_Puntos(pixeles_X, ancho_XVentanaDiafragma, pixeles_Y, ancho_YVentanaDiafragma)

muestreo_Objeto = opt.muestreo_SegunSensorFresnel(pixeles_X, ancho_XVentanaDiafragma, propiedad_SistemaAnterior["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, ancho_YVentanaDiafragma)
ancho_XVentanaObjeto = muestreo_Objeto["delta_XEntrada"] * pixeles_X
ancho_YVentanaObjeto = muestreo_Objeto["delta_YEntrada"] * pixeles_Y
malla_XObjeto, malla_YObjeto = opt.malla_Puntos(pixeles_X, ancho_XVentanaObjeto, pixeles_Y, ancho_YVentanaObjeto)


'''Las siguientes lineas son para extraer la informacion de fase del holograma'''

''' creacion del objeto '''
mascara = opt.read_tiff("images/Hologram.tiff")
mascara = opt.resize_with_pad(mascara, [2448, 2048]) * opt.onda_inclinada(coseno_directorX, coseno_directorY, malla_XObjeto, malla_YObjeto,longitud_Onda)
#mascara = opt.funcion_Circulo(0.25E-6,None,malla_XObjeto,malla_YObjeto)
diafragma = opt.funcion_Circulo(diametro_Diafragma/2, None, malla_XDiafragma, malla_YDiafragma)
filtro = opt.funcion_Circulo(6E-4,[-1.3E-3,8E-4], malla_XDiafragma, malla_YDiafragma) + opt.funcion_Circulo(6E-4, [1.2547E-3,-7.910E-4], malla_XDiafragma, malla_YDiafragma) 

campo_Anterior = tlen.imagen_Sistema(propiedad_SistemaAnterior, mascara, ancho_XVentanaDiafragma, pixeles_X, ancho_YVentanaDiafragma, pixeles_Y, longitud_Onda)
campo_AnteriorDiafragma = campo_Anterior * diafragma * filtro #filtramos los ordenes 1 y -1 correspondientes a los terminos de interferencia

campo_Salida = tlen.imagen_SistemaShift(propiedad_SistemaPosterior, campo_AnteriorDiafragma, longitud_SensorX, pixeles_X, longitud_SensorY, pixeles_Y, longitud_Onda)
'''Con el campo de salida calculamos la fase del objeto del holograma'''
fase_Salida = -np.arccos(campo_Salida/(np.max(np.abs(campo_Salida))))+np.sqrt(1+(coseno_directorX/longitud_Onda)**2+(coseno_directorY/longitud_Onda)**2)

'''Reconstruimos el holograma iluminando en la misma direccion en la cual fue creado y propagando la misma distancia con la cual fue creado'''
holograma = mascara*np.exp(1j*fase_Salida)* opt.onda_inclinada(coseno_directorX, coseno_directorY, malla_XObjeto, malla_YObjeto,longitud_Onda)
holograma = opt.resize_withComplexPad(holograma, [2448, 2448])

distancia_reconstruccion = 0.0858
reconstruccion = diff.transformada_Fresnel(holograma, ancho_XVentanaObjeto, distancia_reconstruccion, longitud_Onda)
#graph.intensidad(holograma, ancho_XVentanaObjeto, ancho_YVentanaObjeto)
#graph.fase(holograma, ancho_XVentanaObjeto, ancho_YVentanaObjeto)
delta_Salida = opt.producto_EspacioFrecuenciaFresnel(longitud_Onda, distancia_reconstruccion, ancho_XVentanaObjeto, 2448)
ancho_VentanaReconstruccion = delta_Salida["delta_Salida"]*2448


graph.intensidad(holograma, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma, 0, 0.6)
graph.intensidad(np.fft.fftshift(reconstruccion), ancho_VentanaReconstruccion, ancho_VentanaReconstruccion, 0, 0.2)
graph.fase(holograma, ancho_XVentanaObjeto, ancho_YVentanaObjeto)
