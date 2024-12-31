import numpy as np
import matplotlib.pyplot as plt

def intensidad(campo, ventana):
    ''' Grafica un patron de intensidad del campo ingresado    
    ENTRADAS:
    - campo: campo optico al que se le quiere representar su intensidad
    - ventana: longitud de la ventana que se desea graficar, se grafica en una ventana cuadrada

    RETORNA: Nada, solo despliega una ventana emergente con el grafico de la intensidad dedl campo optico que se quiere representar '''

    ''' Definir los parametros para poder realizar la grafica '''
    limites_eje = np.array([-ventana/2, ventana/2, -ventana/2, ventana/2]) #definimos los valores de los ejes del campo que vamos a representar
    campo_Intensidad = (np.abs(campo))**2 #calculamos la intensidad del campo que se ponga en la entrada

    ''' GRAFICAR '''
    plt.imshow(campo_Intensidad, extent = limites_eje, origin='lower', cmap='gray') #generamos la grafica
    plt.colorbar(label="Intensidad") #agregamos la barra de color para representar la intensidad
    plt.xlabel("X (m)") #ponemos etiquetas en los ejes
    plt.ylabel("Y (m)") #ponemos etiquetas en los ejes
    plt.title("Mapa de Intensidad") #agregamos un titulo en el grafico
    plt.show() #mostramos el grafico

def fase(campo, ventana):
    ''' Grafica un mapa de fase del campo ingresado    
    ENTRADAS:
    - campo: campo optico al que se le quiere representar su distribucion de fase
    - ventana: longitud de la ventana que se desea graficar, se grafica en una ventana cuadrada

    RETORNA: Nada, solo despliega una ventana emergente con el grafico de la distribucion de fase del campo optico que se quiere representar '''

    ''' Definir los parametros para poder realizar la grafica '''
    limites_eje = np.array([-ventana/2, ventana/2, -ventana/2, ventana/2])
    campo_Fase = np.angle(campo) #calculamos la intensidad del campo que se ponga en la entrada

    ''' GRAFICAR '''
    plt.imshow(campo_Fase, extent = limites_eje, origin='lower', cmap='rainbow') #generamos la grafica
    plt.colorbar(label="Fase") #agregamos la barra de color para representar la distribucion de fase
    plt.xlabel("X (m)") #ponemos etiquetas en los ejes
    plt.ylabel("Y (m)") #ponemos etiquetas en los ejes
    plt.title("Mapa de fase") #agregamos un titulo en el grafico
    plt.show() #mostramos el grafico


