#!/usr/bin/env python3
"""
Script para generar tarjeta de información estilo neofetch.
- Genera SVG simulando salida de comando neofetch
- Incluye animaciones CSS/SMIL de fade-in escalonadas
"""

def generate_info_card(output_path='info-card.svg'):
    """
    Genera SVG con información del perfil estilo neofetch.
    """
    # Datos del perfil
    username = 'mireelees-edu5206'
    full_name = 'Brayan Eduardo Heras Mireles'
    role = 'Software Engineering Student'
    detail = 'Web & Mobile App Developer'
    
    # Stack técnico
    os = 'GitHub Dark'
    shell = 'zsh'
    de = 'VS Code'
    terminal = 'Windows Terminal'
    cpu = 'Intel/AMD'
    memory = '16GB RAM'
    
    languages = ['Python', 'JavaScript', 'TypeScript']
    frameworks = ['React', 'React Native', 'FastAPI', 'Kivy']
    databases = ['PostgreSQL', 'MySQL']
    tools = ['Git', 'GitHub']
    
    # Colores estilo neofetch
    bg_color = '#0d1117'
    text_color = '#c9d1d9'
    accent_colors = [
        '#79c0ff',  # Azul
        '#d2a8ff',  # Púrpura
        '#ff7b72',  # Rojo
        '#ffa657',  # Naranja
        '#56d364',  # Verde
        '#a5d6ff',  # Azul claro
    ]
    
    # Configuración SVG
    font_size = 14
    line_height = 22
    padding = 20
    svg_width = 500
    svg_height = 400
    
    # Iniciar SVG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">
  <defs>
    <style>
      @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(-5px); }}
        to {{ opacity: 1; transform: translateY(0); }}
      }}
      .info-text {{
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: {font_size}px;
        fill: {text_color};
        animation: fadeIn 0.5s ease-out forwards;
        opacity: 0;
      }}
      .label {{
        fill: {accent_colors[0]};
        font-weight: bold;
      }}
      .value {{
        fill: {text_color};
      }}
      .title {{
        font-size: 16px;
        font-weight: bold;
        fill: {accent_colors[1]};
      }}
      .subtitle {{
        font-size: 12px;
        fill: {accent_colors[3]};
      }}
    </style>
  </defs>
  <rect width="100%" height="100%" fill="{bg_color}" rx="12"/>
'''
    
    # Agregar líneas con animación escalonada
    delay = 0
    y_offset = padding
    
    # Título principal
    svg_content += f'  <text x="{padding}" y="{y_offset}" class="info-text title" style="animation-delay: {delay}s;">{username}@github</text>\n'
    delay += 0.1
    y_offset += line_height
    
    svg_content += f'  <text x="{padding}" y="{y_offset}" class="info-text subtitle" style="animation-delay: {delay}s;">-----------</text>\n'
    delay += 0.1
    y_offset += line_height * 1.5
    
    # Nombre y rol
    svg_content += f'  <text x="{padding}" y="{y_offset}" class="info-text" style="animation-delay: {delay}s;">{full_name}</text>\n'
    delay += 0.1
    y_offset += line_height
    
    svg_content += f'  <text x="{padding}" y="{y_offset}" class="info-text" style="animation-delay: {delay}s;">{role}</text>\n'
    delay += 0.1
    y_offset += line_height
    
    svg_content += f'  <text x="{padding}" y="{y_offset}" class="info-text" style="animation-delay: {delay}s;">{detail}</text>\n'
    delay += 0.15
    y_offset += line_height * 1.5
    
    # Información del sistema
    info_lines = [
        ('OS', os),
        ('Shell', shell),
        ('DE', de),
        ('Terminal', terminal),
        ('CPU', cpu),
        ('Memory', memory),
    ]
    
    for i, (label, value) in enumerate(info_lines):
        color = accent_colors[i % len(accent_colors)]
        svg_content += f'  <text x="{padding}" y="{y_offset}" class="info-text"><tspan class="label" fill="{color}">{label}</tspan><tspan class="value">: {value}</tspan></text>\n'
        delay += 0.08
        y_offset += line_height
    
    y_offset += line_height * 0.5
    
    # Lenguajes
    svg_content += f'  <text x="{padding}" y="{y_offset}" class="info-text label" style="animation-delay: {delay}s;">Languages:</text>\n'
    delay += 0.08
    y_offset += line_height
    svg_content += f'  <text x="{padding + 20}" y="{y_offset}" class="info-text value" style="animation-delay: {delay}s;">{", ".join(languages)}</text>\n'
    delay += 0.08
    y_offset += line_height
    
    # Frameworks
    svg_content += f'  <text x="{padding}" y="{y_offset}" class="info-text label" style="animation-delay: {delay}s;">Frameworks:</text>\n'
    delay += 0.08
    y_offset += line_height
    svg_content += f'  <text x="{padding + 20}" y="{y_offset}" class="info-text value" style="animation-delay: {delay}s;">{", ".join(frameworks)}</text>\n'
    delay += 0.08
    y_offset += line_height
    
    # Bases de datos
    svg_content += f'  <text x="{padding}" y="{y_offset}" class="info-text label" style="animation-delay: {delay}s;">Databases:</text>\n'
    delay += 0.08
    y_offset += line_height
    svg_content += f'  <text x="{padding + 20}" y="{y_offset}" class="info-text value" style="animation-delay: {delay}s;">{", ".join(databases)}</text>\n'
    delay += 0.08
    y_offset += line_height
    
    # Herramientas
    svg_content += f'  <text x="{padding}" y="{y_offset}" class="info-text label" style="animation-delay: {delay}s;">Tools:</text>\n'
    delay += 0.08
    y_offset += line_height
    svg_content += f'  <text x="{padding + 20}" y="{y_offset}" class="info-text value" style="animation-delay: {delay}s;">{", ".join(tools)}</text>\n'
    
    svg_content += '</svg>'
    
    # Guardar SVG
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"Tarjeta de información generada: {output_path}")

if __name__ == "__main__":
    generate_info_card()
