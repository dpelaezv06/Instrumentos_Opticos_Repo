import numpy as np
import optics_library.mascaras as opt
import optics_library.graficas as graph
import Matrices_ABCD as mat

def formacion_Imagen(mascara, ventana, foco, distancia_MascaraLente, distancia_LenteSensor,longitud_onda = 632.8E-9):
    '''
    Función que permite la formación de imágenes con lentes delgadas
    ENTRADAS:
        mascara == objeto
        ventana == longitud total física de la mascara
        foco == foco del sistema óptico
        distancia_MascaraLente == float
        distancia_LenteSensor == Distancia donde se quiere sensar la luz
        longitud_onda == float
    RETORNA:
        Campo óptico que representa la imagen formada
    '''
    numero_Onda = 2*np.pi/longitud_onda                 #Evidentemente
    resolucion = len(mascara)                           #Se obtiene la resolucion
    xx , yy = opt.malla_Puntos(resolucion, ventana)     #Se crea la malla de puntos espacial
    fx = xx/(longitud_onda*distancia_MascaraLente)      #Coordenada espectral fx
    fy = yy/(longitud_onda*distancia_MascaraLente)      #Coordenada espectral fy
    propagacacion_MascaraLente = np.exp(-1j * np.pi * longitud_onda *distancia_MascaraLente * (xx**2 +yy**2))   #El término que propaga el espectro
    campo_AnteriorLente = np.fft.ifft2(np.fft.fft2(mascara)*propagacacion_MascaraLente)                         #Campo Óptico incidente en la lente
    transmitancia_Lente = np.exp(-1j * numero_Onda/(2*foco)*(xx**2 + yy**2))                                    #Transmitancia de una lente delgada
    campo_PosteriorLente = campo_AnteriorLente * transmitancia_Lente                                            #Campo Óptico que sale de la lente
    fase_ParabolicaImagen = np.exp(1j * numero_Onda / (2*distancia_LenteSensor) * (fx**2 +fy**2))               #Fase parabólica; coordenadas imagen
    fase_ParabolicaObjeto = np.exp(1j * numero_Onda / (2*distancia_LenteSensor) * (xx**2 +yy**2))               #Fase parabólica; coordenadas objeto
    imagen_Formada = fase_ParabolicaImagen/(1j*longitud_onda*distancia_LenteSensor) * np.fft.fft2(campo_PosteriorLente*fase_ParabolicaObjeto)
    imagen_shifteada = np.fft.fftshift(imagen_Formada)
    return imagen_shifteada

def imagen_Geometrica(sistema, objeto, ventana_Objeto, resolucion, longitud_Onda):
    ''' Funcion que saca una prediccion de la imagen geometrica de un campo optico al pasar por un sistema
    ENTRADAS:
    - sistema: diccionario con las propiedades del sistema, proviene de la salida de la funcion "sistema_Optico" definida en el archivo matrices ABCD
    - objeto: campo optico a la entrada del sistema
    - ventana_Objeto: ancho de la ventana en el plano objeto
    - resolucion: Cantidad de muestras que se toma del objeto
    - longitud_Onda: Longitud de onda de la iluminacion
    
    RETORNA:
    Campo optico a la salida del sistema '''

    numero_Onda = (2*np.pi)/longitud_Onda #calculamos el numero de onda usando la longitud de onda
    malla_EntradaXX, malla_EntradaYY = opt.malla_Puntos(resolucion, ventana_Objeto) #Malla de puntos relativa al muestreo del objeto a la entrada del sistema
    deltas = opt.producto_EspacioFrecuenciaFresnel(longitud_Onda, sistema["matriz_Sistema"][0,1], ventana_Objeto, resolucion) #Aplicacion del producto espacio-frecuencia para obtener informacion de los anchos de las ventanas
    longitud_VentanaSalida = resolucion * deltas["delta_Llegada"] #calculamos la longitud de la ventana a la salida usando la resolucion y el producto espacio-frecuencia
    malla_SalidaXX, malla_SalidaYY = opt.malla_Puntos(resolucion, longitud_VentanaSalida) #malla de puntos correspondiente a las coordenadas del plano de salida del sistema
    fase_Constante = np.exp(1j*numero_Onda*sistema["camino_EjeOptico"]) #el termino de fase constante, relativo a la longitud de camino optico que recorre el rayo que pasa por el centro del sistema
    fase_ParabolicaEntrada = np.exp((1j*numero_Onda*sistema["matriz_Sistema"][0,0]*(malla_EntradaXX**2 + malla_EntradaYY**2))/(2*sistema["matriz_Sistema"][0,1])) #fase parabolica que se debe aplicar relativa a las coordenadas del sistema en la salida
    fase_ParabolicaSalida = np.exp((1j*numero_Onda*sistema["matriz_Sistema"][1,1]*(malla_SalidaXX**2 + malla_SalidaYY**2))/(2*sistema["matriz_Sistema"][0,1])) #fase parabolica que se debe aplicar relativa a las coordenadas del sistema en la entrada
    transformada_Fresnel = np.fft.fftshift(np.fft.fft2(objeto*fase_ParabolicaEntrada)) #calculamos la transformada de fourier modificada, de la transformada de fresnel
    campo_Salida = ((deltas["delta_Llegada"])**2)*fase_Constante*fase_ParabolicaSalida*transformada_Fresnel #calculamos el campo de salida multiplicando por las fases parabolicas y la transformada de fresnel 
    return campo_Salida #retornamos el campo a la salida del sistema


