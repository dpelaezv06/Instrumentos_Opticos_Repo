import Optica_Geometrica_Lentes.Matrices_ABCD as mat
import optics_library.mascaras as opt
import Optica_Geometrica_Lentes.formacion_ImagenLenteDelgada as tlen
import optics_library.graficas as graph
import procesamiento_imagen as img
import numpy as np

''' definicion de parametros del montaje experimental para la formacion de imagenes '''
longitud_Onda = 632.8E-9 #longitud de onda usada en la iluminacion
foco_lenteTubo = 200E-3  #distancia focal de la lente de tubo
foco_objetivo = 50E-3 #distancia focal del objetivo de microscopio
foco_lenteFourier = 200E-3
foco_posteriorIluminador = 50E-3
foco_anteriorIluminador = 50E-3
diametro_Diafragma = 6.03022E-3 #diametro de la pupila del objetivo de microscopio

#calculo de las caracteristicas de cada sistema
sistema_anteriorIluminador = [mat.propagacion(foco_anteriorIluminador), mat.lente_Delgada(foco_anteriorIluminador), mat.propagacion(foco_anteriorIluminador)] #primera etapa del sistema de demagnificacion del iluminador
sistema_posteriorIluminador = [mat.propagacion(foco_posteriorIluminador), mat.lente_Delgada(foco_posteriorIluminador), mat.propagacion(foco_posteriorIluminador)] #segunda etapa del sistema de demagnificacion del iluminador
sistema_transformadaFourier = [mat.propagacion(foco_lenteFourier), mat.lente_Delgada(foco_lenteFourier), mat.propagacion(foco_lenteFourier)] #en esta etapa se hace la transformada de fourier de los deltas generados por el dmd
sistema_objetivo = [mat.propagacion(foco_objetivo), mat.lente_Delgada(foco_objetivo), mat.propagacion(foco_objetivo)] #propiedades del sistema compuesto por el objetivo de microscopio
sistema_lenteTubo = [mat.propagacion(foco_lenteTubo), mat.lente_Delgada(foco_lenteTubo), mat.propagacion(foco_lenteTubo)] #propiedades del sistema compuesto por la lente de tubo

propiedad_sistemaAnteriorIluminador = mat.sistema_Optico(sistema_anteriorIluminador, foco_anteriorIluminador) #calculo de las propiedades del sistema compuesto por la primera lente del sistema de demagnificacion del iluminador
propiedad_sistemaPosteriorIluminador = mat.sistema_Optico(sistema_posteriorIluminador, foco_posteriorIluminador) #calculo de las propiedades del sistema compuesto por la segunda lente del sistema demagnificador del iluminador
propiedad_sistemaTransformadaFourier = mat.sistema_Optico(sistema_transformadaFourier, foco_lenteFourier) #propiedades del sistema conformado por la lente de fourier, la cual convierte el conjunto de deltas en un patron sinusoidal de intensidad
propiedad_sistemaObjetivo = mat.sistema_Optico(sistema_objetivo, foco_objetivo) #calculo de las propiedades del sistema conformado por la lente del objetivo
propiedad_sistemaLenteTubo = mat.sistema_Optico(sistema_lenteTubo, foco_lenteTubo) #calculo de las propiedades del sistema conformado por la lente de tubo

#caracteristicas del sensor y parametros de muestreo... Pueden depender del sensor
pixeles_X = 4000 #numero de pixeles puestos en el eje x
pixeles_Y = 3000 #numero de pixeles puestos en el eje y
tamano_Pixel = 1.85E-6 #tamano de los pixeles del detector
tamano_microespejo = 5.4E-6 #tamano fisico del cuadrado del arreglo de microespejos
longitud_SensorX = pixeles_X * tamano_Pixel #calculo de las dimensiones fisicas del sensor en el eje x
longitud_SensorY = pixeles_Y * tamano_Pixel #calculo de las dimensiones fisicas del sensor en el eje y


