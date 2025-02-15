import optics_library.mascaras as opt 
import optics_library.graficas as graph
import numpy as np

mascara = opt.read_tiff("images\Hologram.tiff")
mascara = np.fft.fftshift(np.fft.fft2(mascara))

graph.intensidad(mascara,1,1,0,0.000001)