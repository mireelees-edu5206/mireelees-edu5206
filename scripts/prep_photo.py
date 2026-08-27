#!/usr/bin/env python3
"""
Script para preparar la foto de perfil.
- Convierte a escala de grises
- Aplica contraste adaptativo (CLAHE) con OpenCV
- Guarda en escala de grises
"""

import cv2
import numpy as np
from PIL import Image
import os

def prep_photo(input_path='mi-foto.jpg', output_path='source-prepped.png'):
    """
    Prepara la foto para conversión ASCII.
    
    Args:
        input_path: Ruta de la imagen de entrada
        output_path: Ruta de la imagen de salida
    """
    # Verificar que el archivo de entrada existe
    if not os.path.exists(input_path):
        print(f"Error: No se encontró {input_path}")
        print("Por favor coloca tu foto como 'mi-foto.jpg' en el directorio raíz")
        return False
    
    print(f"Procesando {input_path}...")
    
    # Cargar imagen
    input_image = Image.open(input_path)
    
    # Convertir a array de numpy para procesamiento con OpenCV
    img_array = np.array(input_image)
    
    # Si tiene canal alpha, convertir a RGB
    if img_array.shape[2] == 4:
        img_rgb = cv2.cvtColor(img_array[:, :, :3], cv2.COLOR_RGBA2RGB)
    else:
        img_rgb = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Convertir a escala de grises
    print("Convirtiendo a escala de grises...")
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    
    # Aplicar CLAHE (Contrast Limited Adaptive Histogram Equalization)
    print("Aplicando contraste adaptativo (CLAHE)...")
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Guardar resultado
    print(f"Guardando resultado en {output_path}...")
    final_image = Image.fromarray(enhanced, mode='L')
    final_image.save(output_path)
    
    print("¡Foto preparada exitosamente!")
    return True

if __name__ == "__main__":
    prep_photo()
