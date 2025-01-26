import Optica_Geometrica_Lentes.Matrices_ABCD as mat
import optics_library.mascaras as opt
import Optica_Geometrica_Lentes.formacion_ImagenLenteDelgada as tlen
import optics_library.graficas as graph

''' definicion de parametros del montaje experimental'''
#caracteristicas del montaje y la ilimunacion
longitud_Onda = 533E-9
foco_LenteAnterior = 500E-3
foco_LentePosterior = foco_LenteAnterior
distancia_Adicional = foco_LentePosterior
diametro_Diafragma = 100E-3

ancho_FiltroHorizontal = 450E-6
ancho_FiltroVertical = 450E-6
lado = 390E-6

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

mascara = opt.img_to_array("images/Ruido_E04.png")
mascara = opt.resize_with_pad(mascara, [2448, 2048])

#filtro = opt.funcion_GaussianaSimetrica(ancho_Filtro, malla_XDiafragma, malla_YDiafragma)
filtro = opt.funcion_Rectangulo(lado, lado, [-1.243E-3,0.254E-3], malla_XDiafragma, malla_YDiafragma)
filtro |= opt.funcion_Rectangulo(lado, lado, [-0.403-3, 0.280E-3],malla_XDiafragma,malla_YDiafragma)
filtro |= opt.funcion_Rectangulo(lado, lado, [0.435E-3, 0.228E-3],malla_XDiafragma,malla_YDiafragma)
filtro |= opt.funcion_Rectangulo(lado, lado, [-0.403E-3, -0.192E-3],malla_XDiafragma,malla_YDiafragma)
filtro |= opt.funcion_Rectangulo(lado, lado, [0.435E-3, -0.245E-3],malla_XDiafragma,malla_YDiafragma)
filtro |= opt.funcion_Rectangulo(lado, lado, [1.281E-3, -0.216E-3],malla_XDiafragma,malla_YDiafragma)
filtro |= opt.funcion_Rectangulo(lado, lado, [-0.406E-3, 0.279E-3],malla_XDiafragma,malla_YDiafragma)
filtro = opt.invertir_Array(filtro)

campo_Anterior = tlen.imagen_Sistema(propiedad_SistemaAnterior, mascara, ancho_XVentanaDiafragma, pixeles_X, ancho_YVentanaDiafragma, pixeles_Y, longitud_Onda)
#filtro = 0.7*(opt.funcion_Anillo(radio_Filtro, diametro_Lente,None, malla_XDiafragma, malla_YDiafragma, opacidad_Filtro) * opt.funcion_CruzGaussiana(1.5E-3, 1.5E-3, malla_XDiafragma, malla_YDiafragma, None) * (opt.invertir_Array(opt.funcion_GaussianaSimetrica(150E-6, malla_XDiafragma, malla_YDiafragma))))+0.3
campo_AnteriorDiafragma = campo_Anterior * filtro

campo_Salida = tlen.imagen_SistemaShift(propiedad_SistemaPosterior, campo_AnteriorDiafragma, longitud_SensorX, pixeles_X, longitud_SensorY, pixeles_Y, longitud_Onda)

graph.intensidad(mascara, ancho_XVentanaObjeto, ancho_YVentanaObjeto)
graph.intensidad(campo_Anterior, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma, 0, 0.001)
graph.intensidad(filtro, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma)
graph.intensidad(campo_AnteriorDiafragma, ancho_XVentanaDiafragma, ancho_YVentanaDiafragma, 0, 0.001)
graph.intensidad(campo_Salida, longitud_SensorX, longitud_SensorY, 0.2 , 0.7)
