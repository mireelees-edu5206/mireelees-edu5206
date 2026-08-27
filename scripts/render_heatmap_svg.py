#!/usr/bin/env python3
"""
Script para renderizar el mapa de calor de contribuciones.
- Lee JSON de contribuciones
- Genera SVG con cuadrícula 53x7
- Usa paleta de verdes de GitHub con animación diagonal
"""

import json
import os
from datetime import datetime, timedelta

def render_heatmap_svg(input_path='data/contributions.json', output_path='contrib-heatmap.svg'):
    """
    Renderiza el mapa de calor de contribuciones en SVG.
    
    Args:
        input_path: Ruta del JSON con datos de contribuciones
        output_path: Ruta del SVG de salida
    """
    # Cargar datos
    print(f"Cargando datos de {input_path}...")
    
    if not os.path.exists(input_path):
        print(f"Error: No se encontró {input_path}")
        print("Ejecuta primero fetch_contributions.py")
        return False
    
    with open(input_path, 'r', encoding='utf-8') as f:
        contributions = json.load(f)
    
    # Convertir a diccionario por fecha
    contrib_dict = {c['date']: c for c in contributions}
    
    # Paleta de colores de GitHub (de oscuro a claro)
    colors = [
        '#161b22',  # Nivel 0 (sin contribuciones)
        '#0e4429',  # Nivel 1
        '#006d32',  # Nivel 2
        '#26a641',  # Nivel 3
        '#39d353',  # Nivel 4
    ]
    
    # Configuración SVG
    box_size = 12
    box_spacing = 3
    padding = 20
    weeks = 53
    days = 7
    
    svg_width = weeks * (box_size + box_spacing) + padding * 2
    svg_height = days * (box_size + box_spacing) + padding * 2 + 30  # +30 para labels
    
    # Calcular fecha de inicio (hace 52 semanas)
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=52)
    start_date = start_date - timedelta(days=start_date.weekday())  # Ajustar al domingo
    
    # Iniciar SVG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">
  <defs>
    <style>
      @keyframes fadeIn {{
        from {{ opacity: 0; transform: scale(0.8); }}
        to {{ opacity: 1; transform: scale(1); }}
      }}
      .contribution-box {{
        rx: 2;
        animation: fadeIn 0.3s ease-out forwards;
        opacity: 0;
      }}
      .day-label {{
        font-family: 'Consolas', monospace;
        font-size: 10px;
        fill: #8b949e;
      }}
      .title {{
        font-family: 'Consolas', monospace;
        font-size: 12px;
        fill: #c9d1d9;
      }}
    </style>
  </defs>
  <rect width="100%" height="100%" fill="#0d1117" rx="8"/>
'''
    
    # Agregar título
    svg_content += f'  <text x="{padding}" y="{padding - 5}" class="title">Contributions (last year)</text>\n'
    
    # Labels de días
    day_labels = ['', 'Mon', '', 'Wed', '', 'Fri', '']
    for day, label in enumerate(day_labels):
        if label:
            y = padding + 30 + day * (box_size + box_spacing) + box_size
            svg_content += f'  <text x="{padding - 5}" y="{y}" class="day-label" text-anchor="end">{label}</text>\n'
    
    # Generar cuadrícula con animación diagonal
    delay = 0
    for week in range(weeks):
        for day in range(days):
            # Calcular fecha
            current_date = start_date + timedelta(weeks=week, days=day)
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Obtener nivel de contribución
            contrib = contrib_dict.get(date_str, {'level': 0, 'count': 0})
            level = contrib['level']
            count = contrib['count']
            
            # Calcular posición
            x = padding + week * (box_size + box_spacing)
            y = padding + 30 + day * (box_size + box_spacing)
            
            # Color según nivel
            color = colors[min(level, 4)]
            
            # Animación escalonada en diagonal
            anim_delay = (week + day) * 0.005
            
            # Agregar rectángulo
            svg_content += f'  <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" class="contribution-box" style="animation-delay: {anim_delay}s;">\n'
            svg_content += f'    <title>{date_str}: {count} contributions</title>\n'
            svg_content += f'  </rect>\n'
    
    # Agregar leyenda
    legend_x = padding
    legend_y = svg_height - 15
    legend_labels = ['Less', '', '', '', '', 'More']
    
    for i, (color, label) in enumerate(zip(colors, legend_labels)):
        x = legend_x + i * (box_size + box_spacing)
        svg_content += f'  <rect x="{x}" y="{legend_y}" width="{box_size}" height="{box_size}" fill="{color}" rx="2"/>\n'
        if label:
            svg_content += f'  <text x="{x + box_size/2}" y="{legend_y - 5}" class="day-label" text-anchor="middle">{label}</text>\n'
    
    svg_content += '</svg>'
    
    # Guardar SVG
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"Mapa de calor generado: {output_path}")
    return True

if __name__ == "__main__":
    render_heatmap_svg()
