import procesamiento_imagen as img
import numpy as np
import optics_library.mascaras as opt
import Optica_Geometrica_Lentes.formacion_ImagenLenteDelgada as tlen
import Optica_Geometrica_Lentes.Matrices_ABCD as mat
import optics_library.graficas as graph

longitud_Onda = 632.8E-9 #longitud de onda usada en la iluminacion
foco_lenteTubo = 200E-3  #distancia focal de la lente de tubo
foco_objetivo = 50E-3 #distancia focal del objetivo de microscopio
foco_lenteFourier = 150E-3
foco_posteriorIluminador = 40E-3
foco_anteriorIluminador = 100E-3
diametro_Diafragma = 6.03022E-3 #diametro de la pupila del objetivo de microscopio
ancho_franjaEspejos = 8
angulo = -45
pupila_sistetica = 0

lista_imagenes = []
lista_desplazamientos = []

frecuencia = img.frecuencia_muestra()
desplazamiento_0 = img.desplazamiento_frecuencia(frecuencia, 0, foco_objetivo)
desplazamiento_45 = img.desplazamiento_frecuencia(frecuencia, 45, foco_objetivo)
desplazamiento_90 = img.desplazamiento_frecuencia(frecuencia, 90, foco_objetivo)
desplazamiento_menos45 = img.desplazamiento_frecuencia(frecuencia, -45, foco_objetivo)

imagen0 = opt.img_to_array('Proyecto/Images/0_8_simulado.png')
imagen45 = opt.img_to_array('Proyecto/Images/45_8_simulado.png')
imagen90 = opt.img_to_array('Proyecto/Images/90_8_simulado.png')
imagen_menos45 = opt.img_to_array('Proyecto/Images/-45_8_simulado.png')

lista_imagenes = [imagen0, imagen45, imagen90, imagen_menos45]
lista_desplazamientos = [desplazamiento_0, desplazamiento_45, desplazamiento_90, desplazamiento_menos45]

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

espectro_imagen = 0

angulo = -45

pupila_original = opt.funcion_Circulo(diametro_Diafragma/2, None, malla_XspliterImagen, malla_YspliterImagen)
pupila_sistetica = pupila_original

angulo = -45
multiplo = 1.75
for iteracion in range(0, len(lista_imagenes)):
    angulo = angulo + 45
    fourier = np.fft.fftshift(np.fft.fft2(lista_imagenes[iteracion]))

    pupila_sisteticaMas = img.desplazar_imagen(pupila_original, -ancho_XventanaSpliterImagen/2, ancho_XventanaSpliterImagen/2, -ancho_YventanaSpliterImagen/2, ancho_YventanaSpliterImagen/2, lista_desplazamientos[iteracion], angulo + 90)
    pupila_sisteticaMenos = img.desplazar_imagen(pupila_original, -ancho_XventanaSpliterImagen/2, ancho_XventanaSpliterImagen/2, -ancho_YventanaSpliterImagen/2, ancho_YventanaSpliterImagen/2, -lista_desplazamientos[iteracion], angulo + 90)
    imagen_desplazadaMas = img.desplazar_imagen(fourier*pupila_sisteticaMas, -ancho_XventanaSpliterImagen/2, ancho_XventanaSpliterImagen/2, -ancho_YventanaSpliterImagen/2, ancho_YventanaSpliterImagen/2, -multiplo*lista_desplazamientos[iteracion], angulo + 90)
    imagen_desplazadaMenos = img.desplazar_imagen(fourier*pupila_sisteticaMenos, -ancho_XventanaSpliterImagen/2, ancho_XventanaSpliterImagen/2, -ancho_YventanaSpliterImagen/2, ancho_YventanaSpliterImagen/2, multiplo*lista_desplazamientos[iteracion], angulo + 90)
    espectro_imagen = espectro_imagen + imagen_desplazadaMas + imagen_desplazadaMenos
    #graph.intensidad_Logaritmica(fourier, ancho_XventanaSpliterImagen, ancho_YventanaSpliterImagen)
    #graph.intensidad_Logaritmica(imagen_desplazadaMas, ancho_XventanaSpliterImagen, ancho_YventanaSpliterImagen)
    #graph.intensidad_Logaritmica(imagen_desplazadaMenos, ancho_XventanaSpliterImagen, ancho_YventanaSpliterImagen)
    #graph.intensidad_Logaritmica(espectro_imagen, ancho_XventanaSpliterImagen, ancho_YventanaSpliterImagen)

angulo = 0
pupila_original = opt.funcion_Circulo(diametro_Diafragma/2, None, malla_XspliterImagen, malla_YspliterImagen)
for iteracion in range (0, len(lista_imagenes)):
    angulo = angulo + 45
    pupila_sistetica = pupila_sistetica | img.desplazar_imagen(pupila_original, -ancho_XventanaSpliterImagen/2, ancho_XventanaSpliterImagen/2, -ancho_YventanaSpliterImagen/2, ancho_YventanaSpliterImagen/2, lista_desplazamientos[iteracion], angulo)
    pupila_sistetica = pupila_sistetica | img.desplazar_imagen(pupila_original, -ancho_XventanaSpliterImagen/2, ancho_XventanaSpliterImagen/2, -ancho_YventanaSpliterImagen/2, ancho_YventanaSpliterImagen/2, -lista_desplazamientos[iteracion], angulo)

#graph.intensidad(pupila_original, ancho_XventanaSpliterImagen, ancho_YventanaSpliterImagen)
#graph.intensidad(pupila_sistetica, ancho_XventanaSpliterImagen, ancho_YventanaSpliterImagen)


graph.intensidad_Logaritmica(espectro_imagen, ancho_XventanaSpliterImagen, ancho_YventanaSpliterImagen)

imagen_reconstruida = np.fft.ifft2(espectro_imagen)
graph.intensidad(imagen_reconstruida, longitud_SensorX, longitud_SensorY, 0, 0.3)