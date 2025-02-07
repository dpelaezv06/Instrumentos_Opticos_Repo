'''Este archivo es ajeno a la entrega 2 de instrumentos ópticos, es simplemente un complemento a la entrega de Óptica de Fourier'''

import numpy as np
import optics_library.mascaras as opt
import optics_library.graficas as graph
import Optica_Geometrica_Lentes.Matrices_ABCD as mat
import Optica_Geometrica_Lentes.formacion_ImagenLenteDelgada as tlen


##############################################################################################
'''Se empieza definiendo los parámetros para la simulación'''
foco_lente = 500E-3 #mm                 #Distancia focal del lente
tamaño_lente = 200E-3 #mm               #Tamaño físico de la lente
distancia_imagen = foco_lente           #La imagen se sitúa a la distancia focal de la lente
distancia_LenteMascara = 450E-3 #mm     #Distancia entre el lente y la máscara que en este caso está posicionada en la parte posterior del lente
distancia_objeto = foco_lente           #La luz se ubica en el foco de la lente para producir su transformada de Fourier en el siguiente foco
ventana = 500E-3 #mm                    #Tamaño de la ventana
No_Puntos = 2048                        #Cantidad de puntos de la ventana
lado = 100E-3 #mm                       #Lado para crear la luz sin modificar que ingresa
x_in , y_in = opt.malla_Puntos(No_Puntos,ventana)   #Meshgrid de puntitos

##############################################################################################
transmitancia = opt.img_to_array("images\Ciencias_Agrarias.jpg")
transmitancia = opt.resize_with_pad(transmitancia, [2048,2048])
'''fft_transmitancia = np.fft.fft2(transmitancia)
factor = 10000
ruido = factor*opt.funcion_Circulo(5E-3,[5E-3,5E-3],x_in,y_in)
#graph.intensidad(ruido,ventana,ventana)
fft_transmitancia_ruidosa = fft_transmitancia
#graph.intensidad(fft_transmitancia_ruidosa,ventana,ventana,0,0.00001)
fft_transmitancia_ruidosa = ruido + fft_transmitancia
graph.intensidad(np.fft.fftshift(fft_transmitancia_ruidosa),ventana,ventana,0,0.0000001)
transmitancia_ruidosa = np.fft.fft2(fft_transmitancia_ruidosa)
graph.intensidad(transmitancia_ruidosa,ventana,ventana)
'''
'''Ahora, se calcula la pupila de acuerdo a la posición donde se encuentre la máscara'''
#transmitancia= opt.funcion_Rectangulo(5E-2,5E-2,None,x_in,y_in)
radio_Pupila = (foco_lente-distancia_LenteMascara)*tamaño_lente/foco_lente          #Se calcula el área que ilumina la lente de acuerdo a la distancia que se ubica la máscara
pupila = opt.funcion_Circulo(radio_Pupila,None,x_in,y_in)                           #La pupila es un círculo de radio igual a la proyección de la lente en la máscara
imagen_foco = np.fft.fftshift(np.fft.fft2(transmitancia*pupila))
#graph.intensidad(imagen_foco,ventana,ventana,0,0.00001)

reconstruccion = np.fft.fft2(imagen_foco)

graph.intensidad(transmitancia,ventana,ventana)
graph.intensidad(imagen_foco,ventana,ventana,0,0.001)
graph.intensidad(reconstruccion,ventana,ventana,0,1)