''' sistema de formacion de imagenes '''
muestreo_spliterImagen = opt.muestreo_SegunSensorFresnel(pixeles_X, longitud_SensorX, propiedad_sistemaLenteTubo["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, longitud_SensorY) #propiedades de muestreo del divisor de haz considerando las caracteristicas de registro del sensor
ancho_XventanaSpliterImagen = muestreo_spliterImagen["delta_XEntrada"] * pixeles_X #calculo de la ventana de muestreo del divisor de haz en la direccion de formacion de imagenes
ancho_YventanaSpliterImagen = muestreo_spliterImagen["delta_YEntrada"] * pixeles_Y #calculo de la ventana de muestreo del divisor de haz en la direccion de formacion de imagenes
malla_XspliterImagen, malla_YspliterImagen = opt.malla_Puntos(pixeles_X, ancho_XventanaSpliterImagen, pixeles_Y, ancho_YventanaSpliterImagen) #calculo de la malla de puntos que muestrea el divisor de haz en la direccion de formacion de imagenes

muestreo_muestra = opt.muestreo_SegunSensorFresnel(pixeles_X, ancho_XventanaSpliterImagen, propiedad_sistemaObjetivo["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, ancho_YventanaSpliterImagen) #propiedades de muestreo del plano de la muestra considerando las caracteristicas de muestreo del divisor de haz en la direccion de formacion de imagenes
ancho_XventanaMuestra = muestreo_muestra["delta_XEntrada"] * pixeles_X #calculo de la ventana de muestreo de la muestra en el eje x
ancho_YventanaMuestra = muestreo_muestra["delta_YEntrada"] * pixeles_Y #calculo de la ventana de muestreo de la muestra en el eje y
malla_Xmuestra, malla_Ymuestra = opt.malla_Puntos(pixeles_X, ancho_XventanaMuestra, pixeles_Y, ancho_YventanaMuestra) #calculo de la malla de puntos que muestrea la muestra

''' sistema de iluminacion '''
muestreo_spliterIluminador = opt.muestreo_SegunSensorFresnel(pixeles_X, ancho_XventanaMuestra, propiedad_sistemaObjetivo["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, ancho_YventanaMuestra) #propiedades de muestreo del plano del divisor de haz en la direccion del iluminador tenienddo el cuenta el muestreo sobre la muestra
ancho_XventanaSpliterIluminador = muestreo_spliterIluminador["delta_XEntrada"] * pixeles_X #calculo de la ventana de muestreo del spliter en direccion del iluminador en el eje x
ancho_YventanaSpliterIluminador = muestreo_spliterIluminador["delta_YEntrada"] * pixeles_Y #calculo de la ventana de muestreo del spliter en direccion del iluminador en el eje y
malla_XspliterIluminador, malla_YspliterIluminador = opt.malla_Puntos(pixeles_X, ancho_XventanaSpliterIluminador, pixeles_Y, ancho_YventanaSpliterIluminador) #calculo de la malla de puntos que muestrea el spliter en la direccion del iluminador

muestreo_patronDemagnificado = opt.muestreo_SegunSensorFresnel(pixeles_X, ancho_XventanaSpliterIluminador, propiedad_sistemaTransformadaFourier["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, ancho_YventanaSpliterIluminador) #propiedades de muestreo del plano del patron de iluminacion demagnificado considerando las caracteristicas de muestreo del spliter en direccion del iluminador
ancho_XventanaPatronDemagnificado = muestreo_patronDemagnificado["delta_XEntrada"] * pixeles_X #calculo de la ventana de muestreo de la muestra en el eje x
ancho_YventanaPatronDemagnificado = muestreo_patronDemagnificado["delta_YEntrada"] * pixeles_Y #calculo de la ventana de muestreo de la muestra en el eje y
malla_XpatronDemagnificado, malla_YpatronDemagnificado = opt.malla_Puntos(pixeles_X, ancho_XventanaPatronDemagnificado, pixeles_Y, ancho_YventanaPatronDemagnificado) #calculo de la malla de puntos que muestrea la muestra

muestreo_lenteAnteriorDemagnificador = opt.muestreo_SegunSensorFresnel(pixeles_X, ancho_XventanaPatronDemagnificado, propiedad_sistemaPosteriorIluminador["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, ancho_YventanaPatronDemagnificado) #propiedades de muestreo del plano del patron de iluminacion demagnificado considerando las caracteristicas de muestreo del spliter en direccion del iluminador
ancho_XventanaLenteAnteriorDemagnificador = muestreo_lenteAnteriorDemagnificador["delta_XEntrada"] * pixeles_X #calculo de la ventana de muestreo de la muestra en el eje x
ancho_YventanaLenteAnteriorDemagnificador = muestreo_lenteAnteriorDemagnificador["delta_YEntrada"] * pixeles_Y #calculo de la ventana de muestreo de la muestra en el eje y
malla_XlenteAnteriorDemagnificador, malla_YlenteAnteriorDemagnificador = opt.malla_Puntos(pixeles_X, ancho_XventanaLenteAnteriorDemagnificador, pixeles_Y, ancho_YventanaLenteAnteriorDemagnificador) #calculo de la malla de puntos que muestrea la muestra

muestreo_patronDMD = opt.muestreo_SegunSensorFresnel(pixeles_X, ancho_XventanaLenteAnteriorDemagnificador, propiedad_sistemaAnteriorIluminador["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, ancho_YventanaLenteAnteriorDemagnificador) #propiedades de muestreo del plano del patron de iluminacion demagnificado considerando las caracteristicas de muestreo del spliter en direccion del iluminador
ancho_XventanaPatronDMD = muestreo_patronDMD["delta_XEntrada"] * pixeles_X #calculo de la ventana de muestreo de la muestra en el eje x
ancho_YventanaPatronDMD = muestreo_patronDMD["delta_YEntrada"] * pixeles_Y #calculo de la ventana de muestreo de la muestra en el eje y
malla_XpatronDMD, malla_YpatronDMD = opt.malla_Puntos(pixeles_X, ancho_XventanaPatronDMD, pixeles_Y, ancho_YventanaPatronDMD) #calculo de la malla de puntos que muestrea la muestra


''' simulacion de las imagnes que obtiene el microscopio '''

''' sistema de iluminacion '''
lado_ordenesDifraccion = 5.4E-6 #longitud del lado de los cuadrados que componen el patron de difraccion del dmd usando en el sistema de iluminacion
posicion_primerOrden = 7E-3 #posicion de los primeros ordenes de difraccion 1 y -1 que genera el patron de difraccion del dmd, se usan para codificar la frecuencia del patron sinusoidal con el que se va a iluminar
patron_DMD = opt.rejilla_difraccion(tamano_microespejo, malla_XpatronDMD, malla_YpatronDMD)
campo_bloqueo = tlen.imagen_Sistema(propiedad_sistemaAnteriorIluminador, patron_DMD, ancho_XventanaLenteAnteriorDemagnificador, pixeles_X,  ancho_YventanaLenteAnteriorDemagnificador, pixeles_Y, longitud_Onda)
campo_iluminadorDemagnificado = tlen.imagen_SistemaShift(propiedad_sistemaPosteriorIluminador, campo_bloqueo, ancho_XventanaPatronDemagnificado, pixeles_X,  ancho_YventanaPatronDemagnificado, pixeles_Y, longitud_Onda)
campo_lenteFourier = tlen.imagen_SistemaShift(propiedad_sistemaTransformadaFourier, campo_iluminadorDemagnificado, ancho_XventanaSpliterIluminador, pixeles_X,  ancho_YventanaSpliterIluminador, pixeles_Y, longitud_Onda)
campo_muestra = tlen.imagen_SistemaShift(propiedad_sistemaObjetivo, campo_lenteFourier, ancho_XventanaMuestra, pixeles_X,  ancho_YventanaMuestra, pixeles_Y, longitud_Onda)
campo_espectroMuestra = tlen.imagen_SistemaShift(propiedad_sistemaObjetivo, campo_muestra, ancho_XventanaSpliterImagen, pixeles_X,  ancho_YventanaSpliterImagen, pixeles_Y, longitud_Onda)
campo_sensor = tlen.imagen_SistemaShift(propiedad_sistemaLenteTubo, campo_espectroMuestra, longitud_SensorX, pixeles_X,  longitud_SensorY, pixeles_Y, longitud_Onda)



graph.intensidad(patron_DMD, ancho_XventanaPatronDMD, ancho_YventanaPatronDMD)
graph.intensidad(campo_bloqueo, ancho_XventanaLenteAnteriorDemagnificador, ancho_YventanaLenteAnteriorDemagnificador)
graph.intensidad(campo_iluminadorDemagnificado, ancho_XventanaPatronDemagnificado, ancho_YventanaPatronDemagnificado)
graph.intensidad(campo_lenteFourier, ancho_XventanaSpliterIluminador, ancho_YventanaSpliterIluminador)
graph.intensidad(campo_muestra, ancho_XventanaMuestra, ancho_YventanaMuestra)

# ''' calculo de la imagen '''
# mascara = opt.img_to_array("images/USAF-1951.png")
# mascara = opt.resize_with_pad(mascara, [4000, 3000])
# diafragma = opt.funcion_Circulo(diametro_Diafragma/2, None, malla_XspliterImagen, malla_YspliterImagen)

# campo_Anterior = tlen.imagen_Sistema(propiedad_sistemaObjetivo, mascara, ancho_XVentanaDiafragma, pixeles_X, ancho_YVentanaDiafragma, pixelesq_Y, longitud_Onda)
# campo_AnteriorDiafragma = campo_AnteriorH * diafragma * filtroH
# campo_SalidaH = tlen.imagen_SistemaShift(propiedad_sistemaLenteTubo, campo_AnteriorDiafragmaH, longitud_SensorX, pixeles_X, longitud_SensorY, pixeles_Y, longitud_Onda)


# graph.intensidad(mascara, ancho_XVentanaObjeto, ancho_YVentanaObjeto)
# graph.intensidad(campo_AnteriorH, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma, 0, 0.001)
# graph.intensidad(campo_AnteriorDiafragmaH, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma, 0, 0.001)
# graph.intensidad(campo_SalidaH, longitud_SensorX, longitud_SensorY)
