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

def formacion_Imagen(mascara, ventana, foco, distancia_MascaraLente, distancia_LenteSensor, longitud_onda = 632.8E-9):
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

def imagen_Sistema(sistema, objeto, ventana_PosteriorX, pixeles_X, ventana_PosteriorY = None, pixeles_Y = None, longitud_Onda = 632.8E-9):
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
    muestreo_Anterior = opt.muestreo_SegunSensorFresnel(pixeles_X, ventana_PosteriorX, sistema["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, ventana_PosteriorY) #se calcula el muestreo de la ventana de entrada dependiendod del seensor usado
    ancho_XVentanaAnterior = muestreo_Anterior["delta_XEntrada"] * pixeles_X # ancho de la ventana de la entrada
    ancho_YVentanaAnterior = muestreo_Anterior["delta_YEntrada"] * pixeles_Y # alto de la ventana de la entrada
    malla_XAnterior, malla_YAnterior = opt.malla_Puntos(pixeles_X, ancho_XVentanaAnterior, pixeles_Y, ancho_YVentanaAnterior) #malla de puntos de la entrada
    malla_XPosterior, malla_YPosterior = opt.malla_Puntos(pixeles_X, ventana_PosteriorX, pixeles_Y, ventana_PosteriorY) #malla de puntos de la salida
    delta_XPosterior = ventana_PosteriorX / pixeles_X  # delta de muestreo de la salida en el eje x
    delta_YPosterior = ventana_PosteriorY / pixeles_Y # delta de muestreo de la salida en el eje y

    fase_Constante = np.exp(1j*numero_Onda*sistema["camino_EjeOptico"]) #el termino de fase constante, relativo a la longitud de camino optico que recorre el rayo que pasa por el centro del sistema
    fase_ParabolicaAnterior = np.exp((1j*numero_Onda*sistema["matriz_Sistema"][0,0]*(malla_XAnterior**2 + malla_YAnterior**2))/(2*sistema["matriz_Sistema"][0,1])) #fase parabolica que se debe aplicar relativa a las coordenadas del sistema en la salida
    fase_ParabolicaPosterior = np.exp((1j*numero_Onda*sistema["matriz_Sistema"][1,1]*(malla_XPosterior**2 + malla_YPosterior**2))/(2*sistema["matriz_Sistema"][0,1])) #fase parabolica que se debe aplicar relativa a las coordenadas del sistema en la entrada
    transformada_Fresnel = np.fft.fftshift(np.fft.fft2(objeto*fase_ParabolicaAnterior)) #calculamos la transformada de fourier modificada, de la transformada de fresnel
    campo_Salida = delta_XPosterior*delta_YPosterior*fase_Constante*fase_ParabolicaPosterior*transformada_Fresnel #calculamos el campo de salida multiplicando por las fases parabolicas y la transformada de fresnel 
    return campo_Salida #retornamos el campo a la salida del sistema

def imagen_SistemaShift(sistema, objeto, ventana_PosteriorX, pixeles_X, ventana_PosteriorY = None, pixeles_Y = None, longitud_Onda = 632.8E-9):
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
    muestreo_Anterior = opt.muestreo_SegunSensorFresnel(pixeles_X, ventana_PosteriorX, sistema["matriz_Sistema"][0,1], longitud_Onda, pixeles_Y, ventana_PosteriorY) # se calcula el muestreo de la ventana de entrada segun el muestreo de la salida
    ancho_XVentanaAnterior = muestreo_Anterior["delta_XEntrada"] * pixeles_X # ancho de la ventana de muestreo en el eje x del plano anterior del sistema
    ancho_YVentanaAnterior = muestreo_Anterior["delta_YEntrada"] * pixeles_Y # alto de la ventana de muestreo en el eje y del plano anterior del sistema
    malla_XAnterior, malla_YAnterior = opt.malla_Puntos(pixeles_X, ancho_XVentanaAnterior, pixeles_Y, ancho_YVentanaAnterior) #malla de puntos de la entrada del sistema
    malla_XPosterior, malla_YPosterior = opt.malla_Puntos(pixeles_X, ventana_PosteriorX, pixeles_Y, ventana_PosteriorY) #malla de puntos del plano de salida del sistema
    delta_XPosterior = ventana_PosteriorX / pixeles_X #delta de muestreo de la ventana de salida del sistema en el eje x
    delta_YPosterior = ventana_PosteriorY / pixeles_Y #delta de muestreo de la ventana de salida del sistema en el eje y

    fase_Constante = np.exp(1j*numero_Onda*sistema["camino_EjeOptico"]) #el termino de fase constante, relativo a la longitud de camino optico que recorre el rayo que pasa por el centro del sistema
    fase_ParabolicaAnterior = np.exp((1j*numero_Onda*sistema["matriz_Sistema"][0,0]*(malla_XAnterior**2 + malla_YAnterior**2))/(2*sistema["matriz_Sistema"][0,1])) #fase parabolica que se debe aplicar relativa a las coordenadas del sistema en la salida
    fase_ParabolicaPosterior = np.exp((1j*numero_Onda*sistema["matriz_Sistema"][1,1]*(malla_XPosterior**2 + malla_YPosterior**2))/(2*sistema["matriz_Sistema"][0,1])) #fase parabolica que se debe aplicar relativa a las coordenadas del sistema en la entrada
    transformada_Fresnel = (np.fft.fft2(objeto*fase_ParabolicaAnterior)) #calculamos la transformada de fourier modificada, de la transformada de fresnel
    campo_Salida = delta_XPosterior*delta_YPosterior*fase_Constante*fase_ParabolicaPosterior*transformada_Fresnel #calculamos el campo de salida multiplicando por las fases parabolicas y la transformada de fresnel 
    return campo_Salida #retornamos el campo a la salida del sistema
