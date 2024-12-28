# Instrumentos_Opticos_Repo
 Repositorio que contiene los programas relativos a la asignatura de instrumentos opticos

# Instalación del paquete "optics"

Este archivo proporciona una guía paso a paso para instalar y configurar el paquete "optics" en sistemas operativos Linux y Windows.

---

## Requisitos previos

1. **Python 3.8 o superior**: Asegúrate de tener Python instalado.
   - En Linux, verifica con: `python3 --version` o `python --version`.
   - En Windows, verifica con: `python --version`.

2. **pip**: Asegúrate de que `pip` esté instalado.
   - En Linux: `python3 -m ensurepip --upgrade`
   - En Windows: `python -m ensurepip --upgrade`

3. **Git** (opcional): Si planeas clonar el repositorio desde GitHub.

---

## Instalación en Linux

1. **Clona o descarga el repositorio**:
   - Si tienes Git:  
     ```bash
     git clone https://github.com/tu_usuario/optics.git
     cd optics
     ```
   - O descarga y descomprime el repositorio manualmente, luego navega al directorio raíz:
     ```bash
     cd /ruta/al/directorio/optics
     ```

2. **(Opcional) Crear un entorno virtual**:
   - Crear un entorno virtual:
     ```bash
     python3 -m venv env
     ```
   - Activar el entorno virtual:
     ```bash
     source env/bin/activate
     ```

3. **Instalar el paquete**:
   En el directorio donde está el archivo `setup.py`, ejecuta:
   ```bash
   pip install -e .
