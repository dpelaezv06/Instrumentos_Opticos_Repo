''' Actividad 1 del Parcial de instrumentos ópticos '''
import Optica_Geometrica_Lentes.Matrices_ABCD as mat
import optics_library.mascaras as opt
import Optica_Geometrica_Lentes.formacion_ImagenLenteDelgada as tlen
import optics_library.graficas as graph
import numpy as np

''' definicion de parametros del montaje experimental'''
#caracteristicas del montaje y la ilimunacion
longitud_Onda = 533E-9
foco_LenteAnterior = 10E-3
foco_LentePosterior = 0.2
distancia_Adicional = foco_LentePosterior
radio_Filtro = 0.1E-3
diametro_Lente = 7E-3
opacidad_Filtro = 0

#calculo de las caracteristicas de cada sistema
sistema_Anterior = [mat.propagacion(foco_LenteAnterior), mat.lente_Delgada(foco_LenteAnterior), mat.propagacion(foco_LenteAnterior)]
sistema_Posterior = [mat.propagacion(foco_LentePosterior), mat.lente_Delgada(foco_LentePosterior), mat.propagacion(distancia_Adicional)]

propiedad_SistemaAnterior = mat.sistema_Optico(sistema_Anterior, foco_LenteAnterior)
propiedad_SistemaPosterior = mat.sistema_Optico(sistema_Posterior, distancia_Adicional)

#caracteristicas del sensor y parametros de muestreo... Pueden depender del sensor
pixeles_X = 2848
pixeles_Y = 2848
tamano_Pixel = 2.47E-6
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
mascara = opt.leer_CSV("images/MuestraBio_E04.csv")
mascara = opt.resize_withComplexPad(mascara, [2048, 2448]) 

'''Creación del filtro'''

filtro = (1 + np.exp(0.5j*np.pi)*opt.funcion_Circulo(radio_Filtro,None,malla_XDiafragma,malla_YDiafragma)) * opt.funcion_Circulo(diametro_Lente, None, malla_XDiafragma, malla_YDiafragma)
#graph.fase(filtro,ancho_XVentanaDiafragma,ancho_YVentanaDiafragma)

campo_Anterior = tlen.imagen_Sistema(propiedad_SistemaAnterior, mascara, ancho_XVentanaDiafragma, pixeles_X, ancho_YVentanaDiafragma, pixeles_Y, longitud_Onda)
campo_AnteriorDiafragma = campo_Anterior * filtro

campo_Salida = tlen.imagen_SistemaShift(propiedad_SistemaPosterior, campo_AnteriorDiafragma, longitud_SensorX, pixeles_X, longitud_SensorY, pixeles_Y, longitud_Onda)

#graph.intensidad(mascara, ancho_XVentanaObjeto , ancho_YVentanaObjeto)
#graph.fase(mascara, ancho_XVentanaObjeto, ancho_YVentanaObjeto)
#graph.intensidad(campo_Anterior, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma, 0, 0.00001)
#graph.intensidad(filtro, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma)
graph.fase(filtro, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma)
#graph.intensidad(campo_AnteriorDiafragma, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma, 0, 0.001)
#graph.intensidad(campo_Salida, longitud_SensorX, longitud_SensorY, 0.2 , 0.7)
