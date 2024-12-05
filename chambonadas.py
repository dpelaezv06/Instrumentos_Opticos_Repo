import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Crear una ventana oculta para el diálogo de archivo
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal de tkinter

# Abrir el diálogo para seleccionar una imagen
ruta_imagen = filedialog.askopenfilename(
    title="Selecciona una imagen",
    filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif")]
)

# Verificar si se seleccionó una imagen
if ruta_imagen:   
    imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)      # Cargar la imagen en escala de grises
    imagen_normalizada = imagen / 255                           # Normalizar los valores de intensidad entre 0 y 1

#Función para seleccionar una imagen desde el PC y convertirla en un array normalizado de escala de grises
def seleccionar_imagen(): 
    root = tk.Tk()                  # Crea una ventana oculta para el diálogo de archivo
    root.withdraw()                 # Oculta la ventana que acabamos de crear, para no mostrar nada
    ruta_imagen = filedialog.askopenfilename(
    title="Selecciona una imagen",
    filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif")])
    array_grises = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)      #Leer la escala de grises
    array_intensidades = array_grises/255                             #Normalizar el Array
    return array_intensidades

#Función para darle una ruta y que devuelva el array correspondiente - solo cuestión de no andar poniendo comandos al ejecutar
def abrir_imagen(ruta):
    array_grises = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
    array_intensidades = array_grises / 255
    return  array_intensidades