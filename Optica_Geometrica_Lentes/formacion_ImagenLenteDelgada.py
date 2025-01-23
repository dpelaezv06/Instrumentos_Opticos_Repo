import numpy as np
import optics_library.mascaras as opt
import optics_library.graficas as graph
import Optica_Geometrica_Lentes.Matrices_ABCD as mat

def Lente_NoParaxial(campo_Entrada, longitud_Onda, delta_X, radio_Anterior, radio_Posterior, grosor_Central, material, opacidad):
    ''' esta funcion devuelve el campo optico a la salida de una lente delgada convergente sin la aproximacion paraxial, se considera que la lente es
        de extension infinita, por tanto hay que definir el diafragma de la lente antes de usar esta funcion 
        
        Parametros:
        - campo_Entrada: Campo optico en la entrada de la lente, es decir, amplitud y fase punto a punto sobre el plano de la lente
        - radio_Anterior: Radio de curvatura de la cara anterior a la lente
        - longitud_Onda: longitud de onda de la iluminacion incidente
        - radio_Posterior: Radio de curvatura de la cara posterior de la lente
        - delta_X: El paso los puntos en el producto espacio frecuencia correspondiente al campo optico de entrada
        - Grosor_Central: Grosor de la lente en el eje optico (si no se ingresa se pone un cero por defecto)
        - material: Indice de refraccion del material de la lente (si no se ingresa un valor por defecto pone 1.5, asumiendo vidrio)
        - opacidad: Factor de transmision de la lente, (0 completamente opaca, 1 completamente translucida), si no se ingresa valor por defecto pone
          1, asumiendo una leente completamente transparente
          
        Retorna: Campo optico en la salida de la lente'''
    
    ''' definicion de los parametros por defecto en caso de que no se especifiquen '''
    if grosor_Central is None: #si no se pone un valor en el grosor central
        grosor_Central = 0 #se asume que es completamente nulo
    
    if material is None: #si no se especifica el material de la lente
        material = 1.5 #se asume el indice de refraccion del vidrio
    
    if opacidad is None: #si no se define un factor de atenuacion de amplitud
        opacidad = 1 #se asume que la lente es completamente translucida

    ''' Definicion de las coordenadas y las mallas de puntos que usaremos para realizar los calculos de transferencia '''
    resolucion_X, resolucion_Y = campo_Entrada.shape #resolucion del campo de entrada (tamano de la matriz 2d del campo de entrada)
    extension_X = resolucion_X * delta_X #calculo de los pasos de cada punto en la lente considerando las dimensiones del campo optico en la entrada
    extension_Y = resolucion_Y * delta_X #calculo de los pasos de cada punto en la lente considerando las dimensiones del campo optico en la entrada
    malla_X = np.linspace(-extension_X /2, extension_X /2) #creacion de la malla de puntos 1d para el eje x de las coordenadas de la lente
    malla_Y = np.linspace(-extension_Y /2, extension_Y /2) #creacion de la malla de puntos 1d para el eje y de las coordenadas de la lente
    malla_XX, malla_YY =  np.meshgrid(malla_X, malla_Y) #creacion de la malla de puntos 2d para las coordenadas de la lente

    ''' calculo de las funciones de grosor '''
    grosor_Anterior = radio_Anterior * (1 - np.sqrt(1 - (malla_XX **2 + malla_YY **2) / (radio_Anterior **2))) #calculo del grosor anterior de la lente
    grosor_Posterior = radio_Posterior * (1 - np.sqrt(1 - (malla_XX **2 + malla_YY **2) / (radio_Posterior **2))) #calculo del grosor posterior de la lente
    grosor_Lente = grosor_Central - grosor_Anterior + grosor_Posterior #calculo del grosor total de la lente punto a punto

    numero_Onda = 2 * np.pi / longitud_Onda #numero de onda de la iluminacion incidente sobre la lente
    transmitancia_Lente = opacidad * np.exp(1j * numero_Onda * grosor_Central) * np.exp(1j * numero_Onda * (material-1) * grosor_Lente) #calculamos la transmitancia de la lente
    campo_Salida = campo_Entrada * transmitancia_Lente #calculamos el campo de salida
    
    return campo_Salida #retornamos el campo de salida

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

def imagen_Sistema(sistema, objeto, ventana_Objeto, resolucion, longitud_Onda = 632.8E-9):
    ''' Funcion que saca una prediccion de la imagen geometrica de un campo optico al pasar por un sistema
    ENTRADAS:
    - sistema: diccionario con las propiedades del sistema, proviene de la salida de la funcion "sistema_Optico" definida en el archivo matrices ABCD
    - objeto: campo optico a la entrada del sistema
    - ventana_Objeto: ancho de la ventana en el plano objeto
    - resolucion: Cantidad de muestras que se toma del objeto
    - longitud_Onda: Longitud de onda de la iluminacion
    
    RETORNA:
    Campo optico a la salida del sistema '''
    numero_Onda = (2*np.pi)/longitud_Onda #calculo del numero de onda asociado a la iluminacion incidente
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

