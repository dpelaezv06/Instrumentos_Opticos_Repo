from setuptools import setup, find_packages

setup(
    name='optics',
    version='0.1.0',
    description='Repositorio para contenidos del curso de instrumentos ópticos, incluyendo modelos de difracción y herramientas ópticas',
    author='Jose Diaz, Daniel Pelaez',
    author_email='jodiazgu@unal.edu.co; dpelaezv@unal.edu.co',
    packages=find_packages(include=['optics_library', 'optics_library.*', 'Modelos_Difraccion', 'Modelos_Difraccion.*',
                                    'Optica_Geometrica_Lentes','Optica_Geometrica_Lentes.*']),
    install_requires=[
        'numpy>=1.18.0',
        'opencv-python>=4.5.0',
        'Pillow>=8.0.0',
    ],
)