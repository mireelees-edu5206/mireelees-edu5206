#!/usr/bin/env python3
"""
Script para convertir imagen a ASCII art y generar SVG.
- Convierte imagen a caracteres ASCII
- Genera SVG dinámico con colores estilo consola
"""

from PIL import Image
import numpy as np

def image_to_ascii(image_path, output_path='avi-ascii.svg', 
                   ramp=" .`:-=+*cs#%@"):
    """
    Convierte imagen a ASCII art y genera SVG.
    
    Args:
        image_path: Ruta de la imagen de entrada
        output_path: Ruta del SVG de salida
        ramp: Rampa de caracteres ASCII (de oscuro a claro)
    """
    # Cargar imagen
    print(f"Cargando {image_path}...")
    img = Image.open(image_path)
    
    # Redimensionar para ASCII (ancho ~80 caracteres)
    width = 80
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.55)  # 0.55 para compensar altura de caracteres
    
    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    
    # Convertir a escala de grises si no lo está
    if img_resized.mode != 'L':
        img_resized = img_resized.convert('L')
    
    # Convertir a array numpy
    img_array = np.array(img_resized)
    
    # Mapear valores de gris a caracteres ASCII
    # Normalizar de 0-255 a 0-(len(ramp)-1)
    normalized = img_array / 255.0 * (len(ramp) - 1)
    indices = normalized.astype(int)
    
    # Generar líneas ASCII
    ascii_lines = []
    for row in indices:
        line = ''.join([ramp[idx] for idx in row])
        ascii_lines.append(line)
    
    # Generar SVG
    print(f"Generando SVG en {output_path}...")
    generate_svg(ascii_lines, output_path)
    
    print("¡SVG ASCII generado exitosamente!")

def generate_svg(ascii_lines, output_path):
    """
    Genera SVG con caracteres ASCII y colores estilo consola.
    """
    # Colores estilo consola terminal
    colors = [
        '#79c0ff',  # Azul claro
        '#d2a8ff',  # Púrpura
        '#ff7b72',  # Rojo
        '#79c0ff',  # Azul
        '#56d364',  # Verde
        '#ffa657',  # Naranja
    ]
    
    # Configuración SVG
    font_size = 10
    line_height = 12
    char_width = 6
    bg_color = '#0d1117'
    
    # Calcular dimensiones
    max_width = max(len(line) for line in ascii_lines)
    svg_width = max_width * char_width + 20
    svg_height = len(ascii_lines) * line_height + 20
    
    # Iniciar SVG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">
  <style>
    @keyframes typewriter {{
      from {{ opacity: 0; }}
      to {{ opacity: 1; }}
    }}
    .char {{
      font-family: 'Courier New', monospace;
      font-size: {font_size}px;
      animation: typewriter 0.5s ease-in-out forwards;
    }}
  </style>
  <rect width="100%" height="100%" fill="{bg_color}" rx="8"/>
'''
    
    # Agregar caracteres con animación escalonada
    delay = 0
    for y, line in enumerate(ascii_lines):
        for x, char in enumerate(line):
            if char != ' ':
                color = colors[(x + y) % len(colors)]
                svg_content += f'  <text x="{x * char_width + 10}" y="{y * line_height + 15}" fill="{color}" class="char" style="animation-delay: {delay}s;">{char}</text>\n'
                delay += 0.01
    
    svg_content += '</svg>'
    
    # Guardar SVG
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

if __name__ == "__main__":
    image_to_ascii('source-prepped.png')