def imagen_SistemaShift(sistema, objeto, ventana_Objeto, resolucion, longitud_Onda = 632.8E-9):
    ''' Funcion que saca una prediccion de la imagen geometrica de un campo optico al pasar por un sistema
    ENTRADAS:
    - sistema: diccionario con las propiedades del sistema, proviene de la salida de la funcion "sistema_Optico" definida en el archivo matrices ABCD
    - objeto: campo optico a la entrada del sistema
    - ventana_Objeto: ancho de la ventana en el plano objeto
    - resolucion: Cantidad de muestras que se toma del objeto
    - longitud_Onda: Longitud de onda de la iluminacion
    
    RETORNA:
    Campo optico a la salida del sistema '''
    numero_Onda = (2*np.pi)/longitud_Onda #calculo del numero de onda asociado a la iluminacion incidente
    malla_EntradaXX, malla_EntradaYY = opt.malla_Puntos(resolucion, ventana_Objeto) #Malla de puntos relativa al muestreo del objeto a la entrada del sistema
    deltas = opt.producto_EspacioFrecuenciaFresnel(longitud_Onda, sistema["matriz_Sistema"][0,1], ventana_Objeto, resolucion) #Aplicacion del producto espacio-frecuencia para obtener informacion de los anchos de las ventanas
    longitud_VentanaSalida = resolucion * deltas["delta_Llegada"] #calculamos la longitud de la ventana a la salida usando la resolucion y el producto espacio-frecuencia
    malla_SalidaXX, malla_SalidaYY = opt.malla_Puntos(resolucion, longitud_VentanaSalida) #malla de puntos correspondiente a las coordenadas del plano de salida del sistema
    fase_Constante = np.exp(1j*numero_Onda*sistema["camino_EjeOptico"]) #el termino de fase constante, relativo a la longitud de camino optico que recorre el rayo que pasa por el centro del sistema
    fase_ParabolicaEntrada = np.exp((1j*numero_Onda*sistema["matriz_Sistema"][0,0]*(malla_EntradaXX**2 + malla_EntradaYY**2))/(2*sistema["matriz_Sistema"][0,1])) #fase parabolica que se debe aplicar relativa a las coordenadas del sistema en la salida
    fase_ParabolicaSalida = np.exp((1j*numero_Onda*sistema["matriz_Sistema"][1,1]*(malla_SalidaXX**2 + malla_SalidaYY**2))/(2*sistema["matriz_Sistema"][0,1])) #fase parabolica que se debe aplicar relativa a las coordenadas del sistema en la entrada
    transformada_Fresnel = (np.fft.ifft2(objeto*fase_ParabolicaEntrada)) #calculamos la transformada de fourier modificada, de la transformada de fresnel
    campo_Salida = ((deltas["delta_Llegada"])**2)*fase_Constante*fase_ParabolicaSalida*transformada_Fresnel #calculamos el campo de salida multiplicando por las fases parabolicas y la transformada de fresnel 
    return campo_Salida #retornamos el campo a la salida del sistema


def diafragma_Sistema(ventana, interfases):


    return 0
    
def diafragma_ParLentes(lente_Anterior, lente_Posterior, distancia_Lentes, vector_Entrada):


    return 0


longitud_Onda = 533E-9
lado = 0.05
resolucion = 3000
ancho_Ventana = 4
xx_Entrada, yy_Entrada = opt.malla_Puntos(resolucion, ancho_Ventana)
mascara = opt.funcion_Rectangulo(lado, lado, None, xx_Entrada, yy_Entrada)

foco_LenteAnterior = 0.07
foco_LentePosterior = 0.05
distancia_Adicional = 0.01
distancia_Objeto = 0.3


'''
sistema = [mat.propagacion(foco_LentePosterior), mat.lente_Delgada(foco_LentePosterior), mat.propagacion(distancia_Adicional), mat.propagacion(foco_LenteAnterior), mat.lente_Delgada(foco_LenteAnterior), mat.propagacion(foco_LenteAnterior)]
propiedad_Sistema = mat.sistema_Optico(sistema, foco_LenteAnterior,1,1)
'''
sistema_Anterior = [mat.propagacion(foco_LenteAnterior), mat.lente_Delgada(foco_LenteAnterior), mat.propagacion(foco_LenteAnterior)]
propiedad_SistemaAnterior = mat.sistema_Optico(sistema_Anterior, foco_LenteAnterior, ancho_Ventana)
deltas_Anterior = opt.producto_EspacioFrecuenciaFresnel(longitud_Onda, propiedad_SistemaAnterior["matriz_Sistema"][0,1], ancho_Ventana, resolucion)
ventana_SalidaDiafragma = resolucion*deltas_Anterior["delta_Llegada"]
campo_Anterior = imagen_Sistema(propiedad_SistemaAnterior, mascara, ancho_Ventana, resolucion, longitud_Onda)
#graph.intensidad(campo_Anterior, ventana_SalidaDiafragma)

xx_Diafragma, yy_Diafragma = opt.malla_Puntos(resolucion, ventana_SalidaDiafragma)
diafragma_Campo = opt.funcion_Circulo(1, None, xx_Diafragma, yy_Diafragma)
campo_AnteriorDiafragma = diafragma_Campo * campo_Anterior

sistema_Posterior = [mat.propagacion(foco_LentePosterior), mat.lente_Delgada(foco_LentePosterior), mat.propagacion(distancia_Adicional)]
propiedad_SistemaPosterior = mat.sistema_Optico(sistema_Posterior, distancia_Adicional, ventana_SalidaDiafragma)
deltas_Posterior = opt.producto_EspacioFrecuenciaFresnel(longitud_Onda, propiedad_SistemaPosterior["matriz_Sistema"][0,1], ventana_SalidaDiafragma, resolucion)
ventana_Salida = resolucion*deltas_Posterior["delta_Llegada"]
campo_Salida = imagen_SistemaShift(propiedad_SistemaPosterior, campo_AnteriorDiafragma, ventana_SalidaDiafragma, resolucion, longitud_Onda)



graph.intensidad(mascara, ancho_Ventana, 1, 1)
graph.intensidad(campo_Anterior,ventana_Salida,1, 0.01)
graph.intensidad(campo_AnteriorDiafragma, ventana_SalidaDiafragma, 1, 0.01)
graph.intensidad(campo_Salida, ventana_Salida, 1, 0.001)

