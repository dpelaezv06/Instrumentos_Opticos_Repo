import Optica_Geometrica_Lentes.Matrices_ABCD as mat
import optics_library.mascaras as opt
import Optica_Geometrica_Lentes.formacion_ImagenLenteDelgada as tlen
import optics_library.graficas as graph
import numpy as np

''' definicion de parametros del montaje experimental'''
#caracteristicas del montaje y la ilimunacion
longitud_Onda = 533E-9
foco_LenteAnterior = 20E-3
foco_LentePosterior = 200E-3
distancia_Adicional = foco_LentePosterior
diametro_Diafragma = 10.328E-3


#calculo de las caracteristicas de cada sistema
sistema_Anterior = [mat.propagacion(foco_LenteAnterior), mat.lente_Delgada(foco_LenteAnterior), mat.propagacion(foco_LenteAnterior)]
sistema_Posterior = [mat.propagacion(foco_LentePosterior), mat.lente_Delgada(foco_LentePosterior), mat.propagacion(distancia_Adicional)]

propiedad_SistemaAnterior = mat.sistema_Optico(sistema_Anterior, foco_LenteAnterior)
propiedad_SistemaPosterior = mat.sistema_Optico(sistema_Posterior, distancia_Adicional)

#caracteristicas del sensor y parametros de muestreo... Pueden depender del sensor
pixeles_X = 2848
pixeles_Y = 2848
tamano_Pixel = 2.74E-6
longitud_SensorX = pixeles_X * tamano_Pixel
longitud_SensorY = pixeles_Y * tamano_Pixel


#calculo de ventana en el espacio de muestreo del diafragma
muestreo_Diafragma = opt.muestreo_SegunSensorFresnel(pixeles_X, longitud_SensorX, propiedad_SistemaPosterior["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, longitud_SensorY)
ancho_XVentanaDiafragma = muestreo_Diafragma["delta_XEntrada"] * pixeles_X
ancho_YVentanaDiafragma = muestreo_Diafragma["delta_YEntrada"] * pixeles_Y
malla_XDiafragma, malla_YDiafragma = opt.malla_Puntos(pixeles_X, ancho_XVentanaDiafragma, pixeles_Y, ancho_YVentanaDiafragma)

muestreo_Objeto = opt.muestreo_SegunSensorFresnel(pixeles_X, ancho_XVentanaDiafragma, propiedad_SistemaAnterior["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, ancho_YVentanaDiafragma)
ancho_XVentanaObjeto = muestreo_Objeto["delta_XEntrada"] * pixeles_X
ancho_YVentanaObjeto = muestreo_Objeto["delta_YEntrada"] * pixeles_Y
malla_XObjeto, malla_YObjeto = opt.malla_Puntos(pixeles_X, ancho_XVentanaObjeto, pixeles_Y, ancho_YVentanaObjeto)


''' creacion del objeto '''

mascara = opt.img_to_array("images\\USAF-1951.png") 
mascara = opt.resize_with_pad(mascara, [2848, 2848])
#mascara = opt.funcion_Circulo(0.25E-6,None,malla_XObjeto,malla_YObjeto)
diafragma = opt.funcion_Circulo(diametro_Diafragma/2, None, malla_XDiafragma, malla_YDiafragma)

campo_Anterior = tlen.imagen_Sistema(propiedad_SistemaAnterior, mascara, ancho_XVentanaDiafragma, pixeles_X, ancho_YVentanaDiafragma, pixeles_Y, longitud_Onda)
campo_AnteriorDiafragma = campo_Anterior * diafragma

campo_Salida = tlen.imagen_SistemaShift(propiedad_SistemaPosterior, campo_AnteriorDiafragma, longitud_SensorX, pixeles_X, longitud_SensorY, pixeles_Y, longitud_Onda)

graph.intensidad(mascara, ancho_XVentanaObjeto, ancho_YVentanaObjeto)
#graph.intensidad(campo_Anterior, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma, 0, 0.00001)
#graph.intensidad(diafragma, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma)
#graph.intensidad(campo_AnteriorDiafragma, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma, 0, 0.00001)
graph.intensidad(campo_Salida, longitud_SensorX, longitud_SensorY)
