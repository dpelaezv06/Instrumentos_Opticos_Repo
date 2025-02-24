import Optica_Geometrica_Lentes.Matrices_ABCD as mat
import optics_library.mascaras as opt
import Optica_Geometrica_Lentes.formacion_ImagenLenteDelgada as tlen
import optics_library.graficas as graph
import numpy as np

''' definicion de parametros del montaje experimental para la formacion de imagenes '''
longitud_Onda = 632.8E-9 #longitud de onda usada en la iluminacion
foco_objetivo = 50E-3 #distancia focal del objetivo de microscopio
foco_lenteTubo = 200E-3  #distancia focal de la lente de tubo
diametro_Diafragma = 6.03022E-3 #diametro de la pupila del objetivo de microscopio
frecuencia = 92E3


#calculo de las caracteristicas de cada sistema
sistema_objetivo = [mat.propagacion(foco_objetivo), mat.lente_Delgada(foco_objetivo), mat.propagacion(foco_objetivo)] #propiedades del sistema compuesto por el objetivo de microscopio
sistema_lenteTubo = [mat.propagacion(foco_lenteTubo), mat.lente_Delgada(foco_lenteTubo), mat.propagacion(foco_lenteTubo)] #propiedades del sistema compuesto por la lente de tubo

propiedad_sistemaObjetivo = mat.sistema_Optico(sistema_objetivo, foco_objetivo) #calculo de las propiedades del sistema conformado por la lente del objetivo
propiedad_sistemaLenteTubo = mat.sistema_Optico(sistema_lenteTubo, foco_lenteTubo) #calculo de las propiedades del sistema conformado por la lente de tubo

#caracteristicas del sensor y parametros de muestreo... Pueden depender del sensor
pixeles_X = 2448 #numero de pixeles puestos en el eje x
pixeles_Y = 2048 #numero de pixeles puestos en el eje y
tamano_Pixel = 3.45E-6 #tamano de los pixeles del detector
longitud_SensorX = pixeles_X * tamano_Pixel #calculo de las dimensiones fisicas del sensor en el eje x
longitud_SensorY = pixeles_Y * tamano_Pixel #calculo de las dimensiones fisicas del sensor en el eje y




''' sistema de formacion de imagenes '''
#calculo de ventana en el espacio de muestreo del diafragma
muestreo_Diafragma = opt.muestreo_SegunSensorFresnel(pixeles_X, longitud_SensorX, propiedad_sistemaLenteTubo["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, longitud_SensorY) #propiedades de muestreo del diafragma del sistema considerando las caracteristicas de registro del sensor
ancho_XVentanaDiafragma = muestreo_Diafragma["delta_XEntrada"] * pixeles_X #calculo de la ventana de muestreo del diafragma en el eje x
ancho_YVentanaDiafragma = muestreo_Diafragma["delta_YEntrada"] * pixeles_Y #calculo de la ventana de muestreo del diafragma en el eje y
malla_XDiafragma, malla_YDiafragma = opt.malla_Puntos(pixeles_X, ancho_XVentanaDiafragma, pixeles_Y, ancho_YVentanaDiafragma) #calculo de la malla de puntos que muestrea el diafragma

muestreo_Objeto = opt.muestreo_SegunSensorFresnel(pixeles_X, ancho_XVentanaDiafragma, propiedad_sistemaObjetivo["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, ancho_YVentanaDiafragma) #propiedades de muestreo del plano de la muestra del sistema considerando las caracteristicas de muestreo del diafragma
ancho_XVentanaObjeto = muestreo_Objeto["delta_XEntrada"] * pixeles_X #calculo de la ventana de muestreo de la muestra en el eje x
ancho_YVentanaObjeto = muestreo_Objeto["delta_YEntrada"] * pixeles_Y #calculo de la ventana de muestreo de la muestra en el eje y
malla_XObjeto, malla_YObjeto = opt.malla_Puntos(pixeles_X, ancho_XVentanaObjeto, pixeles_Y, ancho_YVentanaObjeto) #calculo de la malla de puntos que muestrea la muestra
ancho_filtro = 1.5E-3
filtro = opt.funcion_Rectangulo(ancho_filtro, diametro_Diafragma, None, malla_XDiafragma, malla_YDiafragma)
filtro = opt.invertir_Array(filtro)


''' calculo de la imagen '''
mascara = opt.img_to_array("images/USAF-1951.png")
mascara = opt.resize_with_pad(mascara, [2448, 2048])
mascaraH = mascara * 0.5*(1+np.cos(2*np.pi*malla_XObjeto*frecuencia))
diafragma = opt.funcion_Circulo(diametro_Diafragma/2, None, malla_XDiafragma, malla_YDiafragma)

campo_AnteriorH = tlen.imagen_Sistema(propiedad_sistemaObjetivo, mascaraH, ancho_XVentanaDiafragma, pixeles_X, ancho_YVentanaDiafragma, pixeles_Y, longitud_Onda)*filtro
campo_AnteriorDiafragmaH = campo_AnteriorH * diafragma
campo_SalidaH = tlen.imagen_SistemaShift(propiedad_sistemaLenteTubo, campo_AnteriorDiafragmaH, longitud_SensorX, pixeles_X, longitud_SensorY, pixeles_Y, longitud_Onda)

graph.intensidad(mascara, ancho_XVentanaObjeto, ancho_YVentanaObjeto)
graph.intensidad(campo_AnteriorH, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma, 0, 0.00001)
graph.intensidad(diafragma, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma)
graph.intensidad(campo_AnteriorDiafragmaH, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma, 0, 0.00001)
graph.intensidad(campo_SalidaH, longitud_SensorX, longitud_SensorY)

''' calculo de la imagen '''
mascaraV = mascara * 0.5*(1+np.cos(2*np.pi*malla_YObjeto*frecuencia))
diafragma = opt.funcion_Circulo(diametro_Diafragma/2, None, malla_XDiafragma, malla_YDiafragma)


campo_Anterior = tlen.imagen_Sistema(propiedad_sistemaObjetivo, mascaraV, ancho_XVentanaDiafragma, pixeles_X, ancho_YVentanaDiafragma, pixeles_Y, longitud_Onda)
campo_AnteriorDiafragma = campo_Anterior * diafragma
campo_Salida = tlen.imagen_SistemaShift(propiedad_sistemaLenteTubo, campo_AnteriorDiafragma, longitud_SensorX, pixeles_X, longitud_SensorY, pixeles_Y, longitud_Onda)
graph.intensidad(campo_Salida, longitud_SensorX, longitud_SensorY)

