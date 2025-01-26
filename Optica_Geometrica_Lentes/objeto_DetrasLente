'''Este archivo es ageno a la entrega 2 de instrumentos ópticos, es simplemente un complemento a la entrega de Óptica de Fourier'''

import numpy as np
import optics_library.mascaras as opt
import optics_library.graficas as graph
import Optica_Geometrica_Lentes.Matrices_ABCD as mat
import Optica_Geometrica_Lentes.formacion_ImagenLenteDelgada as tlen


##############################################################################################
foco_lente = 500E-3 #mm
tamaño_lente = 10E-3 #mm
distancia_imagen = foco_lente
distancia_LenteMascara = 100E-3 #mm
distancia_objeto = np.inf()
ventana = 50E-3 #mm
No_Puntos = 2048
lado = 100E-3 #mm   
x_in , y_in = opt.malla_Puntos(No_Puntos,ventana)
mascara = opt.funcion_Rectangulo(lado,lado,None,x_in,y_in)

##############################################################################################
interfases_TransferenciaPupila = [mat.propagacion(distancia_LenteMascara),mat.lente_Delgada(foco_lente)]
transferencia_Pupila = mat.sistema_Optico(interfases_TransferenciaPupila, distancia_objeto) 
tlen.imagen_Sistema(transferencia_Pupila, mascara,ventana,No_Puntos)