import Optica_Geometrica_Lentes.Matrices_ABCD as mat
import optics_library.mascaras as opt
import Optica_Geometrica_Lentes.formacion_ImagenLenteDelgada as tlen
import optics_library.graficas as graph

''' definicion de parametros del montaje experimental'''
#caracteristicas del montaje y la ilimunacion
longitud_Onda = 533E-9
foco_LenteAnterior = 500E-3
foco_LentePosterior = 100E-3
distancia_Adicional = foco_LentePosterior
diametro_Diafragma = 100E-3

#calculo de las caracteristicas de cada sistema
propagacion_Entrada = [mat.propagacion(foco_LenteAnterior)]
sistema_Anterior = [mat.propagacion(foco_LenteAnterior), mat.lente_Delgada(foco_LenteAnterior)]
sistema_Posterior = [mat.propagacion(foco_LentePosterior), mat.lente_Delgada(foco_LentePosterior), mat.propagacion(distancia_Adicional)]

propiedad_PropagacionEntrada = mat.sistema_Optico(propagacion_Entrada, foco_LenteAnterior)
propiedad_SistemaAnterior = mat.sistema_Optico(sistema_Anterior, foco_LenteAnterior)
propiedad_SistemaPosterior = mat.sistema_Optico(sistema_Posterior, distancia_Adicional)

#caracteristicas del sensor y parametros de muestreo... Pueden depender del sensor
pixeles_X = 2448
pixeles_Y = 2048
tamano_Pixel = 3.45E-6
longitud_SensorX = pixeles_X * tamano_Pixel
longitud_SensorY = pixeles_Y * tamano_Pixel


#calculo de ventana en el espacio de muestreo del diafragma
muestreo_Diafragma = opt.muestreo_SegunSensorFresnel(pixeles_X, longitud_SensorX, propiedad_SistemaPosterior["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, longitud_SensorY)
ancho_XVentanaDiafragma = muestreo_Diafragma["delta_XEntrada"] * pixeles_X
ancho_YVentanaDiafragma = muestreo_Diafragma["delta_YEntrada"] * pixeles_Y
malla_XDiafragma, malla_YDiafragma = opt.malla_Puntos(pixeles_X, ancho_XVentanaDiafragma, pixeles_Y, ancho_YVentanaDiafragma)

muestreo_Lente = opt.muestreo_SegunSensorFresnel(pixeles_X, ancho_XVentanaDiafragma, propiedad_SistemaAnterior["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, ancho_YVentanaDiafragma)
ancho_XVentanaLente = muestreo_Lente["delta_XEntrada"] * pixeles_X
ancho_YVentanaLente = muestreo_Lente["delta_YEntrada"] * pixeles_Y
malla_XLente, malla_YLente = opt.malla_Puntos(pixeles_X, ancho_XVentanaLente, pixeles_Y, ancho_YVentanaLente)
muestreo_Objeto = opt.muestreo_SegunSensorFresnel(pixeles_X, ancho_XVentanaLente, propiedad_PropagacionEntrada["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, ancho_YVentanaLente)
ancho_XVentanaObjeto = muestreo_Objeto["delta_XEntrada"] * pixeles_X
ancho_YVentanaObjeto = muestreo_Objeto["delta_YEntrada"] * pixeles_Y
malla_XObjeto, malla_YObjeto = opt.malla_Puntos(pixeles_X, ancho_XVentanaDiafragma, pixeles_Y, ancho_YVentanaDiafragma)

''' creacion del objeto '''
ancho_FiltroHorizontal = 450E-6
ancho_FiltroVertical = 450E-6
lado = 390E-6
mascara = opt.img_to_array("images/Ruido_E04.png")
mascara = opt.resize_with_pad(mascara, [2448, 2048])


campo_Lente = tlen.imagen_Sistema(propiedad_PropagacionEntrada, mascara, ancho_XVentanaLente, pixeles_X, ancho_YVentanaLente, pixeles_Y, longitud_Onda)
diafragma_Campo = opt.funcion_Circulo(diametro_Diafragma/2, None, malla_YDiafragma, malla_YDiafragma)
campo_LenteTamanoFinito = campo_Lente * diafragma_Campo
campo_Anterior = tlen.imagen_SistemaShift(propiedad_SistemaAnterior, campo_LenteTamanoFinito, ancho_XVentanaDiafragma, pixeles_X, ancho_YVentanaDiafragma, pixeles_Y, longitud_Onda)
#filtro = opt.funcion_GaussianaSimetrica(ancho_Filtro, malla_XDiafragma, malla_YDiafragma)
filtro = opt.funcion_Rectangulo(lado, lado, [-1.243E-3,0.254E-3], malla_XDiafragma, malla_YDiafragma)
filtro |= opt.funcion_Rectangulo(lado, lado, [-0.403-3, 0.280E-3],malla_XDiafragma,malla_YDiafragma)
filtro |= opt.funcion_Rectangulo(lado, lado, [0.435E-3, 0.228E-3],malla_XDiafragma,malla_YDiafragma)
filtro |= opt.funcion_Rectangulo(lado, lado, [-0.403E-3, -0.192E-3],malla_XDiafragma,malla_YDiafragma)
filtro |= opt.funcion_Rectangulo(lado, lado, [0.435E-3, -0.245E-3],malla_XDiafragma,malla_YDiafragma)
filtro |= opt.funcion_Rectangulo(lado, lado, [1.281E-3, -0.216E-3],malla_XDiafragma,malla_YDiafragma)
filtro |= opt.funcion_Rectangulo(lado, lado, [-0.406E-3, 0.279E-3],malla_XDiafragma,malla_YDiafragma)
filtro = opt.invertir_Array(filtro)
campo_AnteriorDiafragma = campo_Anterior * filtro

campo_Salida = tlen.imagen_SistemaShift(propiedad_SistemaPosterior, campo_AnteriorDiafragma, longitud_SensorX, pixeles_X, longitud_SensorY, pixeles_Y, longitud_Onda)

#graph.intensidad(mascara, ancho_XVentanaObjeto, ancho_YVentanaObjeto, 1, 1)
#graph.intensidad(campo_LenteTamanoFinito, ancho_XVentanaLente, ancho_YVentanaLente, 1, 1)
#graph.intensidad(campo_Anterior,ancho_XVentanaDiafragma, ancho_YVentanaDiafragma, 1, 0.00001)
#graph.intensidad(filtro, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma)
#graph.intensidad(campo_AnteriorDiafragma, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma, 1, 0.00001)
graph.intensidad(campo_Salida, longitud_SensorX, longitud_SensorY, 1, 1)

